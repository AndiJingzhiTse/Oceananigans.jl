#!/usr/bin/env python3
"""Run all seven standard benchmark series locally or submit them to Slurm."""
import argparse
from datetime import datetime, timezone
import fcntl
import json
import math
import os
from pathlib import Path
import re
import shlex
import signal
import shutil
import subprocess
import sys
import time

from suite.plan import SERIES, GRIDS, build_plan, allocation_groups
from suite.report import TERMINAL, validate, write_report

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def command(args, **kwargs):
    return subprocess.run([str(a) for a in args], text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=60, **kwargs)


def atomic_json(path, data):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(data, indent=2) + '\n')
    temporary.replace(path)


def load_server(path=None):
    user = json.loads(Path(path).read_text()) if path else {}
    backend = user.get('backend', 'local')
    assigned_cpus = os.sched_getaffinity(0) if hasattr(os, 'sched_getaffinity') else range(os.cpu_count())
    physical_cores = set()
    for cpu in assigned_cpus:
        topology = Path(f'/sys/devices/system/cpu/cpu{cpu}/topology')
        if topology.exists():
            physical_cores.add(((topology / 'physical_package_id').read_text().strip(),
                                (topology / 'core_id').read_text().strip()))
    cpu_capacity = len(physical_cores) or len(assigned_cpus)
    gpu_info = command(['nvidia-smi', '--query-gpu=uuid', '--format=csv,noheader']) if shutil.which('nvidia-smi') else None
    gpu_capacity = len(gpu_info.stdout.strip().splitlines()) if gpu_info and not gpu_info.returncode else 0
    visible = os.environ.get('CUDA_VISIBLE_DEVICES')
    if visible is not None:
        gpu_capacity = min(gpu_capacity, len([v for v in visible.split(',') if v and v != '-1']))
    if backend == 'slurm' and any(key not in user for key in ('max_cpu_cores', 'max_gpus', 'cpu_cores_per_node', 'gpus_per_node')):
        raise ValueError('Slurm config must state max_cpu_cores, max_gpus, cpu_cores_per_node and gpus_per_node')
    server = dict(backend=backend, project=str(ROOT), julia='julia', mpi=['mpiexec'],
                  max_cpu_cores=cpu_capacity, max_gpus=gpu_capacity,
                  cpu_cores_per_node=cpu_capacity, gpus_per_node=max(1, gpu_capacity),
                  gpu_host_cores=8, cpu_account='', gpu_account='', cpu_partition='', gpu_partition='',
                  gpu_type='', cpu_constraint='', exclusive_cpu=True, environment_script='', mpi_init='',
                  cpu_time='03:00:00', gpu_time='00:45:00', partition_time='03:00:00',
                  gpu_memory='128G', cpu_memory_base_gb=64, cpu_memory_per_rank_gb=4,
                  cpu_sbatch_extra=[], gpu_sbatch_extra=[],
                  trace_root=str(Path(os.environ.get('SCRATCH', str(ROOT / 'results'))) / 'benchmark_traces'),
                  case_timeout_seconds=86400, matplotlib=True, python='python3', report_modules=[])
    unknown = set(user) - set(server)
    if unknown:
        raise ValueError('Unknown server settings: ' + ', '.join(sorted(unknown)))
    server.update(user)
    if server['backend'] not in ('local', 'slurm'):
        raise ValueError('backend must be local or slurm')
    if any(not isinstance(server[k], int) or server[k] < 1 for k in ('max_cpu_cores', 'cpu_cores_per_node', 'gpus_per_node', 'gpu_host_cores')):
        raise ValueError('CPU capacity and per-node resource counts must be positive integers')
    if not isinstance(server['max_gpus'], int) or server['max_gpus'] < 0:
        raise ValueError('max_gpus must be a nonnegative integer')
    for key in ('mpi', 'cpu_sbatch_extra', 'gpu_sbatch_extra', 'report_modules'):
        if not isinstance(server[key], list) or any(not isinstance(a, str) for a in server[key]):
            raise ValueError(f'{key} must be an array of command arguments')
    for key in ('project', 'trace_root', 'environment_script', 'mpi_init'):
        if server[key]:
            server[key] = str(Path(os.path.expandvars(server[key])).expanduser().resolve())
    return server


