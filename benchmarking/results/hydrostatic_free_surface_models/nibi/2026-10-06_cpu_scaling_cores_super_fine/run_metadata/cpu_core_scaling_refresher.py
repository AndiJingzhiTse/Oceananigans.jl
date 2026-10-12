#!/usr/bin/env python3
"""Replacement Nibi CPU scaling: 3 cores, doubling to full nodes and beyond."""
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

SCRIPT_DIR = Path(__file__).resolve().parent
BRANCH = 'codex/nibi-gpu-strong-scaling'
GRID = (1440, 720, 200)
TERMINAL_STATES = TERMINAL | {'GEOMETRY_LIMIT'}


def run(*args):
    return subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)


def balanced_sizes(n, parts):
    q, r = divmod(n, parts)
    return [q + (i < r) for i in range(parts)]


def partition_for_ranks(ranks):
    options = []
    for rx in range(1, ranks + 1):
        if ranks % rx:
            continue
        ry = ranks // rx
        # The earth_ocean model has seven-cell horizontal halos. Vertical
        # decomposition is unsupported by the split-explicit free surface.
        if GRID[0] // rx >= 7 and GRID[1] // ry >= 7:
            sx, sy = balanced_sizes(GRID[0], rx), balanced_sizes(GRID[1], ry)
            imbalance = max(sx) * max(sy) / (min(sx) * min(sy))
            aspect = abs(math.log((GRID[0] / rx) / (GRID[1] / ry)))
            options.append((imbalance, aspect, rx, ry))
    if not options:
        raise ValueError(f'{ranks} MPI ranks have no horizontal partition with at least seven cells per local dimension')
    _, _, rx, ry = min(options)
    return [rx, ry, 1]


