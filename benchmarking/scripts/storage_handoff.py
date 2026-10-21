#!/usr/bin/env python3
"""Let an active allocation finish, clean its old MPI temporary files, and resume."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from suite.storage import atomic_json, archive_runtime


def process_identity(pid):
    try:
        fields = Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()
        return fields[19], fields[0]
    except FileNotFoundError:
        return None


def active_group(group):
    for path in Path('/proc').iterdir():
        if not path.name.isdigit():
            continue
        try:
            fields = (path / 'stat').read_text().rsplit(')', 1)[1].split()
            if int(fields[2]) == group and fields[0] != 'Z':
                return True
        except (FileNotFoundError, PermissionError, ProcessLookupError):
            pass
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--results', type=Path, required=True)
    parser.add_argument('--old-controller', type=int, required=True)
    parser.add_argument('--allocation', type=int, required=True)
    parser.add_argument('--mpi', type=int, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    running = []
    for mode in ('baseline', 'dagger'):
        for suite in (args.study / mode).glob('*/suite.json'):
            data = json.loads(suite.read_text())
            running.extend((mode, suite, data, case) for case in data['cases'] if case['state'] == 'RUNNING')
    if len(running) != 1:
        raise RuntimeError('Expected exactly one active allocation to hand over')
    mode, suite, data, case = running[0]
    controller = process_identity(args.old_controller)
    allocation = process_identity(args.allocation)
    if not controller or not allocation or os.getpgid(args.allocation) != args.allocation:
        raise RuntimeError('Controller or allocation identity changed')
    command = Path(f'/proc/{args.old_controller}/cmdline').read_bytes()
    if b'compare_dagger.py' not in command:
        raise RuntimeError('Unexpected controller process')
    os.kill(args.old_controller, signal.SIGSTOP)
    record = args.results / 'storage_migration.json'
    status = json.loads(record.read_text()) if record.exists() else {}
    status.update(cpu_cleanup='Waiting for active allocation to finish', active_case=str(suite.parent / case['id']),
                  allocation_pid=args.allocation, previous_controller=args.old_controller, watcher_pid=os.getpid())
    atomic_json(record, status)
    started = datetime.fromisoformat((suite.parent / case['id'] / 'started.txt').read_text().strip().replace('Z', '+00:00'))
    deadline = started.timestamp() + data['server']['case_timeout_seconds']
    print(f'Waiting for allocation {args.allocation}; current model processes remain running.', flush=True)
    timed_out = False
    while active_group(args.allocation):
        identity = process_identity(args.allocation)
        if identity and identity[0] != allocation[0]:
            raise RuntimeError('Allocation PID was reused')
        if time.time() >= deadline:
            os.killpg(args.allocation, signal.SIGTERM)
            time.sleep(5)
            if active_group(args.allocation):
                os.killpg(args.allocation, signal.SIGKILL)
            timed_out = True
        time.sleep(10)
    identity = process_identity(args.old_controller)
    if identity and identity[0] == controller[0]:
        # Only the stopped controller is replaced. Its completed child job has
        # already exited; OS closure releases the old study lock.
        os.kill(args.old_controller, signal.SIGKILL)
        for _ in range(50):
            identity = process_identity(args.old_controller)
            if identity is None or identity[1] == 'Z':
                break
            time.sleep(0.1)
        else:
            raise RuntimeError('Old controller has not released its process resources')
    if timed_out:
        case.update(state='TIMEOUT', details='Local allocation exceeded configured time limit during storage handoff')
        atomic_json(suite, data)
    old_tmp = Path('/tmp/ompi.rondeau.8193') / f'pid.{args.mpi}'
    archive = args.results / mode / case['series'] / 'run_records' / case['id'] / 'mpi_runtime_from_tmp'
    if old_tmp.exists():
        archive_runtime(old_tmp, archive)
        cleanup = f'Verified, archived and removed {old_tmp}'
    else:
        cleanup = f'MPI already removed {old_tmp} on exit'
    status = json.loads(record.read_text())
    status.update(cpu_cleanup=cleanup, cleanup_at=datetime.now(timezone.utc).isoformat())
    # The ready marker is created after code checks and the profile relocation.
    while not (args.study / 'storage_handoff.ready').exists():
        time.sleep(10)
    saved = json.loads((args.results / 'study.json').read_text())
    with (args.study / 'controller.log').open('a') as log:
        log.write('\nResuming controller after storage relocation.\n')
        log.flush()
        process = subprocess.Popen(saved['command'], cwd=root, stdin=subprocess.DEVNULL,
                                   stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    saved['controller_pid'] = process.pid
    saved['controller_revision_after_storage_fix'] = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    atomic_json(args.results / 'study.json', saved)
    (args.study / 'controller.pid').write_text(str(process.pid) + '\n')
    status['resumed_controller'] = process.pid
    atomic_json(record, status)
    print(f'{cleanup}; resumed controller {process.pid}.', flush=True)


if __name__ == '__main__':
    main()
