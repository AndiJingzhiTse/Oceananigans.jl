#!/usr/bin/env python3
"""Run matched baseline/Dagger benchmark series for either model locally."""
import argparse
import copy
import fcntl
import json
import shutil
import os
import time
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

import benchmark_suite as runner
from suite.plan import machine_series, ALL_SERIES, MODEL_FOLDERS
from suite.catalog import publish_series, write_machine_report
from suite.variants import write_comparison
from suite.storage import archive_finished_case, archive_runtime, runtime_environment, digest


def profile_manifest(destination):
    files = [dict(path=str(path), bytes=path.stat().st_size, sha256=digest(path))
             for path in sorted((destination / 'raw_profiles').rglob('*')) if path.is_file()]
    if files:
        runner.atomic_json(destination / 'profile_manifest.json', files)


def annotate_failures(folder, data):
    for case in data['cases']:
        if case['state'] not in ('FAILED', 'OUT_OF_MEMORY'):
            continue
        case_dir = folder / case['id']
        logs = [case_dir / 'job.out', *case_dir.glob('rank_*/profile.out')]
        messages = []
        for log in logs:
            if log.exists():
                messages.extend(line for line in log.read_text(errors='replace').splitlines()
                                if any(marker in line for marker in ('OutOfGPUMemoryError', 'OutOfMemoryError',
                                    'Out of GPU memory', 'Pressure solve failed', 'Recomputed pressure residual', 'ERROR:')))
        memory_errors = [line for line in messages if any(marker in line for marker in
                         ('OutOfGPUMemoryError', 'OutOfMemoryError', 'Out of GPU memory'))]
        if messages:
            case['details'] = 'Execution failed; ' + (memory_errors or messages)[0][:1000]
        if memory_errors:
            case['state'] = 'OUT_OF_MEMORY'
    runner.atomic_json(folder / 'suite.json', data)


def commit_records(destination):
    # Only the study's designated result tree is staged. Never stage user edits
    # elsewhere or consume an existing staged change.
    repo = runner.REPO
    if subprocess.run(['git', '-C', str(repo), 'diff', '--cached', '--quiet']).returncode:
        raise RuntimeError('Index contains unrelated staged changes; refusing automatic commit')
    relative = str(destination.relative_to(repo))
    subprocess.run(['git', '-C', str(repo), 'add', '-u', '--', relative], check=True)
    # New curated JSON/Markdown files are ignored globally. Add scientific
    # records explicitly while keeping captures and closed raw logs out of Git.
    paths = [str(p.relative_to(repo)) for p in destination.rglob('*') if p.is_file()
             and (p.relative_to(destination).parts[0] in {'baseline', 'dagger', 'comparisons'} or
                  len(p.relative_to(destination).parts) == 1)
             and (p.suffix in {'.json', '.md', '.csv', '.svg', '.toml', '.txt'} or p.name == 'source.tar.gz')
             and not {'raw_profiles', 'run_records', '.runtime', '__pycache__'}.intersection(p.relative_to(destination).parts)
             and not p.name.endswith(('.lock', '.tmp')) and p.stat().st_size < 64 * 1024**2]
    for offset in range(0, len(paths), 100):
        subprocess.run(['git', '-C', str(repo), 'add', '-f', '--', *paths[offset:offset + 100]], check=True)
    if subprocess.run(['git', '-C', str(repo), 'diff', '--cached', '--quiet']).returncode:
        subprocess.run(['git', '-C', str(repo), 'commit', '-m',
                        f'Record {destination.name} {destination.parent.name} baseline and Dagger outcomes'], check=True)


