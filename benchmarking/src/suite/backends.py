"""Local and Slurm launch adapters, independent of models and execution plugins."""
import math
import os
from pathlib import Path
import re
import shlex
import signal
import subprocess


def free_gpu_uuids(command):
    devices = command(['nvidia-smi', '--query-gpu=index,uuid,memory.used', '--format=csv,noheader,nounits'])
    processes = command(['nvidia-smi', '--query-compute-apps=gpu_uuid', '--format=csv,noheader'])
    if devices.returncode or processes.returncode:
        return []
    occupied = set(processes.stdout.strip().splitlines())
    visible = os.environ.get('CUDA_VISIBLE_DEVICES')
    visible = None if visible is None else visible.split(',')
    available = []
    for line in devices.stdout.splitlines():
        fields = [f.strip() for f in line.split(',')]
        if len(fields) != 3:
            continue
        index, uuid, memory = fields
        if visible is not None and not any(v == index or uuid.startswith(v) for v in visible if v and v != '-1'):
            continue
        if uuid not in occupied and float(memory) <= 256:
            available.append(uuid)
    return available


class LocalBackend:
    name = 'local'

    def launch(self, server, config, args):
        return [*server['mpi'], '-n', str(config['ranks']), '--map-by', 'core', '--bind-to', 'core', '--report-bindings', *args]

    def execute_group(self, api, folder, data, group, script, on_start):
        with (script.parent / 'allocation.out').open('w') as log:
            process = subprocess.Popen(['bash', str(script)], stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            for case in group:
                case.update(state='RUNNING', details='Local allocation started; see job.out')
            api.atomic_json(folder / 'suite.json', data)
            try:
                if on_start is not None:
                    on_start()
                status = process.wait(timeout=data['server']['case_timeout_seconds'] * len(group))
                for case in group:
                    if not (folder / case['id'] / 'finished.txt').exists():
                        case.update(state='INTERRUPTED', details=f'Allocation exited {status} without a completion marker')
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                for case in group:
                    if not (folder / case['id'] / 'finished.txt').exists():
                        case.update(state='TIMEOUT', details='Local allocation exceeded configured time limit')
            except BaseException:
                if process.poll() is None:
                    os.killpg(process.pid, signal.SIGTERM)
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait()
                for case in group:
                    case.update(state='INTERRUPTED', details='Controller interrupted; owned process group terminated')
                api.atomic_json(folder / 'suite.json', data)
                raise
        api.refresh(folder, data, query_slurm=False)

    def accounting(self, api, folder, ids):
        return {}

    def allocation_evidence(self, server, config, destination):
        return []

    def finalize(self, api, folder, data):
        return None


class SlurmBackend:
    name = 'slurm'

    def launch(self, server, config, args):
        return ['srun', '--kill-on-bad-exit=1', '--distribution=block:block',
                '--cpu-bind=cores' if config['device'] == 'CPU' else '--cpu-bind=none',
                *(['--gpus-per-task=' + (server['gpu_type'] + ':' if server['gpu_type'] else '') + '1']
                  if config['device'] == 'GPU' and server.get('full_gpu_nodes', False) else []), *args]

    def execute_group(self, api, folder, data, group, script, on_start):
        args = sbatch_command(data['server'], group, script)
        submitted = api.command(args)
        (script.parent / 'submission.txt').write_text(shlex.join(args) + '\n' + submitted.stdout)
        job = job_id(submitted.stdout)
        for case in group:
            case.update(state='SUBMITTED' if not submitted.returncode and job else 'SUBMISSION_FAILED',
                        job_id=job, details=submitted.stdout.strip())
        print(f'{group[0]["series"]}: {group[0]["state"]} {job}', flush=True)

    def accounting(self, api, folder, ids):
        records = {}
        if not ids:
            return records
        result = api.command(['sacct', '-X', '-n', '-P', '-j', ','.join(ids), '--format=JobIDRaw,State%40,ExitCode,Reason%200'])
        (folder / ('accounting.txt' if not result.returncode else 'accounting_error.txt')).write_text(result.stdout)
        if not result.returncode:
            records = {row[0]: (row[1].split()[0].rstrip('+'), f'Exit {row[2]}; {row[3]}')
                       for line in result.stdout.splitlines() if len(row := line.split('|')) >= 4}
        result = api.command(['squeue', '--start', '-h', '-u', os.environ.get('USER', ''), '-o', '%i|%T|%R|%S'])
        (folder / 'queue.txt').write_text(result.stdout)
        if not result.returncode:
            for line in result.stdout.splitlines():
                row = line.split('|')
                if len(row) >= 4 and row[0] in ids:
                    records[row[0]] = row[1], f'{row[2]}; estimated start {row[3]} (scheduler timezone)'
        return records

    def allocation_evidence(self, server, config, destination):
        per_node = server['gpus_per_node' if config['device'] == 'GPU' else 'cpu_cores_per_node']
        nodes = math.ceil(config['ranks'] / per_node)
        hardware = 'hostname; lscpu'
        if config['device'] == 'GPU':
            hardware += '; nvidia-smi --query-gpu=name,uuid,driver_version,memory.total --format=csv; nvidia-smi topo -m'
        info = ['srun', '--ntasks=' + str(nodes), '--ntasks-per-node=1', '--cpus-per-task=1', 'bash', '-c', hardware]
        return [shlex.join(info) + ' > ' + shlex.quote(str(destination.parent / 'compute_hardware.txt')),
                'scontrol show job "$SLURM_JOB_ID" > ' + shlex.quote(str(destination.parent / 'slurm_job.txt'))]

    def finalize(self, api, folder, data):
        return submit_finalizer(api, folder, data)


def job_id(output):
    return next((line.split(';')[0] for line in reversed(output.splitlines())
                 if re.fullmatch(r'\d+(;\S+)?', line.strip())), '')


def backend(server):
    return {'local': LocalBackend, 'slurm': SlurmBackend}[server['backend']]()


def sbatch_command(server, group, script):
    config = group[0]['configuration']
    gpu = config['device'] == 'GPU'
    per_node = server['gpus_per_node' if gpu else 'cpu_cores_per_node']
    nodes = math.ceil(config['ranks'] / per_node)
    # Slurm can distribute a non-multiple rank count evenly without allocating
    # more ranks than requested. Recorded layouts verify the actual mapping.
    tasks_per_node = math.ceil(config['ranks'] / nodes)
    prefix = 'bench_nh_' if config.get('model_type') == 'NonhydrostaticModel' else 'bench_'
    args = ['sbatch', '--parsable', f'--job-name={prefix}{config["series"][:30]}',
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
    if not gpu:
        limit = server.get('cpu_time_overrides', {}).get(str(config['ranks']), limit)
    args.append('--time=' + limit)
    if gpu:
        kind = server['gpu_type'] + ':' if server['gpu_type'] else ''
        full_nodes = server.get('full_gpu_nodes', False)
        memory = '0' if tasks_per_node == per_node or full_nodes else server['gpu_memory']
        assigned = per_node // tasks_per_node if full_nodes and tasks_per_node < per_node else 1
        args += [f'--gpus-per-task={kind}{assigned}', '--mem=' + memory]
        if full_nodes and tasks_per_node < per_node:
            args += ['--exclusive']
    else:
        args.append('--hint=nomultithread')
        if server['cpu_constraint']:
            args.append('--constraint=' + server['cpu_constraint'])
        if server['exclusive_cpu']:
            args += ['--exclusive', '--mem=0']
        else:
            memory = server['cpu_memory_base_gb'] + server['cpu_memory_per_rank_gb'] * tasks_per_node
            args.append(f'--mem={memory}G')
    extra = server['gpu_sbatch_extra' if gpu else 'cpu_sbatch_extra']
    if any(a.startswith('--dependency=afterok:') for a in extra):
        args.append('--kill-on-invalid-dep=yes')
    return args + extra + [str(script)]


def submit_finalizer(api, folder, data):
    ids = sorted({c['job_id'] for c in data['cases'] if c['job_id']})
    if not ids or data.get('finalizer_job_id'):
        return
    server = data['server']
    metadata = folder / 'run_metadata'
    path = metadata / 'finalize.sh'
    lines = ['#!/usr/bin/env bash', *api.environment_lines(server)]
    if server['report_modules']:
        lines.append(shlex.join(['module', 'load', *server['report_modules']]))
    args = [server['python'], str(metadata / 'scripts/benchmark_suite.py')]
    if data.get('workflow_root'):
        args += ['--study', data['workflow_root'], '--refresh']
    else:
        args += ['--output', str(folder.parent), '--series', folder.name, '--refresh']
    if data.get('commit'):
        args.append('--commit')
    if data.get('publish_to'):
        args += ['--publish', data['publish_to']]
    lines.append(shlex.join(args))
    path.write_text('\n'.join(lines) + '\n')
    args = ['sbatch', '--parsable', '--nodes=1', '--ntasks=1', '--cpus-per-task=1',
            '--mem=4G', '--time=00:30:00', '--job-name=benchmark_finalize',
            '--dependency=afterany:' + ':'.join(ids), '--output=' + str(metadata / 'finalize.out')]
    if server['cpu_account']:
        args.append('--account=' + server['cpu_account'])
    args.append(str(path))
    result = api.command(args)
    (metadata / 'finalizer_submission.txt').write_text(shlex.join(args) + '\n' + result.stdout)
    job = next((line.split(';')[0] for line in reversed(result.stdout.splitlines()) if re.fullmatch(r'\d+(;\S+)?', line.strip())), '')
    data['finalizer_job_id'] = job
    if result.returncode or not job:
        print('Finalizer submission failed; run --refresh manually. ' + result.stdout, flush=True)