def snapshot(folder, server):
    metadata = folder / 'run_metadata'
    metadata.mkdir()
    # Executable planner/worker snapshot: queued jobs do not depend on later edits.
    shutil.copy2(ROOT / 'benchmark_suite.py', metadata / 'benchmark_suite.py')
    shutil.copytree(ROOT / 'suite', metadata / 'suite', ignore=shutil.ignore_patterns('__pycache__'))
    for name in ('Project.toml', 'Manifest.toml', 'LocalPreferences.toml'):
        source = Path(server['project']) / name
        if source.exists():
            shutil.copy2(source, metadata / name)
    shutil.copytree(ROOT / 'src', metadata / 'benchmark_source')
    (metadata / 'revision.txt').write_text(command(['git', '-C', REPO, 'rev-parse', 'HEAD']).stdout)
    (metadata / 'working_tree.txt').write_text(command(['git', '-C', REPO, 'status', '--short']).stdout)
    for setting in ('environment_script', 'mpi_init'):
        if server[setting]:
            source = Path(server[setting])
            if not source.is_file():
                raise ValueError(f'{setting} does not exist: {source}')
            shutil.copy2(source, metadata / source.name)
    for tool in ('lscpu', 'nvidia-smi'):
        if shutil.which(tool):
            (metadata / f'{tool}.txt').write_text(command([tool]).stdout)
    return metadata


def config_markdown(config):
    return ('# Benchmark configuration\n\n'
            f"Series: {config['series']}. Device: {config['device']}; MPI ranks: {config['ranks']}; one thread/rank.\n"
            f"Grid: {config['grid_name']}, {' × '.join(map(str, config['global_resolution']))}, {config['grid_type']}.\n"
            f"Partition: {' × '.join(map(str, config['partition']))}.\n"
            f"Local resolution: x {min(config['x_sizes'])}–{max(config['x_sizes'])}, y {min(config['y_sizes'])}–{max(config['y_sizes'])}, z {config['global_resolution'][2]}.\n"
            'Float64; WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.\n'
            f"Δt={config['dt']} s; free-surface substeps={config['free_surface_substeps']} requested; extend_halos={config['extend_free_surface_halos']}.\n"
            f"Two untimed steps, {config['samples']} windows of {config['time_steps']} steps. Profile={config['profile']}.\n")


def prepare(folder, server, selected):
    if (folder / 'suite.json').exists():
        raise ValueError('Suite exists; use --resume or --refresh, or choose a fresh output directory')
    folder.mkdir(parents=True, exist_ok=True)
    cases = build_plan(server, selected)
    for case in cases:
        destination = folder / case['id']
        destination.mkdir(parents=True)
        if 'configuration' in case:
            atomic_json(destination / 'configuration.json', case['configuration'])
            (destination / 'configuration.md').write_text(config_markdown(case['configuration']))
        else:
            (destination / 'limit.md').write_text(f"# Unavailable partition\n\nGlobal grid: 1440 × 720 × 200 LatitudeLongitudeGrid.\nRanks: {case['ranks']}; partition: {case['partition']}.\n{case['details']}\n")
    snapshot(folder, server)
    data = dict(server=server, cases=cases, submitted_at=None)
    atomic_json(folder / 'suite.json', data)
    write_report(folder, cases, plotting=False)
    return data