def free_gpu_uuids():
    devices = runner.command(['nvidia-smi', '--query-gpu=index,uuid,memory.used', '--format=csv,noheader,nounits'])
    processes = runner.command(['nvidia-smi', '--query-compute-apps=gpu_uuid', '--format=csv,noheader'])
    if devices.returncode or processes.returncode:
        raise RuntimeError('Cannot verify GPU availability with nvidia-smi')
    occupied = set(processes.stdout.strip().splitlines())
    visible = os.environ.get('CUDA_VISIBLE_DEVICES')
    allowed = visible.split(',') if visible is not None else None
    available = []
    for line in devices.stdout.splitlines():
        index, uuid, memory = [part.strip() for part in line.split(',')]
        if allowed is not None and index not in allowed and uuid not in allowed:
            continue
        if uuid not in occupied and float(memory) <= 256:
            available.append(uuid)
    return available


def pending_pairs(studies, selected):
    pairs = []
    for order, series in enumerate(selected):
        cases = sorted(studies['baseline', series][1]['cases'], key=lambda c: (c['ranks'], c['id']))
        for index, case in enumerate(cases):
            modes = ('baseline', 'dagger') if index % 2 == 0 else ('dagger', 'baseline')
            if any(next(c for c in studies[mode, series][1]['cases'] if c['id'] == case['id'])['state'] == 'PLANNED'
                   for mode in modes):
                pairs.append((case['ranks'], order, index, series, case, modes))
    return sorted(pairs, key=lambda item: item[:3])


def source_fingerprint():
    paths = ('src', 'Project.toml', 'benchmarking/src', 'benchmarking/Project.toml')
    if subprocess.run(['git', '-C', str(runner.REPO), 'diff', '--quiet', 'HEAD', '--', *paths]).returncode:
        raise RuntimeError('Benchmark source has uncommitted changes; stop the study before editing code')
    return dict(zip(paths, subprocess.check_output(
        ['git', '-C', str(runner.REPO), 'rev-parse', *['HEAD:' + p for p in paths]], text=True).splitlines()))


