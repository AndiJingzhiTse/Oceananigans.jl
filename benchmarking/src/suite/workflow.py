"""One persisted model/mode study using the common local or Slurm executor."""
import argparse
import copy
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import time

from .backends import free_gpu_uuids
from .catalog import publish_series, write_machine_report
from .plan import MODEL_FOLDERS, machine_series, allocation_groups
from .publication import annotate_failures, commit_records, profile_manifest
from .report import TERMINAL
from .storage import archive_finished_case, archive_runtime, runtime_environment
from .variants import write_comparison

MODELS = {'hydrostatic': 'HydrostaticFreeSurfaceModel', 'nonhydrostatic': 'NonhydrostaticModel',
          **{m: m for m in MODEL_FOLDERS}}
MODES = ('baseline', 'dagger')


def selections(models=None, modes=None, combinations=None, all_combinations=False):
    if all_combinations and (models or modes):
        raise ValueError('--all cannot be combined with --models or --modes')
    if combinations:
        if models or modes or all_combinations:
            raise ValueError('--combinations cannot be combined with --models, --modes or --all')
        pairs = [tuple(v.split(':')) for v in combinations.split(',')]
        if any(len(p) != 2 or p[0] not in MODELS or p[1] not in MODES for p in pairs):
            raise ValueError('Use model:mode pairs, for example hydrostatic:baseline,nonhydrostatic:dagger')
        result = [(MODELS[m], mode) for m, mode in pairs]
    else:
        selected_models = list(MODEL_FOLDERS) if all_combinations or models == 'both' else [MODELS.get(m, m) for m in (models or 'hydrostatic').split(',')]
        selected_modes = list(MODES) if all_combinations or modes == 'both' else (modes or 'baseline').split(',')
        if any(m not in MODEL_FOLDERS for m in selected_models) or any(m not in MODES for m in selected_modes):
            raise ValueError('Choose hydrostatic/nonhydrostatic/both models and baseline/dagger/both modes')
        result = [(m, mode) for m in selected_models for mode in selected_modes]
    if len(result) != len(set(result)):
        raise ValueError('Choose each model/mode combination only once')
    return result


def checked_storage(path):
    path = Path(path).expanduser().resolve()
    for forbidden in ('/tmp', '/var/tmp', '/local_scratch'):
        if path == Path(forbidden) or Path(forbidden) in path.parents:
            raise ValueError('Use project-controlled storage instead of system temporary or local_scratch directories')
    return path


def source_state(repo):
    result = {}
    for name in ('src', 'benchmarking/src', 'benchmarking/scripts', 'benchmarking/server', 'Project.toml', 'benchmarking/Project.toml'):
        source = repo / name
        paths = sorted(source.rglob('*')) if source.is_dir() else [source]
        value = hashlib.sha256()
        for path in paths:
            if path.is_file() and path.suffix in {'.jl', '.py', '.sh', '.json', '.toml'} and '__pycache__' not in path.parts:
                value.update(path.relative_to(repo).as_posix().encode() + b'\0')
                value.update(path.read_bytes())
        result[name] = value.hexdigest()
    return result