def launch_command(server, config, case_dir, metadata, trace_root):
    rank_script = metadata / 'suite/rank.sh'
    worker = metadata / 'suite/worker.jl'
    args = ['bash', str(rank_script), str(case_dir), server['project'], str(worker),
            str(trace_root / config['series'] / case_dir.name), server['julia']]
    if server['backend'] == 'slurm':
        return ['srun', '--kill-on-bad-exit=1', '--distribution=block:block',
                '--cpu-bind=cores' if config['device'] == 'CPU' else '--cpu-bind=none', *args]
    return [*server['mpi'], '-n', str(config['ranks']), '--map-by', 'core', '--bind-to', 'core', '--report-bindings', *args]


def environment_lines(server):
    lines = ['set -eo pipefail']
    if server['environment_script']:
        lines.append('source ' + shlex.quote(server['environment_script']))
    lines += ['export JULIA_NUM_THREADS=1 JULIA_NUM_GC_THREADS=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1',
              'export JULIA_PKG_PRECOMPILE_AUTO=0 JULIA_CUDA_MEMORY_POOL=none']
    if server['mpi_init']:
        lines.append('export BENCHMARK_MPI_INIT=' + shlex.quote(server['mpi_init']))
    return lines


def group_script(folder, server, cases):
    first = cases[0]
    destination = folder / first['id'] / 'allocation.sh'
    metadata = folder / 'run_metadata'
    traces = Path(server['trace_root']) / folder.name
    lines = ['#!/usr/bin/env bash', *environment_lines(server), 'failed=0']
    lines += ['if type module >/dev/null 2>&1; then module -t list > ' + shlex.quote(str(destination.parent / 'modules.txt')) + ' 2>&1; fi',
              shlex.join([server['julia'], '--version']) + ' > ' + shlex.quote(str(destination.parent / 'julia_version.txt')),
              'if command -v nsys >/dev/null; then nsys --version > ' + shlex.quote(str(destination.parent / 'nsight_version.txt')) + '; fi']
    if server['backend'] == 'slurm':
        per_node = server['gpus_per_node' if first['configuration']['device'] == 'GPU' else 'cpu_cores_per_node']
        nodes = math.ceil(first['ranks'] / per_node)
        hardware = 'hostname; lscpu'
        if first['configuration']['device'] == 'GPU':
            hardware += '; nvidia-smi --query-gpu=name,uuid,driver_version,memory.total --format=csv; nvidia-smi topo -m'
        info = ['srun', '--ntasks=' + str(nodes), '--ntasks-per-node=1', '--cpus-per-task=1',
                'bash', '-c', hardware]
        lines.append(shlex.join(info) + ' > ' + shlex.quote(str(destination.parent / 'compute_hardware.txt')))
        lines.append('scontrol show job "$SLURM_JOB_ID" > ' + shlex.quote(str(destination.parent / 'slurm_job.txt')))
    for case in cases:
        path = folder / case['id']
        launch = launch_command(server, case['configuration'], path, metadata, traces)
        (path / 'command.txt').write_text(shlex.join(launch) + '\n')
        prefix = shlex.quote(str(path))
        lines += [f'date -u +%FT%TZ > {prefix}/started.txt', 'status=0',
                  shlex.join(launch) + f' > {prefix}/job.out 2>&1 || status=$?',
                  f'printf "%s\\n" "$status" > {prefix}/exit_code.txt',
                  f'date -u +%FT%TZ > {prefix}/finished.txt',
                  'if [[ "$status" != 0 ]]; then failed=1; fi']
    lines += ['exit "$failed"']
    destination.write_text('\n'.join(lines) + '\n')
    return destination