def configuration(cores, layout='mpi'):
    threads = 1 if layout == 'mpi' else min(cores, 192)
    ranks = cores // threads
    nodes = max(1, cores // 192)
    partition = partition_for_ranks(ranks)
    return dict(cores=cores, nodes=nodes, ranks=ranks, ranks_per_node=ranks // nodes,
                threads_per_rank=threads, layout=layout, partition=partition,
                global_resolution=list(GRID), grid_type='LatitudeLongitudeGrid',
                x_sizes=balanced_sizes(GRID[0], partition[0]), y_sizes=balanced_sizes(GRID[1], partition[1]),
                float_type='Float64', samples=5, time_steps=10, warmup_steps=2, dt=60,
                free_surface_substeps=30, extend_free_surface_halos=False,
                momentum_advection='WENOVectorInvariantDefault', tracer_advection='WENO7',
                closure='CATKE', tracers=['T', 'S'], timestepper='SplitRungeKutta3')


def save_jobs(folder, jobs):
    tmp = folder / 'jobs.json.tmp'
    tmp.write_text(json.dumps(jobs, indent=2) + '\n')
    tmp.replace(folder / 'jobs.json')


def parse_job_id(output):
    return next(line.strip().split(';')[0] for line in reversed(output.splitlines())
                if re.fullmatch(r'\d+(;\S+)?', line.strip()))


def write_configuration(case, config):
    case.mkdir(exist_ok=True)
    (case / 'configuration.json').write_text(json.dumps(config, indent=2) + '\n')
    sx, sy = config['x_sizes'], config['y_sizes']
    (case / 'configuration.md').write_text(
        '# Benchmark configuration\n\n'
        f"Global resolution: 1440 × 720 × 200. Grid type: {config['grid_type']}.\n"
        f"Partition: {' × '.join(map(str, config['partition']))}.\n"
        f"{config['cores']} cores; {config['nodes']} nodes; {config['ranks']} MPI ranks; "
        f"{config['threads_per_rank']} pinned Julia threads per rank.\n"
        f"Local resolution: x {min(sx)}–{max(sx)}, y {min(sy)}–{max(sy)}, z 200. "
        'Remainder cells are distributed evenly; the global grid is preserved.\n'
        'Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.\n'
        'Δt=60 s; two warmup steps, five ten-step windows.\n'
        'SplitExplicitFreeSurface(substeps=30, extend_halos=false): exchange halos at every substep.\n')


def submit(folder, layout):
    if (folder / 'jobs.json').exists():
        raise SystemExit('Already submitted; use a new directory for a new series')
    metadata = folder / 'run_metadata'
    metadata.mkdir(exist_ok=True)
    for name in ('Project.toml', 'Manifest.toml', 'LocalPreferences.toml'):
        shutil.copy2(SCRIPT_DIR / 'environment' / name, metadata / name)
    for name in ('cpu_core_scaling.py', 'cpu_core_benchmark.sbatch', 'run_cpu_core_benchmark.jl',
                 'finalize_cpu_cores.sbatch', 'refresh_scaling.py'):
        shutil.copy2(SCRIPT_DIR / name, metadata / name)
    shutil.copy2(SCRIPT_DIR.parents[1] / 'src' / 'earth_ocean.jl', metadata / 'earth_ocean.jl')
    (metadata / 'revision.txt').write_text(run('git', '-C', str(SCRIPT_DIR), 'rev-parse', 'HEAD').stdout)
    snapshot = run('scontrol', 'show', 'partition', 'cpubase_bynode_b1')
    if snapshot.returncode:
        raise RuntimeError(snapshot.stdout)
    (metadata / 'partitions.txt').write_text(snapshot.stdout)
    node_limit = int(re.search(r'TotalNodes=(\d+)', snapshot.stdout).group(1))
    jobs = []
    cores = 3
    while cores <= node_limit * 192:
        case = folder / f'{cores}_cores'
        case.mkdir(exist_ok=True)
        try:
            config = configuration(cores, layout)
        except ValueError as error:
            record = dict(cores=cores, nodes=max(1, cores // 192), job_id='',
                          state='GEOMETRY_LIMIT', details=str(error))
            jobs.append(record)
            (case / 'limit.txt').write_text(str(error) + '\n')
            save_jobs(folder, jobs)
            break
        write_configuration(case, config)
        # Small core counts on a 207M-cell grid need long timed windows.
        hours = max(3, math.ceil(72 / cores))
        time_limit = '1-00:00:00' if hours == 24 else f'{hours:02}:00:00'
        # Nibi selects the partition from time, memory/core and whole-node use.
        # A small-core run needs more memory/core than the base bycore class.
        cmd = ['sbatch', '--parsable', '--account=def-fpoulin_cpu',
               '--constraint=granite', f'--job-name=nibi_cpu_cores_{cores}', f"--nodes={config['nodes']}",
               f"--ntasks={config['ranks']}", f"--ntasks-per-node={config['ranks_per_node']}",
               f"--cpus-per-task={config['threads_per_rank']}", f'--time={time_limit}',
               f'--output={case}/job.out']
        if cores >= 192:
            cmd += ['--exclusive', '--mem=0']
        else:
            cmd += [f"--mem={64 + 4 * config['ranks_per_node']}G"]
        cmd += [str(SCRIPT_DIR / 'cpu_core_benchmark.sbatch'), str(case),
                'x'.join(map(str, config['partition'])), str(SCRIPT_DIR)]
        result = run(*cmd)
        (case / 'submission.txt').write_text('Command: ' + ' '.join(cmd) + '\n' + result.stdout)
        record = dict(cores=cores, nodes=config['nodes'], job_id='',
                      state='SUBMISSION_FAILED' if result.returncode else 'SUBMITTED', details='')
        if not result.returncode:
            record['job_id'] = parse_job_id(result.stdout)
            (case / 'job_id.txt').write_text(record['job_id'] + '\n')
        else:
            record['details'] = result.stdout.strip()
        jobs.append(record)
        save_jobs(folder, jobs)
        print(f"{cores} cores, {config['ranks']} ranks: {record['state']} {record['job_id']}", flush=True)
        if result.returncode:
            break
        cores *= 2
    ids = [j['job_id'] for j in jobs if j['job_id']]
    if ids:
        finalizer = run('sbatch', '--parsable', '--account=def-fpoulin_cpu',
                        '--dependency=afterany:' + ':'.join(ids), f'--output={folder}/finalize.out',
                        str(SCRIPT_DIR / 'finalize_cpu_cores.sbatch'), str(folder), str(SCRIPT_DIR))
        (metadata / 'finalizer_submission.txt').write_text(finalizer.stdout)
        if finalizer.returncode:
            raise RuntimeError('Benchmarks submitted, but finalizer failed: ' + finalizer.stdout)
        (metadata / 'finalizer_job_id.txt').write_text(parse_job_id(finalizer.stdout) + '\n')


def validate(case, config):
    entries = json.loads((case / 'results.json').read_text())
    layout = json.loads((case / 'cpu_layout.json').read_text())
    ranks, threads = config['ranks'], config['threads_per_rank']
    if len(entries) != ranks or {e['rank'] for e in entries} != set(range(ranks)):
        raise ValueError('Missing or duplicate result ranks')
    if len(layout) != ranks or {e['rank'] for e in layout} != set(range(ranks)):
        raise ValueError('Missing or duplicate CPU layout ranks')
    host_cpus, host_ranks = {}, {}
    for rank in layout:
        host = rank['hostname']
        host_cpus.setdefault(host, set())
        host_ranks[host] = host_ranks.get(host, 0) + 1
        affinities = rank['thread_affinities']
        if rank['threads'] != threads or rank['cpus_per_task'] != threads or len(affinities) != threads:
            raise ValueError('Unexpected threads per rank')
        for affinity in affinities:
            if not re.fullmatch(r'\d+', affinity) or int(affinity) in host_cpus[host]:
                raise ValueError('Unpinned threads or overlapping CPU cores on a node')
            host_cpus[host].add(int(affinity))
    if len(host_ranks) != config['nodes'] or any(n != config['ranks_per_node'] for n in host_ranks.values()):
        raise ValueError('Unexpected MPI ranks per node')
    if sum(map(len, host_cpus.values())) != config['cores']:
        raise ValueError('Unexpected total physical core count')
    rx, ry, _ = config['partition']
    total_points = 0
    for entry in entries:
        ix, iy = divmod(entry['rank'], ry)
        expected = [config['x_sizes'][ix], config['y_sizes'][iy], GRID[2]]
        if entry['grid_size'] != expected or entry['configuration'] != config:
            raise ValueError('Unexpected partition, global resolution, grid type, or local grid')
        if entry.get('finite_state') is not True:
            raise ValueError('Nonfinite or unverified model state')
        total_points += math.prod(expected)
        if (entry['metadata']['num_threads'] != threads or entry['float_type'] != 'Float64'
                or entry['samples'] != 5 or entry['time_steps'] != 10 or entry['Δt'] != 60):
            raise ValueError('Unexpected benchmark settings')
        values = [entry[k] for k in ('time_per_step_seconds', 'time_per_step_median_seconds', 'time_per_step_max_seconds')]
        if any(not math.isfinite(v) or v <= 0 for v in values) or values != sorted(values):
            raise ValueError('Invalid timing statistics')
    if total_points != math.prod(GRID):
        raise ValueError('Global grid not preserved')
    return max(e['time_per_step_seconds'] for e in entries), max(e['time_per_step_median_seconds'] for e in entries)


def refresh(folder):
    jobs = json.loads((folder / 'jobs.json').read_text())
    ids = [j['job_id'] for j in jobs if j['job_id']]
    records, queued = {}, {}
    accounting_unavailable = False
    local_outcomes = {}
    for job in jobs:
        case = folder / f"{job['cores']}_cores"
        if (case / 'finished.txt').exists() and (case / 'exit_code.txt').exists():
            local_outcomes[job['job_id']] = 'COMPLETED' if (case / 'exit_code.txt').read_text().strip() == '0' else 'FAILED'
    if ids:
        accounting = run('sacct', '-X', '-n', '-P', '-j', ','.join(ids), '--format=JobIDRaw,State%40,ExitCode,Reason%200')
        if accounting.returncode:
            accounting_unavailable = True
            (folder / 'accounting_error.txt').write_text(accounting.stdout)
            print('Slurm accounting unavailable; using live queue and finished batch markers.', flush=True)
        else:
            (folder / 'accounting.txt').write_text(accounting.stdout)
            records = {r[0]: r for line in accounting.stdout.splitlines() if len(r := line.split('|')) >= 4}
        # Completed jobs disappear from squeue; retain them through sacct and
        # query the live queue only for allocations that are still active.
        active_ids = [j['job_id'] for j in jobs if j['job_id'] and j['job_id'] not in local_outcomes and
                      (records[j['job_id']][1].split()[0].rstrip('+') if j['job_id'] in records else j['state']) not in TERMINAL_STATES]
        queue_output = ''
        if active_ids:
            queue = run('squeue', '--start', '-h', '-j', ','.join(active_ids), '-o', '%i|%T|%R|%S')
            if queue.returncode:
                raise RuntimeError(queue.stdout)
            queue_output = queue.stdout
        (folder / 'queue.txt').write_text(queue_output)
        queued = {r[0]: r for line in queue_output.splitlines() if len(r := line.split('|')) >= 4}
    rows = []
    for job in jobs:
        case = folder / f"{job['cores']}_cores"
        config_path = case / 'configuration.json'
        config = json.loads(config_path.read_text()) if config_path.exists() else None
        record = records.get(job['job_id'])
        if record:
            job['state'] = record[1].split()[0].rstrip('+')
            job['details'] = f'Slurm {job["state"]}, exit {record[2]}; {record[3]}'
        elif accounting_unavailable and job['job_id'] in local_outcomes:
            job['state'] = local_outcomes[job['job_id']]
            job['details'] = 'Finished batch exit marker; Slurm accounting temporarily unavailable'
        q = queued.get(job['job_id'])
        if q:
            if accounting_unavailable:
                job['state'] = q[1]
            job['details'] = f'{q[2]}; estimated start {q[3]} America/Toronto'
        status, details = job['state'], job['details']
        fastest = median = None
        if job['state'] == 'COMPLETED':
            try:
                if record and record[2] != '0:0':
                    raise ValueError('Nonzero Slurm exit code')
                if (case / 'exit_code.txt').read_text().strip() != '0':
                    raise ValueError('Nonzero benchmark exit code')
                fastest, median = validate(case, config)
                details = 'All ranks, unique pinned cores, configuration and timings verified'
            except (ValueError, KeyError, OSError, TypeError) as error:
                status, details = 'INVALID_RESULTS', str(error)
        rows.append(dict(cores=job['cores'], nodes=job['nodes'], ranks=config['ranks'] if config else '',
                         threads_per_rank=config['threads_per_rank'] if config else '',
                         partition='x'.join(map(str, config['partition'])) if config else 'Unavailable',
                         resolution='1440x720x200', grid_type='LatitudeLongitudeGrid', job_id=job['job_id'],
                         state=status, fastest=fastest, median=median, details=details))
    save_jobs(folder, jobs)
    with (folder / 'results.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, rows[0].keys(), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    report(folder, rows)
    print('; '.join(f"{r['cores']} cores: {r['state']}" for r in rows), flush=True)
    return all(j['state'] in TERMINAL_STATES for j in jobs), rows


def report(folder, rows):
    measured = [r for r in rows if r['state'] == 'COMPLETED']
    baseline = next((r for r in measured if r['cores'] == 3), None)
    lines = ['# Replacement CPU core scaling', '',
             'Global resolution: **1440 × 720 × 200**. Grid type: **LatitudeLongitudeGrid** (no bathymetry).',
             'Cores: 3, 6, 12, 24, 48, 96, 192 (one node), 384 (two nodes), 768 (four nodes), 1536 (eight nodes), ….',
             'Each MPI rank uses explicitly pinned Julia threads. Per-run rank/thread/partition configurations appear below.',
             'Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3, Δt=60 s.',
             'Two warmup steps, five windows of ten steps. Free-surface substeps=30 requested; extend_halos=false for every count.',
             'Balanced Sizes partitions distribute remainder cells evenly and preserve the entire global grid.', '',
             f"Highest completed, verified count: **{max((r['cores'] for r in measured), default=0)} cores**.",
             'Accepted or pending requests do not count as completed runs. Failed and timed-out runs are excluded from timing plots.', '']
    if measured:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        plt.rcParams.update({'svg.hashsalt': 'nibi-cpu-cores', 'svg.fonttype': 'none'})
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
        for key, label in (('fastest', 'Fastest window'), ('median', 'Median windows')):
            axes[0].plot([r['cores'] for r in measured], [r[key] for r in measured], 'o-', label=label)
            if baseline:
                axes[1].plot([r['cores'] for r in measured], [100 * baseline[key] * 3 / (r[key] * r['cores']) for r in measured], 'o-', label=label)
        axes[0].set(ylabel='Seconds per step (lower is faster)', yscale='log')
        axes[1].set(ylabel='MPI efficiency relative to three cores (%)')
        if baseline:
            axes[1].axhline(100, color='gray', linestyle='--', linewidth=1)
        else:
            axes[1].text(0.5, 0.5, 'Waiting for three-core baseline', ha='center', transform=axes[1].transAxes)
        for ax in axes:
            ax.set_xscale('log', base=2)
            ax.set_xlabel('Physical CPU cores')
            ax.grid(alpha=0.2)
        axes[0].legend()
        fig.suptitle('Nibi — 1440 × 720 × 200, LatitudeLongitudeGrid')
        fig.tight_layout()
        svg = folder / 'cpu_core_scaling.svg'
        fig.savefig(svg, metadata={'Date': None})
        svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n')
        plt.close(fig)
        lines += ['![CPU timing and MPI efficiency](cpu_core_scaling.svg)', '']
    lines += ['| Cores | Nodes | MPI ranks | Threads/rank | Partition | Resolution | Grid type | Job | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |',
              '|---:|---:|---:|---:|---|---|---|---|---|---:|---:|---|---|']
    for row in rows:
        times = f"{row['fastest']:.6f} | {row['median']:.6f}" if row['fastest'] else '— | —'
        efficiency = '—'
        if baseline and row['fastest']:
            efficiency = ' / '.join(f"{100 * baseline[k] * 3 / (row[k] * row['cores']):.1f}%" for k in ('fastest', 'median'))
        details = row['details'].replace('|', '/').replace('\n', ' ')
        lines.append(f"| {row['cores']} | {row['nodes']} | {row['ranks']} | {row['threads_per_rank']} | {row['partition']} | {row['resolution']} | {row['grid_type']} | {row['job_id']} | {row['state']} | {times} | {efficiency} | {details} |")
    lines += ['', 'A window is ten consecutive steps. Rank minimum/median window elapsed times are divided by ten; the maximum across ranks is reported.',
              'Efficiency = three-core time × 3 ÷ (measured time × measured core count).',
              'Per-run configuration.md/configuration.json record global and local resolutions, grid type and MPI partition. Results retain the actual local grid on every rank.',
              'This replaces the earlier 192-thread-per-rank sweep. The free-surface halo strategy differs; timings from the two series should be interpreted with that difference recorded.']
    (folder / 'plot.md').write_text('\n'.join(lines) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_dir', type=Path)
    parser.add_argument('--submit', action='store_true')
    parser.add_argument('--layout', choices=('mpi', 'threads'), default='mpi')
    parser.add_argument('--watch', action='store_true')
    parser.add_argument('--commit', action='store_true')
    args = parser.parse_args()
    folder = args.run_dir.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    if args.submit:
        submit(folder, args.layout)
    committed = set()
    while True:
        try:
            with (folder / '.controller.lock').open('a') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                done, rows = refresh(folder)
                finished = {(r['cores'], r['state']) for r in rows if r['state'] in TERMINAL_STATES}
                if args.commit and (done or finished - committed):
                    commit_results(folder, BRANCH, 'Record replacement Nibi CPU core scaling results and job outcomes')
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
