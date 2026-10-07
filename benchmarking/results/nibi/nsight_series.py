#!/usr/bin/env python3
"""Submit and summarize six super-fine Nsight Systems GPU profiles on Nibi."""
import argparse
import csv
import fcntl
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import time

from refresh_scaling import TERMINAL, commit_results
from scaling import read_results

SCRIPT_DIR = Path(__file__).resolve().parent
BRANCH = 'codex/nibi-benchmarking'
CASES = {1: ('1x1x1',), 2: ('2x1x1', '1x2x1'), 4: ('4x1x1', '2x2x1', '1x4x1')}
CATEGORIES = ('Gc', 'Gu', 'Gv', 'Others')


def run(*args):
    return subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)


def parse_job(output):
    return next(line.strip().split(';')[0] for line in reversed(output.splitlines())
                if re.fullmatch(r'\d+(;\S+)?', line.strip()))


def config_for(gpus, partition):
    dims = list(map(int, partition.split('x')))
    if len(dims) != 3 or any(p <= 0 for p in dims) or math.prod(dims) != gpus or any(n % p for n, p in zip((1440, 720, 200), dims)):
        raise ValueError('Invalid partition')
    return dict(gpus=gpus, partition=dims, grid_name='super_fine', global_resolution=[1440, 720, 200],
                local_resolution=[n // p for n, p in zip((1440, 720, 200), dims)],
                grid_type='LatitudeLongitudeGrid', float_type='Float64', dt=60,
                warmup_steps=2, time_steps=10, samples=5, free_surface_substeps=30,
                extend_free_surface_halos=True, traces=['cuda', 'nvtx', 'mpi'],
                capture_range='cudaProfilerApi', capture_scope='timing windows after two untimed steps')


def submit(folder):
    if (folder / 'jobs.json').exists():
        raise SystemExit('Already submitted; use a new directory for another series')
    metadata = folder / 'run_metadata'
    metadata.mkdir(exist_ok=True)
    for name in ('Project.toml', 'Manifest.toml', 'LocalPreferences.toml'):
        shutil.copy2(SCRIPT_DIR / 'environment' / name, metadata / name)
    for name in ('nsight_series.py', 'nsight_series.sbatch', 'nsight_rank.sh', 'run_gpu_nsight.jl',
                 'finalize_nsight.sbatch', 'scaling.py', 'refresh_scaling.py'):
        shutil.copy2(SCRIPT_DIR / name, metadata / name)
    for source in (SCRIPT_DIR / '../../run_benchmarks.jl', SCRIPT_DIR / '../../src/earth_ocean.jl'):
        shutil.copy2(source, metadata / source.name)
    (metadata / 'revision.txt').write_text(run('git', '-C', str(SCRIPT_DIR), 'rev-parse', 'HEAD').stdout)
    trace_root = Path('/scratch/anditse/nsight_traces') / folder.name
    trace_root.mkdir(parents=True, exist_ok=True)
    (metadata / 'trace_root.txt').write_text(str(trace_root) + '\n')
    jobs = []
    for gpus, partitions in CASES.items():
        group = folder / f'{gpus}_gpus'
        group.mkdir(exist_ok=True)
        for partition in partitions:
            case = group / partition
            case.mkdir(exist_ok=True)
            config = config_for(gpus, partition)
            (case / 'configuration.json').write_text(json.dumps(config, indent=2) + '\n')
            (case / 'configuration.md').write_text(
                '# Profiling configuration\n\nGlobal resolution: 1440 × 720 × 200 (`super_fine`).\n'
                f"Grid type: LatitudeLongitudeGrid. MPI partition: {partition}.\n"
                f"Local resolution per rank: {' × '.join(map(str, config['local_resolution']))}.\n"
                f'{gpus} H100 GPUs, one MPI rank and one Julia thread per GPU, on one node.\n'
                'Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3, Δt=60 s.\n'
                'Free-surface substeps=30 requested; extend_halos=true.\n'
                'Two untimed steps: one warmup step and one unprofiled preflight window.\n'
                'Nsight captures five ten-step timing windows and timing-helper finalization.\n'
                'CUDA profiler API start/stop markers exclude initialization and warmup; JSON output and finite-state checks follow capture.\n')
        minutes = {1: 30, 2: 45, 4: 60}[gpus]
        limit = '01:00:00' if minutes == 60 else f'00:{minutes:02}:00'
        command = ['sbatch', '--parsable', '--account=def-fpoulin_gpu', f'--job-name=nibi_nsys_{gpus}',
                   f'--ntasks={gpus}', f'--ntasks-per-node={gpus}', f'--time={limit}',
                   f'--output={group}/job.out', str(SCRIPT_DIR / 'nsight_series.sbatch'), str(group),
                   str(trace_root / f'{gpus}_gpus'), str(SCRIPT_DIR), *partitions]
        result = run(*command)
        (group / 'submission.txt').write_text('Command: ' + ' '.join(command) + '\n' + result.stdout)
        job = dict(gpus=gpus, partitions=list(partitions), job_id='',
                   state='SUBMISSION_FAILED' if result.returncode else 'SUBMITTED', details=result.stdout.strip())
        if not result.returncode:
            job['job_id'] = parse_job(result.stdout)
            (group / 'job_id.txt').write_text(job['job_id'] + '\n')
        jobs.append(job)
        (folder / 'jobs.json').write_text(json.dumps(jobs, indent=2) + '\n')
        print(f"{gpus} GPUs: {job['state']} {job['job_id']}", flush=True)
    ids = [j['job_id'] for j in jobs if j['job_id']]
    if ids:
        finalizer = run('sbatch', '--parsable', '--account=def-fpoulin_cpu',
                        '--dependency=afterany:' + ':'.join(ids), f'--output={folder}/finalize.out',
                        str(SCRIPT_DIR / 'finalize_nsight.sbatch'), str(folder), str(SCRIPT_DIR))
        (metadata / 'finalizer_submission.txt').write_text(finalizer.stdout)
        if finalizer.returncode:
            raise RuntimeError('Profiles submitted; finalizer failed: ' + finalizer.stdout)
        (metadata / 'finalizer_job_id.txt').write_text(parse_job(finalizer.stdout) + '\n')


def kernel_summary(path):
    totals = dict.fromkeys(CATEGORIES, 0)
    with path.open() as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError('Empty CUDA kernel summary')
    for row in rows:
        duration = int(row['Total Time (ns)'].replace(',', ''))
        if duration < 0 or int(row['Instances'].replace(',', '')) <= 0:
            raise ValueError('Invalid kernel statistics')
        category = next((c for c in CATEGORIES[:-1] if f'compute_hydrostatic_free_surface_{c}' in row['Name']), 'Others')
        totals[category] += duration
    if sum(totals.values()) <= 0:
        raise ValueError('No recorded GPU kernel activity')
    return totals


def validate(case, gpus, partition):
    entries = read_results(case, gpus, tuple(map(int, partition.split('x'))))
    expected = config_for(gpus, partition)
    layout = json.loads((case / 'gpu_layout.json').read_text())
    if (len(layout) != gpus or {r['rank'] for r in layout} != set(range(gpus))
            or len({r['gpu_uuid'] for r in layout}) != gpus or len({r['hostname'] for r in layout}) != 1):
        raise ValueError('Expected distinct GPUs on one node and complete rank layout')
    for entry in entries:
        if entry['configuration'] != expected or entry.get('finite_state') is not True or entry['metadata']['num_threads'] != 1:
            raise ValueError('Unexpected profiling configuration or invalid model state')
        values = [entry[k] for k in ('time_per_step_seconds', 'time_per_step_median_seconds', 'time_per_step_max_seconds')]
        if any(not math.isfinite(v) or v <= 0 for v in values) or values != sorted(values):
            raise ValueError('Invalid timing statistics')
    totals = dict.fromkeys(CATEGORIES, 0)
    traces = []
    for rank in range(gpus):
        destination = case / f'rank_{rank}'
        if (destination / 'exit_code.txt').read_text().strip() != '0':
            raise ValueError(f'Rank {rank} profile/export failed')
        trace = Path((destination / 'trace_path.txt').read_text().strip())
        size = int((destination / 'trace_bytes.txt').read_text())
        checksum = (destination / 'trace_sha256.txt').read_text().split()[0]
        if trace.suffix != '.nsys-rep' or size <= 0 or trace.stat().st_size != size or not re.fullmatch(r'[0-9a-f]{64}', checksum):
            raise ValueError(f'Rank {rank} trace manifest invalid or raw trace missing')
        for key, value in kernel_summary(destination / 'summary_cuda_gpu_kern_sum.csv').items():
            totals[key] += value
        traces.append(dict(rank=rank, gpu_uuid=next(r['gpu_uuid'] for r in layout if r['rank'] == rank),
                           path=str(trace), bytes=size, sha256=checksum))
    with (case / 'raw_traces.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, traces[0].keys(), lineterminator='\n')
        writer.writeheader()
        writer.writerows(traces)
    return max(e['time_per_step_seconds'] for e in entries), max(e['time_per_step_median_seconds'] for e in entries), totals


def refresh(folder):
    jobs = json.loads((folder / 'jobs.json').read_text())
    ids = [j['job_id'] for j in jobs if j['job_id']]
    records, queued = {}, {}
    if ids:
        accounting = run('sacct', '-X', '-n', '-P', '-j', ','.join(ids), '--format=JobIDRaw,State%40,ExitCode,Reason%200')
        if accounting.returncode:
            (folder / 'accounting_error.txt').write_text(accounting.stdout)
            print('Accounting unavailable; finished case markers and live queue remain available.', flush=True)
        else:
            (folder / 'accounting.txt').write_text(accounting.stdout)
            records = {r[0]: r for line in accounting.stdout.splitlines() if len(r := line.split('|')) >= 4}
        active = []
        for j in jobs:
            record = records.get(j['job_id'])
            if record:
                j['state'] = record[1].split()[0].rstrip('+')
                j['details'] = f'{record[1]}, exit {record[2]}; {record[3]}'
            finished = all((folder / f"{j['gpus']}_gpus" / p / 'finished.txt').exists() for p in j['partitions'])
            if finished and not record:
                j['state'] = 'COMPLETED' if all((folder / f"{j['gpus']}_gpus" / p / 'exit_code.txt').read_text().strip() == '0' for p in j['partitions']) else 'FAILED'
            if j['job_id'] and j['state'] not in TERMINAL and not finished:
                active.append(j['job_id'])
        if active:
            queue = run('squeue', '--start', '-h', '-j', ','.join(active), '-o', '%i|%T|%R|%S')
            if queue.returncode:
                raise RuntimeError(queue.stdout)
            (folder / 'queue.txt').write_text(queue.stdout)
            queued = {r[0]: r for line in queue.stdout.splitlines() if len(r := line.split('|')) >= 4}
    rows, summaries = [], {}
    for j in jobs:
        q = queued.get(j['job_id'])
        if q:
            j['state'], j['details'] = q[1], f'{q[2]}; estimated start {q[3]} America/Toronto'
        for partition in j['partitions']:
            case = folder / f"{j['gpus']}_gpus" / partition
            state, details = j['state'], j['details']
            fastest = median = None
            if (case / 'finished.txt').exists():
                state = 'FAILED'
                details = f"Benchmark/export exit {(case / 'exit_code.txt').read_text().strip()}; see job.out and rank logs"
                if (case / 'exit_code.txt').read_text().strip() == '0':
                    try:
                        fastest, median, totals = validate(case, j['gpus'], partition)
                        state, details = 'COMPLETED', 'All rank timings, finite states, traces and CUDA kernel exports verified'
                        summaries[f"{j['gpus']} GPUs {partition}"] = totals
                    except (ValueError, KeyError, OSError, TypeError) as error:
                        state, details = 'INVALID_RESULTS', str(error)
            elif (case / 'started.txt').exists():
                state = 'INTERRUPTED' if j['state'] in TERMINAL else 'RUNNING'
            elif j['state'] in TERMINAL and j['state'] != 'SUBMISSION_FAILED':
                state = 'NOT_RUN'
            elif j['state'] == 'RUNNING':
                state = 'WAITING'
            rows.append(dict(gpus=j['gpus'], partition=partition, resolution='1440x720x200', grid_type='LatitudeLongitudeGrid',
                             job_id=j['job_id'], state=state, fastest=fastest, median=median, details=details))
    (folder / 'jobs.json').write_text(json.dumps(jobs, indent=2) + '\n')
    with (folder / 'results.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, rows[0].keys(), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    report(folder, rows, summaries)
    print('; '.join(f"{r['gpus']} GPUs {r['partition']}: {r['state']}" for r in rows), flush=True)
    return all(j['state'] in TERMINAL for j in jobs), rows


def report(folder, rows, summaries):
    lines = ['# Nsight Systems — super-fine GPU series', '',
             'Global resolution: **1440 × 720 × 200**. Grid type: **LatitudeLongitudeGrid**. Float64, one MPI rank per GPU.',
             'CUDA, NVTX and OpenMPI traces; capture starts after two untimed steps and covers five ten-step timing windows.',
             'Model: WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3, Δt=60 s, requested free-surface substeps=30, extend_halos=true.',
             'The layouts for each GPU count run sequentially on the same allocated GPU set, with fresh Julia/MPI processes.',
             'Profiled timings include instrumentation overhead and are separate from the existing unprofiled scaling series.', '']
    if summaries:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        plt.rcParams.update({'svg.hashsalt': 'nibi-nsight', 'svg.fonttype': 'none'})
        fig, ax = plt.subplots(figsize=(9, 4.8))
        labels = list(summaries)
        bottom = [0.0] * len(labels)
        for category in CATEGORIES:
            shares = [100 * s[category] / sum(s.values()) for s in summaries.values()]
            ax.bar(labels, shares, bottom=bottom, label=category)
            bottom = [a + b for a, b in zip(bottom, shares)]
        ax.set(ylabel='Share of summed rank GPU kernel duration (%)', title='Nsight Systems — 1440 × 720 × 200')
        ax.tick_params(axis='x', labelrotation=15)
        ax.legend(ncol=4)
        fig.tight_layout()
        svg = folder / 'kernel_breakdown.svg'
        fig.savefig(svg, metadata={'Date': None})
        svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n')
        plt.close(fig)
        lines += ['![GPU kernel breakdown](kernel_breakdown.svg)', '']
    lines += ['| GPUs | Partition | Resolution | Grid type | Job | State | Profiled fastest s/step | Median s/step | Details |',
              '|---:|---|---|---|---|---|---:|---:|---|']
    for r in rows:
        timing = f"{r['fastest']:.6f} | {r['median']:.6f}" if r['fastest'] else '— | —'
        details = r['details'].replace('|', '/').replace('\n', ' ')
        lines.append(f"| {r['gpus']} | {r['partition']} | {r['resolution']} | {r['grid_type']} | {r['job_id']} | {r['state']} | {timing} | {details} |")
    lines += ['', 'Kernel categories follow the existing Rondeau Nsight grouping: hydrostatic Gc (tracers), Gu, Gv, and all other kernels.',
              'Fractions use summed GPU kernel duration across ranks, not elapsed wall time. Concurrent activities may overlap; MPI CPU durations cannot be added to GPU durations to form a wall-time percentage.',
              'Every rank retains CUDA kernel/API/memory, MPI and NVTX summaries when those events are available. Missing optional MPI/NVTX reports are recorded in their export logs.',
              'Raw .nsys-rep traces and exported SQLite databases live in scratch; completed cases have raw_traces.csv with paths, sizes and SHA-256 checksums. Text summaries and timing/configuration metadata are committed here.', '',
              '[Nsight capture and MPI profiling documentation](https://docs.nvidia.com/nsight-systems/UserGuide/index.html)']
    for label, totals in summaries.items():
        lines += ['', f'## {label}', '', '| Category | Summed GPU seconds | Share |', '|---|---:|---:|']
        for category in CATEGORIES:
            lines.append(f'| {category} | {totals[category] / 1e9:.6f} | {100 * totals[category] / sum(totals.values()):.2f}% |')
    (folder / 'plot.md').write_text('\n'.join(lines) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_dir', type=Path)
    parser.add_argument('--submit', action='store_true')
    parser.add_argument('--watch', action='store_true')
    parser.add_argument('--commit', action='store_true')
    args = parser.parse_args()
    folder = args.run_dir.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    if args.submit:
        submit(folder)
    committed = set()
    while True:
        try:
            with (folder / '.controller.lock').open('a') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                done, rows = refresh(folder)
                finished = {(r['gpus'], r['partition'], r['state']) for r in rows if r['state'] in TERMINAL or r['state'] in {'INTERRUPTED', 'NOT_RUN'}}
                if args.commit and (done or finished - committed):
                    commit_results(folder, BRANCH, 'Record Nibi super-fine Nsight profiling results and job outcomes')
                    committed = finished
        except (BlockingIOError, RuntimeError, subprocess.TimeoutExpired) as error:
            print(f'Refresh deferred: {error}', flush=True)
            if not args.watch:
                raise SystemExit(1)
            done = False
        if done or not args.watch:
            break
        time.sleep(60)


if __name__ == '__main__':
    main()