def sbatch_command(server, group, script):
    config = group[0]['configuration']
    gpu = config['device'] == 'GPU'
    per_node = server['gpus_per_node' if gpu else 'cpu_cores_per_node']
    nodes = math.ceil(config['ranks'] / per_node)
    # Slurm can distribute a non-multiple rank count evenly without allocating
    # more ranks than requested. Recorded layouts verify the actual mapping.
    tasks_per_node = math.ceil(config['ranks'] / nodes)
    args = ['sbatch', '--parsable', f'--job-name=bench_{config["series"][:30]}',
            f'--nodes={nodes}', f'--ntasks={config["ranks"]}', f'--ntasks-per-node={tasks_per_node}',
            f'--cpus-per-task={server["gpu_host_cores"] if gpu else 1}',
            f'--output={script.parent}/allocation.out']
    account, partition = server['gpu_account' if gpu else 'cpu_account'], server['gpu_partition' if gpu else 'cpu_partition']
    if account:
        args.append('--account=' + account)
    if partition:
        args.append('--partition=' + partition)
    limit = server['partition_time'] if len(group) > 1 else server['gpu_time' if gpu else 'cpu_time']
    if not gpu and config['ranks'] < 24 and len(group) == 1:
        limit = f'{max(3, min(24, math.ceil(72 / config["ranks"]))):02}:00:00'
    args.append('--time=' + limit)
    if gpu:
        kind = server['gpu_type'] + ':' if server['gpu_type'] else ''
        args += [f'--gpus-per-task={kind}1', '--mem=' + server['gpu_memory']]
    else:
        args.append('--hint=nomultithread')
        if server['cpu_constraint']:
            args.append('--constraint=' + server['cpu_constraint'])
        if server['exclusive_cpu']:
            args += ['--exclusive', '--mem=0']
        else:
            memory = server['cpu_memory_base_gb'] + server['cpu_memory_per_rank_gb'] * tasks_per_node
            args.append(f'--mem={memory}G')
    return args + server['gpu_sbatch_extra' if gpu else 'cpu_sbatch_extra'] + [str(script)]


def execute(folder, data):
    server, cases = data['server'], data['cases']
    for key, group in allocation_groups(cases).items():
        script = group_script(folder, server, group)
        if server['backend'] == 'slurm':
            args = sbatch_command(server, group, script)
            submitted = command(args)
            (script.parent / 'submission.txt').write_text(shlex.join(args) + '\n' + submitted.stdout)
            job = next((line.split(';')[0] for line in reversed(submitted.stdout.splitlines())
                        if re.fullmatch(r'\d+(;\S+)?', line.strip())), '')
            for case in group:
                case.update(state='SUBMITTED' if not submitted.returncode and job else 'SUBMISSION_FAILED',
                            job_id=job, details=submitted.stdout.strip())
            print(f'{key}: {group[0]["state"]} {job}', flush=True)
        else:
            # Local execution occupies the supplied resources synchronously.
            with (script.parent / 'allocation.out').open('w') as log:
                try:
                    process = subprocess.Popen(['bash', str(script)], stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
                    status = process.wait(timeout=server['case_timeout_seconds'] * len(group))
                    for case in group:
                        if not (folder / case['id'] / 'finished.txt').exists():
                            case.update(state='INTERRUPTED', details=f'Allocation exited {status} without a case completion marker; see allocation.out')
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGTERM)
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait()
                    # Kill the whole launcher/rank process group rather than
                    # leaving orphaned MPI processes on allocated resources.
                    for case in group:
                        if not (folder / case['id'] / 'finished.txt').exists():
                            case.update(state='TIMEOUT', details='Local allocation exceeded configured time limit')
            refresh(folder, data, query_slurm=False)
        atomic_json(folder / 'suite.json', data)
    if server['backend'] == 'slurm':
        submit_finalizer(folder, data)
    data['submitted_at'] = datetime.now(timezone.utc).isoformat()
    atomic_json(folder / 'suite.json', data)
    refresh(folder, data)