def frozen_state(folder):
    paths = [*folder.glob('*/configuration.json')]
    metadata = folder / 'run_metadata'
    for name in ('src', 'scripts'):
        paths.extend(p for p in (metadata / name).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    paths.extend(p for p in metadata.glob('*') if p.suffix in {'.toml', '.json'})
    value = hashlib.sha256()
    for path in sorted(paths):
        value.update(path.relative_to(folder).as_posix().encode() + b'\0')
        value.update(path.read_bytes())
    return value.hexdigest()


def verify_source(study, suite=None):
    manifest = json.loads((Path(study) / 'study.json').read_text())
    if source_state(Path(manifest['repository'])) != manifest['source_state']:
        raise RuntimeError('Benchmark/library/server source changed since planning; start a new study before executing')
    for folder, expected in manifest.get('frozen_state', {}).items():
        if (suite is None or Path(suite) == Path(folder)) and frozen_state(Path(folder)) != expected:
            raise RuntimeError('A captured worker, adapter or configuration changed after planning')


def check_before_execution(api, root, manifest):
    try:
        verify_source(root)
    except RuntimeError as error:
        manifest.update(state='STOPPED_SOURCE_CHANGE', details=str(error))
        api.atomic_json(root / 'study.json', manifest)
        raise


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--study', type=Path, required=True, help='Persisted study root for every selected model/mode')
    p.add_argument('--config', type=Path)
    p.add_argument('--models', help='hydrostatic, nonhydrostatic, comma-separated values, or both')
    p.add_argument('--modes', help='baseline, dagger, or both')
    p.add_argument('--combinations', help='Explicit comma-separated model:mode pairs')
    p.add_argument('--all', action='store_true', help='Both models and both execution modes')
    p.add_argument('--series', help='Configured series subset')
    p.add_argument('--project', type=Path, help='Shared Julia environment override')
    p.add_argument('--dagger-adapter', type=Path, help='Directory containing adapter.json and adapter.jl')
    p.add_argument('--dagger-options', help='JSON object passed only to the Dagger adapter')
    p.add_argument('--max-gpus', type=int)
    p.add_argument('--max-cpu-cores', type=int)
    p.add_argument('--gpu-only', action='store_true')
    p.add_argument('--publish', type=Path, help='Result root; default benchmarking/results')
    p.add_argument('--reference-root', type=Path, help='Compatible retained model/server/variant records; default result root')
    p.add_argument('--commit', action='store_true')
    p.add_argument('--watch', action='store_true')
    p.add_argument('--poll-seconds', type=float, default=30)
    action = p.add_mutually_exclusive_group()
    action.add_argument('--plan', action='store_true')
    action.add_argument('--execute', action='store_true', help='Use the configured backend without changing the command')
    action.add_argument('--resume', action='store_true', help='Execute remaining saved cases')
    action.add_argument('--refresh', action='store_true', help='Refresh saved status and reports without launching jobs')
    return p


def prepare(api, args, flat_study=False, publish_server=None):
    if not args.config:
        raise ValueError('A new study requires --config')
    pairs = selections(args.models, args.modes, args.combinations, args.all)
    root = checked_storage(args.study)
    if any(root.iterdir()):
        # The workflow lock itself is the only expected file in a fresh root.
        if any(p.name != '.workflow.lock' for p in root.iterdir()):
            raise ValueError('Study directory exists; use --resume/--refresh or a new directory')
    results = checked_storage(args.publish or api.ROOT / 'results')
    manifest = dict(schema_version=1, repository=str(api.REPO), source_state=source_state(api.REPO),
                    created_at=datetime.now(timezone.utc).isoformat(), state='PLANNED', commit=args.commit,
                    selections=[], frozen_state={}, publish_root=str(results),
                    reference_root=str((args.reference_root or results).resolve()))
    for model, mode in pairs:
        server = api.load_server(args.config, model, mode)
        for name in ('TMPDIR', 'TMP', 'TEMP', 'OMPI_MCA_orte_tmpdir_base'):
            if server['environment'].get(name):
                checked_storage(os.path.expandvars(server['environment'][name]))
        if args.project:
            server['project'] = str(args.project.expanduser().resolve())
        if mode == 'dagger':
            if args.dagger_adapter:
                server['dagger_adapter'] = str(args.dagger_adapter.expanduser().resolve())
            if args.dagger_options:
                server['dagger_options'] = json.loads(args.dagger_options)
        for key in ('max_gpus', 'max_cpu_cores'):
            if getattr(args, key) is not None:
                server[key] = getattr(args, key)
        if server['max_gpus'] < 0 or server['max_cpu_cores'] < 1:
            raise ValueError('Invalid resource limits')
        selected = tuple(args.series.split(',')) if args.series else machine_series(server)
        if not selected or len(set(selected)) != len(selected) or set(selected) - set(machine_series(server)):
            raise ValueError('Choose unique series configured for this server')
        if args.gpu_only and any(not s.startswith('gpu_') for s in selected):
            raise ValueError('--gpu-only cannot include CPU series')
        machine = server['machine']
        model_root = root if flat_study else root / MODEL_FOLDERS[model] / machine
        destination = checked_storage(publish_server) if publish_server else results / MODEL_FOLDERS[model] / machine
        if destination == model_root or model_root in destination.parents or destination in root.parents:
            raise ValueError('Live study and curated result directories must be separate')
        server['workflow_root'] = str(root)
        server['trace_root'] = str(destination / mode)
        server['profile_layout'] = 'series'
        server['trace_namespace'] = hashlib.sha256(str(root).encode()).hexdigest()[:16]
        entry = dict(model=model, mode=mode, machine=machine, backend=server['backend'],
                     folder=str(model_root / mode), destination=str(destination), series=list(selected), cases=0)
        for series in selected:
            folder = model_root / mode / series
            folder.mkdir(parents=True, exist_ok=True)
            data = api.prepare(folder, copy.deepcopy(server), (series,))
            data['workflow_root'] = str(root)
            requests = []
            for group in allocation_groups(data['cases'], server.get('separate_partitions', False)).values():
                script = api.group_script(folder, data['server'], group)
                config = group[0]['configuration']
                requests.append(dict(cases=[c['id'] for c in group], ranks=config['ranks'],
                                     active_gpus=config['ranks'] if config['device'] == 'GPU' else 0,
                                     submission=api.sbatch_command(server, group, script) if server['backend'] == 'slurm' else ['bash', str(script)]))
            data['resource_requests'] = requests
            manifest['frozen_state'][str(folder)] = frozen_state(folder)
            api.atomic_json(folder / 'suite.json', data)
            entry['cases'] += len(data['cases'])
        manifest['selections'].append(entry)
    api.atomic_json(root / 'study.json', manifest)
    return manifest


def load_studies(manifest):
    return [(entry, Path(entry['folder']) / series,
             json.loads((Path(entry['folder']) / series / 'suite.json').read_text()))
            for entry in manifest['selections'] for series in entry['series']]


def update(api, root, manifest, studies, publish=False):
    counts = {}
    for entry, folder, data in studies:
        api.refresh(folder, data)
        annotate_failures(folder, data, api.atomic_json)
        for case in data['cases']:
            counts[case['state']] = counts.get(case['state'], 0) + 1
            if publish:
                allocation_closed = data['server']['backend'] == 'slurm' and case['state'] in TERMINAL and bool(case['job_id'])
                closed = allocation_closed or (folder / case['id'] / 'finished.txt').exists()
                if data['server']['backend'] == 'slurm' and case['state'] in TERMINAL and closed:
                    archive_runtime(folder / '.runtime' / case['id'], Path(entry['destination']) / entry['mode'] /
                                    folder.name / 'run_records' / case['id'] / 'runtime')
                archive_finished_case(folder, case, Path(entry['destination']) / entry['mode'], allocation_closed)
        if publish:
            target = Path(entry['destination']) / entry['mode']
            target.mkdir(parents=True, exist_ok=True)
            publish_series(folder, target / folder.name)
            profile_manifest(target / folder.name, api.atomic_json)
    for entry in manifest['selections']:
        write_machine_report(Path(entry['folder']))
        if publish:
            write_machine_report(Path(entry['destination']) / entry['mode'])
    groups = {(e['model'], e['machine'], str(Path(e['folder']).parent), e['destination']) for e in manifest['selections']}
    for model, machine, model_root, destination in groups:
        selected = tuple(dict.fromkeys(s for e in manifest['selections'] if e['model'] == model for s in e['series']))
        reference = Path(manifest['reference_root']) / MODEL_FOLDERS[model] / machine
        write_comparison(model_root, model_root, selected=selected, model_type=model, machine=machine,
                         references=reference, plotting=False)
        if publish:
            write_comparison(model_root, destination, selected=selected, model_type=model, machine=machine,
                             references=reference)
            if manifest.get('commit'):
                commit_records(Path(destination), Path(manifest['repository']))
    manifest['outcomes'] = counts
    manifest['updated_at'] = datetime.now(timezone.utc).isoformat()
    api.atomic_json(root / 'study.json', manifest)
    return all(c['state'] in TERMINAL for _, _, d in studies for c in d['cases'])


def local_pending(studies):
    groups = {}
    for entry, folder, data in studies:
        for index, case in enumerate(data['cases']):
            key = entry['model'], case['series'], case['id']
            if case['state'] == 'PLANNED':
                groups.setdefault(key, []).append((entry, folder, data, case, index))
    return sorted(groups.items(), key=lambda item: (item[1][0][3]['ranks'], item[0]))


def execute_local(api, root, manifest, studies, interval):
    allocations = manifest.setdefault('allocations', {})
    while pending := local_pending(studies):
        check_before_execution(api, root, manifest)
        available = free_gpu_uuids(api.command) if any(v[0][3]['configuration']['device'] == 'GPU' for _, v in pending) else []
        chosen = None
        for key, group in pending:
            case = group[0][3]
            token = '/'.join(key)
            gpu = case['configuration']['device'] == 'GPU'
            devices = allocations.get(token, available[:case['ranks']]) if gpu else []
            if not gpu or (len(devices) == case['ranks'] and set(devices) <= set(available)):
                chosen = key, group, devices
                break
        if chosen is None:
            manifest.update(state='WAITING_FOR_GPUS', free_gpu_uuids=available, pending_pairs=len(pending))
            api.atomic_json(root / 'study.json', manifest)
            print(f'Waiting for idle GPUs: {len(pending)} cases/pairs pending; {len(available)} GPUs available', flush=True)
            time.sleep(interval)
            continue
        key, group, devices = chosen
        allocations['/'.join(key)] = devices
        group.sort(key=lambda item: (item[0]['mode'] == 'dagger') != (item[4] % 2 == 1))
        # Recheck availability before each member; do not hold devices while waiting.
        entry, folder, data, case, _ = group[0]
        runtime = folder / '.runtime' / case['id']
        data['server']['environment'].update(runtime_environment(runtime))
        if devices:
            data['server']['environment']['CUDA_VISIBLE_DEVICES'] = ','.join(devices)
        manifest.update(state='RUNNING', active=dict(model=entry['model'], mode=entry['mode'], series=folder.name,
                                                    case=case['id'], gpu_uuids=devices))
        api.atomic_json(root / 'study.json', manifest)
        api.execute(folder, data, case_ids={case['id']})
        if case['state'] != 'RUNNING':
            archive_runtime(runtime, Path(entry['destination']) / entry['mode'] / folder.name / 'run_records' / case['id'] / 'runtime')
        update(api, root, manifest, studies, publish=True)


def main(api, argv=None, flat_study=False, publish_server=None):
    args = parser().parse_args(argv)
    if args.poll_seconds <= 0 or args.poll_seconds > 60 or args.plan and args.watch:
        raise ValueError('Use a poll interval between 0 and 60 seconds; --plan cannot --watch')
    root = checked_storage(args.study)
    root.mkdir(parents=True, exist_ok=True)
    with (root / '.workflow.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            if args.refresh:
                print('An active workflow controller owns reporting; refresh deferred.', flush=True)
                return
            raise
        if args.resume or args.refresh:
            if any((args.config, args.models, args.modes, args.combinations, args.all, args.series,
                    args.project, args.dagger_adapter, args.dagger_options, args.publish, args.reference_root,
                    args.max_gpus is not None, args.max_cpu_cores is not None)):
                raise ValueError('Resume/refresh uses saved selections and settings; do not override them')
            manifest = json.loads((root / 'study.json').read_text())
            if manifest.get('schema_version') != 1 or not manifest.get('selections'):
                raise ValueError('Not a shared-workflow study; use the captured controller for historical studies')
            if args.commit:
                manifest['commit'] = True
        else:
            manifest = prepare(api, args, flat_study, publish_server)
        studies = load_studies(manifest)
        for entry in manifest['selections']:
            print(f"{entry['machine']} ({entry['backend']}): {entry['model']} / {entry['mode']}: {entry['cases']} cases -> {entry['destination']}/{entry['mode']}", flush=True)
        done = update(api, root, manifest, studies, publish=args.refresh or args.resume)
        if args.plan or not (args.execute or args.resume or args.refresh):
            return
        if args.execute or args.resume:
            check_before_execution(api, root, manifest)
            if any(c['state'] == 'RUNNING' for _, _, d in studies for c in d['cases'] if d['server']['backend'] == 'local'):
                raise RuntimeError('An unfinished local case exists; inspect its processes before resuming')
            local = [(e, f, d) for e, f, d in studies if d['server']['backend'] == 'local']
            execute_local(api, root, manifest, local, args.poll_seconds)
            for _, folder, data in studies:
                if data['server']['backend'] == 'slurm':
                    api.execute(folder, data)
            done = update(api, root, manifest, studies, publish=True)
        while args.watch and not done:
            time.sleep(args.poll_seconds)
            # Scheduler finalizers or accounting may have completed meanwhile.
            studies = load_studies(manifest)
            done = update(api, root, manifest, studies, publish=True)
        manifest['state'] = ('COMPLETED' if done else 'SUBMITTED'
                             if any(c['job_id'] for _, _, d in studies for c in d['cases']) else 'PLANNED')
        manifest.pop('active', None)
        api.atomic_json(root / 'study.json', manifest)
