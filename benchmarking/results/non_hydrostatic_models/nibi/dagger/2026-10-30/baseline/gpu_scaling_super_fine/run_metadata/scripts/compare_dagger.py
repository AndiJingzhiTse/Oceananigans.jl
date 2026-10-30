#!/usr/bin/env python3
"""Run every nonhydrostatic series in matched baseline/Dagger pairs locally."""
import argparse
import copy
import fcntl
import json
import shutil
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

import benchmark_suite as runner
from suite.plan import machine_series, ALL_SERIES
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
    subprocess.run(['git', '-C', str(repo), 'add', '--', relative], check=True)
    if subprocess.run(['git', '-C', str(repo), 'diff', '--cached', '--quiet']).returncode:
        subprocess.run(['git', '-C', str(repo), 'commit', '-m',
                        'Record Rondeau nonhydrostatic baseline and Dagger study outcomes'], check=True)


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
    args = parser.parse_args()
    study, destination = args.study.resolve(), args.publish.resolve()
    study.mkdir(parents=True, exist_ok=True)
    with (study / '.paired.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        server = runner.load_server(args.config, 'NonhydrostaticModel')
        if server['backend'] != 'local':
            raise ValueError('The paired runner currently supports local execution only')
        server['project'] = str(args.project.resolve())
        selected = tuple(args.series.split(',')) if args.series else machine_series(server)
        if not selected or len(selected) != len(set(selected)) or set(selected) - set(ALL_SERIES):
            raise ValueError('Choose unique series names from the benchmark catalog')
        studies = {}
        for mode in ('baseline', 'dagger'):
            for series in selected:
                folder = study / mode / series
                if (folder / 'suite.json').exists():
                    data = json.loads((folder / 'suite.json').read_text())
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
            write_comparison(study, destination, selected=report_series)
            if args.commit:
                commit_records(destination)

        publish()
        if args.plan or args.refresh:
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