def verify_source(expected, study):
    try:
        if source_fingerprint() != expected:
            raise RuntimeError('Source changed; stop this study before switching branches or changing physics')
    except RuntimeError as error:
        runner.atomic_json(study / 'progress.json', dict(state='STOPPED_SOURCE_CHANGE', details=str(error)))
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--study', type=Path, required=True, help='Fresh scratch directory, or an existing study to resume')
    parser.add_argument('--publish', type=Path, required=True)
    parser.add_argument('--project', type=Path, required=True, help='Shared isolated Julia environment including Dagger')
    parser.add_argument('--plan', action='store_true')
    parser.add_argument('--refresh', action='store_true')
    parser.add_argument('--commit', action='store_true')
    parser.add_argument('--series', help='Comma-separated subset; existing other series remain in comparisons')
    parser.add_argument('--model', choices=tuple(MODEL_FOLDERS), default='NonhydrostaticModel')
    parser.add_argument('--gpu-only', action='store_true', help='Select GPU series only; reject CPU selections')
    parser.add_argument('--wait-for-gpus', action='store_true', help='Use idle GPUs and wait without holding devices when busy')
    args = parser.parse_args()
    study, destination = args.study.resolve(), args.publish.resolve()
    family = next((p.name for p in (destination, *destination.parents) if p.name in MODEL_FOLDERS.values()), None)
    if family and family != MODEL_FOLDERS[args.model]:
        raise ValueError('Publication destination belongs to the other model family')
    study.mkdir(parents=True, exist_ok=True)
    with (study / '.paired.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        server = runner.load_server(args.config, args.model)
        if server['backend'] != 'local':
            raise ValueError('The paired runner currently supports local execution only')
        server['project'] = str(args.project.resolve())
        selected = tuple(args.series.split(',')) if args.series else machine_series(server)
        if args.gpu_only:
            if args.series and any(not s.startswith('gpu_') for s in selected):
                raise ValueError('--gpu-only cannot include CPU series')
            selected = tuple(s for s in selected if s.startswith('gpu_'))
        if not selected or len(selected) != len(set(selected)) or set(selected) - set(ALL_SERIES):
            raise ValueError('Choose unique series names from the benchmark catalog')
        if args.wait_for_gpus and any(not s.startswith('gpu_') for s in selected):
            raise ValueError('--wait-for-gpus requires GPU-only series')
        studies = {}
        for mode in ('baseline', 'dagger'):
            for series in selected:
                folder = study / mode / series
                if (folder / 'suite.json').exists():
                    data = json.loads((folder / 'suite.json').read_text())
                    if data['server']['model_type'] != args.model:
                        raise ValueError('Existing study belongs to a different model')
                    runner.refresh(folder, data, query_slurm=False)
                    # A prior process can be interrupted before its controller
                    # commits the case outcome. Do not silently rerun live work.
                    if any(c['state'] == 'RUNNING' for c in data['cases']):
                        raise RuntimeError(f'Unfinished execution marker in {folder}; inspect its processes before resuming')
                else:
                    settings = copy.deepcopy(server)
                    settings['execution_mode'] = mode
                    data = runner.prepare(folder, settings, (series,))
                # Applies to resumed suites too: old snapshots can retain a
                # /tmp trace root even when the study itself is on scratch.
                data['server']['trace_root'] = str(destination / mode)
                data['server']['profile_layout'] = 'series'
                studies[mode, series] = (folder, data)

        def publish():
            for (mode, series), (folder, data) in studies.items():
                annotate_failures(folder, data)
                for case in data['cases']:
                    archive_finished_case(folder, case, destination / mode)
                publish_series(folder, destination / mode / series)
            for mode in ('baseline', 'dagger'):
                (destination / mode).mkdir(parents=True, exist_ok=True)
                write_machine_report(destination / mode)
                write_machine_report(study / mode)
            report_series = tuple(s for s in machine_series(server)
                                  if any((study / mode / s / 'suite.json').exists() for mode in ('baseline', 'dagger')))
            write_comparison(study, destination, selected=report_series, model_type=args.model)
            if args.commit:
                commit_records(destination)

        publish()
        if args.plan or args.refresh:
            return
        if args.wait_for_gpus:
            guard_path = study / 'source_guard.json'
            expected_source = json.loads(guard_path.read_text()) if guard_path.exists() else source_fingerprint()
            runner.atomic_json(guard_path, expected_source)
            while pairs := pending_pairs(studies, selected):
                verify_source(expected_source, study)
                available = free_gpu_uuids()
                chosen = None
                for item in pairs:
                    ranks, _, _, series, case, modes = item
                    allocation = study / 'allocations' / series / (case['id'] + '.json')
                    previous = json.loads(allocation.read_text()) if allocation.exists() else None
                    devices = previous['gpu_uuids'] if previous else available[:ranks]
                    if len(devices) == ranks and set(devices) <= set(available):
                        chosen = item, devices, allocation
                        break
                if chosen is None:
                    runner.atomic_json(study / 'progress.json', dict(state='WAITING_FOR_GPUS',
                        pending_pairs=len(pairs), free_gpu_uuids=available,
                        updated_at=datetime.now(timezone.utc).isoformat()))
                    print(f'Waiting for idle GPUs: {len(pairs)} pairs pending; {len(available)} devices free', flush=True)
                    time.sleep(30)
                    continue
                (_, _, _, series, case, modes), devices, allocation = chosen
                allocation.parent.mkdir(parents=True, exist_ok=True)
                runner.atomic_json(allocation, dict(gpu_uuids=devices, series=series, case=case['id']))
                for mode in modes:
                    folder, data = studies[mode, series]
                    target = next(c for c in data['cases'] if c['id'] == case['id'])
                    if target['state'] != 'PLANNED':
                        continue
                    while not set(devices) <= set(free_gpu_uuids()):
                        runner.atomic_json(study / 'progress.json', dict(state='WAITING_FOR_GPUS',
                            series=series, case=case['id'], mode=mode, requested_gpu_uuids=devices))
                        time.sleep(30)
                    verify_source(expected_source, study)
                    if target.get('configuration', {}).get('profile') and shutil.disk_usage(destination).free < 32 * 1024**3:
                        runner.atomic_json(study / 'progress.json', dict(state='STOPPED_STORAGE',
                            details='Less than 32 GiB free before an Nsight capture'))
                        raise RuntimeError('Insufficient free storage for the next Nsight capture')
                    runtime = study / mode / series / '.runtime' / case['id']
                    data['server']['environment'].update(runtime_environment(runtime), CUDA_VISIBLE_DEVICES=','.join(devices))
                    runner.atomic_json(study / 'progress.json', dict(state='RUNNING', series=series,
                        case=case['id'], mode=mode, gpu_uuids=devices, pending_pairs=len(pairs)))
                    print(f'{datetime.now(timezone.utc).isoformat()} {mode}/{series}/{case["id"]} GPUs={devices}', flush=True)
                    runner.execute(folder, data, case_ids={case['id']}, on_start=publish)
                    if source_fingerprint() != expected_source:
                        target.update(state='INVALID', details='Source changed during execution; timings excluded')
                        target.pop('measurement', None)
                        runner.atomic_json(folder / 'suite.json', data)
                    if target.get('configuration', {}).get('profile'):
                        profile_manifest(destination / mode / series)
                    archive_runtime(runtime, destination / mode / series / 'run_records' / case['id'] / 'runtime')
                    publish()
            runner.atomic_json(study / 'progress.json', dict(state='COMPLETED', updated_at=datetime.now(timezone.utc).isoformat()))
            print('All planned baseline and Dagger cases have reached terminal outcomes.', flush=True)
            return
        # Exercise every feasible GPU series before the potentially multi-day
        # CPU cases. Large-rank CPU runs go first, then single-core resolutions.
        order = (selected if 'gpu_weak_scaling' in selected or 'gpu_ensemble' in selected else
                 ('gpu_resolution', 'gpu_scaling_super_fine', 'gpu_partition_super_fine',
                  'gpu_nsight_scaling_super_fine', 'gpu_weak_scaling_super_fine',
                  'gpu_scaling_super_super_fine', 'gpu_scaling_super_super_super_fine',
                  'cpu_partition_cores_super_fine', 'cpu_mpi_scaling_super_fine', 'cpu_resolution'))
        for series in (s for s in order if s in selected):
            base_cases = studies['baseline', series][1]['cases']
            cases = sorted(base_cases, key=lambda c: (-c['ranks'] if series.startswith('cpu_') else c['ranks'], c['id']))
            for index, case in enumerate(cases):
                # Alternate the order to reduce consistent first/second bias.
                for mode in (('baseline', 'dagger') if index % 2 == 0 else ('dagger', 'baseline')):
                    folder, data = studies[mode, series]
                    target = next(c for c in data['cases'] if c['id'] == case['id'])
                    if target['state'] != 'PLANNED':
                        continue
                    case_dir = folder / case['id']
                    runtime = study / mode / series / '.runtime' / case['id']
                    data['server']['environment'].update(runtime_environment(runtime))
                    for tool, command in (
                        ('processes', ['ps', '-eo', 'user,pid,psr,pcpu,rss,args', '--sort=-pcpu']),
                        ('gpu_activity', ['nvidia-smi', '--query-gpu=uuid,memory.used,utilization.gpu', '--format=csv']),
                    ):
                        if shutil.which(command[0]):
                            result = runner.command(command)
                            (case_dir / f'{tool}_before.txt').write_text(result.stdout)
                    print(f"{datetime.now(timezone.utc).isoformat()} {mode}/{series}/{case['id']}", flush=True)
                    runner.execute(folder, data, case_ids={case['id']}, on_start=publish)
                    if target.get('configuration', {}).get('profile'):
                        profile_manifest(destination / mode / series)
                    archive_runtime(runtime, destination / mode / series / 'run_records' / case['id'] / 'runtime')
                    publish()
        print('All planned baseline and Dagger cases have reached terminal outcomes.', flush=True)


if __name__ == '__main__':
    main()