def submit_finalizer(folder, data):
    ids = sorted({c['job_id'] for c in data['cases'] if c['job_id']})
    if not ids or data.get('finalizer_job_id'):
        return
    server = data['server']
    metadata = folder / 'run_metadata'
    path = metadata / 'finalize.sh'
    lines = ['#!/usr/bin/env bash', *environment_lines(server)]
    if server['report_modules']:
        lines.append(shlex.join(['module', 'load', *server['report_modules']]))
    args = [server['python'], str(metadata / 'benchmark_suite.py'), '--output', str(folder), '--refresh']
    if data.get('commit'):
        args.append('--commit')
    lines.append(shlex.join(args))
    path.write_text('\n'.join(lines) + '\n')
    args = ['sbatch', '--parsable', '--nodes=1', '--ntasks=1', '--cpus-per-task=1',
            '--mem=4G', '--time=00:30:00', '--job-name=benchmark_finalize',
            '--dependency=afterany:' + ':'.join(ids), '--output=' + str(metadata / 'finalize.out')]
    if server['cpu_account']:
        args.append('--account=' + server['cpu_account'])
    args.append(str(path))
    result = command(args)
    (metadata / 'finalizer_submission.txt').write_text(shlex.join(args) + '\n' + result.stdout)
    job = next((line.split(';')[0] for line in reversed(result.stdout.splitlines()) if re.fullmatch(r'\d+(;\S+)?', line.strip())), '')
    data['finalizer_job_id'] = job
    if result.returncode or not job:
        print('Finalizer submission failed; run --refresh manually. ' + result.stdout, flush=True)


def refresh(folder, data, query_slurm=True):
    cases = data['cases']
    records = {}
    ids = sorted({c['job_id'] for c in cases if c['job_id'] and c['state'] not in TERMINAL})
    if query_slurm and data['server']['backend'] == 'slurm' and ids:
        # Do not query purged completed IDs with squeue; sacct is a fallback,
        # while finished/exit markers remain authoritative if accounting fails.
        accounting = command(['sacct', '-X', '-n', '-P', '-j', ','.join(ids), '--format=JobIDRaw,State%40,ExitCode,Reason%200'])
        (folder / ('accounting.txt' if not accounting.returncode else 'accounting_error.txt')).write_text(accounting.stdout)
        if not accounting.returncode:
            records = {row[0]: (row[1].split()[0].rstrip('+'), f'Exit {row[2]}; {row[3]}')
                       for line in accounting.stdout.splitlines() if len(row := line.split('|')) >= 4}
        queue = command(['squeue', '--start', '-h', '-u', os.environ.get('USER', ''), '-o', '%i|%T|%R|%S'])
        (folder / 'queue.txt').write_text(queue.stdout)
        if not queue.returncode:
            for line in queue.stdout.splitlines():
                row = line.split('|')
                if len(row) >= 4 and row[0] in ids:
                    records[row[0]] = (row[1], f'{row[2]}; estimated start {row[3]} (scheduler timezone)')
    for case in cases:
        destination = folder / case['id']
        if case['state'] in {'RESOURCE_LIMIT', 'GEOMETRY_LIMIT'}:
            continue
        # Reuse a successfully validated snapshot. Explicit --revalidate can
        # remove this cache when artifacts have been edited or relocated.
        if case['state'] == 'COMPLETED' and 'measurement' in case:
            continue
        if (destination / 'finished.txt').exists():
            status = (destination / 'exit_code.txt').read_text().strip()
            case.update(state='FAILED', details=f'Execution/export exit {status}; see job.out and rank logs')
            if status == '0':
                try:
                    case['measurement'] = validate(destination, case['configuration'])
                    case.update(state='COMPLETED', details='Rank results, finite fields and resource placement verified')
                except (ValueError, KeyError, OSError, TypeError) as error:
                    case.update(state='INVALID_RESULTS', details=str(error))
        elif case['job_id'] in records:
            state, detail = records[case['job_id']]
            case.update(state='INTERRUPTED' if state == 'COMPLETED' else state, details=detail)
        elif (destination / 'started.txt').exists() and case['state'] not in TERMINAL:
            case.update(state='RUNNING', details='Started; waiting for completion marker')
    atomic_json(folder / 'suite.json', data)
    write_report(folder, cases, plotting=data['server']['matplotlib'])
    return all(c['state'] in TERMINAL for c in cases)


def commit_artifacts(folder):
    repository = command(['git', '-C', folder, 'rev-parse', '--show-toplevel'])
    if repository.returncode:
        raise RuntimeError('--commit requires an output directory inside a Git repository')
    repo = Path(repository.stdout.strip())
    if command(['git', '-C', repo, 'diff', '--cached', '--quiet']).returncode:
        raise RuntimeError('Index contains unrelated changes; refusing automatic commit')
    staged = command(['git', '-C', repo, 'add', '--', str(folder.relative_to(repo))])
    if staged.returncode:
        raise RuntimeError(staged.stdout)
    if command(['git', '-C', repo, 'diff', '--cached', '--quiet']).returncode:
        committed = command(['git', '-C', repo, 'commit', '-m', 'Record validated benchmark suite results and job outcomes'])
        if committed.returncode:
            raise RuntimeError(committed.stdout)
        print(committed.stdout, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, help='Server resource and environment JSON file')
    parser.add_argument('--output', type=Path, help='Fresh dated run directory, or existing directory to resume/refresh')
    parser.add_argument('--series', default=','.join(SERIES), help='Comma-separated subset; default all seven')
    parser.add_argument('--max-cpu-cores', type=int)
    parser.add_argument('--max-gpus', type=int)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--plan', action='store_true', help='Write configurations without executing or submitting')
    mode.add_argument('--run', action='store_true', help='Run locally inside assigned resources')
    mode.add_argument('--submit', action='store_true', help='Submit allocation groups through Slurm')
    mode.add_argument('--refresh', action='store_true', help='Refresh an existing suite and regenerate reports')
    mode.add_argument('--resume', action='store_true', help='Execute remaining PLANNED cases; never resubmit live jobs')
    parser.add_argument('--watch', action='store_true', help='Refresh until all cases finish; useful with --submit')
    parser.add_argument('--commit', action='store_true', help='Commit newly completed outcomes; requires configured Git identity')
    parser.add_argument('--revalidate', action='store_true', help='Validate completed artifacts again when refreshing')
    args = parser.parse_args()
    if (args.refresh or args.resume) and not args.output:
        parser.error('--refresh/--resume requires --output')
    if args.watch and args.plan:
        parser.error('--watch cannot be used with --plan')
    selected = tuple(args.series.split(','))
    if not selected or len(set(selected)) != len(selected) or set(selected) - set(SERIES):
        parser.error('Choose unique series names from: ' + ', '.join(SERIES))
    folder = (args.output or ROOT / 'results' / ('%s_full_suite' % datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%SZ'))).resolve()
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / '.suite.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if args.refresh or args.resume:
            data = json.loads((folder / 'suite.json').read_text())
            if args.revalidate:
                for case in data['cases']:
                    case.pop('measurement', None)
        else:
            server = load_server(args.config)
            for key in ('max_cpu_cores', 'max_gpus'):
                value = getattr(args, key)
                if value is not None:
                    server[key] = value
            if server['max_cpu_cores'] < 1 or server['max_gpus'] < 0:
                parser.error('Invalid resource capacity')
            if args.run:
                server['backend'] = 'local'
            if args.submit:
                if not args.config:
                    parser.error('--submit requires a server config with explicit Slurm resource capacities')
                server['backend'] = 'slurm'
            data = prepare(folder, server, selected)
        print('Suite: ' + str(folder), flush=True)
        for case in data['cases']:
            print(f"{case['id']}: {case['state']} {case['partition'] or ''}", flush=True)
        if args.plan:
            return
        data['commit'] = args.commit
        if args.resume or not args.refresh:
            execute(folder, data)
        committed = set()
        while True:
            done = refresh(folder, data)
            outcomes = {(c['id'], c['state']) for c in data['cases'] if c['state'] in TERMINAL}
            if args.commit and (done or outcomes - committed):
                commit_artifacts(folder)
                committed = outcomes
            if done or not args.watch:
                break
            time.sleep(30)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, BlockingIOError, FileNotFoundError, subprocess.TimeoutExpired) as error:
        raise SystemExit(str(error))
