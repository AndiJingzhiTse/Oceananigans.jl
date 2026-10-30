"""Independent single-GPU ensembles using the shared simulation worker."""
import copy
import csv
import json
import math
import os
from pathlib import Path
import subprocess

from .storage import atomic_json, runtime_environment


def member_configuration(config, member):
    result = copy.deepcopy(config)
    # Historical ensembles schedule complete simulations; member timestepping
    # stays direct rather than inheriting the outer execution adapter.
    result.pop('execution_adapter', None)
    result.update(execution_mode='baseline', ensemble_execution_mode=config['execution_mode'],
                  ensemble_member=member, initial_condition_seed=config['initial_condition_seed'] + member - 1)
    return result


def physical_cpus(count):
    selected, cores = [], set()
    for cpu in sorted(os.sched_getaffinity(0)):
        topology = Path(f'/sys/devices/system/cpu/cpu{cpu}/topology')
        core = ((topology / 'physical_package_id').read_text(), (topology / 'core_id').read_text())
        if core not in cores:
            cores.add(core)
            selected.append(cpu)
        if len(selected) == count:
            return selected
    raise ValueError('Not enough distinct physical host cores for the GPU ensemble')


def launch_command(server, config, case_dir, metadata):
    if server['backend'] != 'local':
        raise ValueError('GPU ensembles currently support local execution only')
    count = config['ensemble_size']
    result = subprocess.run(['nvidia-smi', '--query-gpu=uuid', '--format=csv,noheader'],
                            check=True, text=True, capture_output=True)
    devices = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    visible = server['environment'].get('CUDA_VISIBLE_DEVICES', os.environ.get('CUDA_VISIBLE_DEVICES'))
    if visible is not None:
        requested = visible.split(',') if visible else []
        devices = [devices[int(v)] if v.isdigit() else next(d for d in devices if d.startswith(v))
                   for v in requested]
    if len(set(devices)) < count:
        raise ValueError(f'Ensemble needs {count} distinct visible GPUs')
    cpus = physical_cpus(count)
    runtime = Path(server['environment']['TMPDIR']).resolve()
    members = []
    for index in range(1, count + 1):
        folder = case_dir / f'member_{index}'
        folder.mkdir(exist_ok=True)
        atomic_json(folder / 'configuration.json', member_configuration(config, index))
        members.append(dict(id=index, directory=str(folder), gpu_uuid=devices[index - 1], cpu=cpus[index - 1],
                            environment=runtime_environment(runtime / f'member_{index}')))
    settings = case_dir / 'ensemble_launch.json'
    atomic_json(settings, dict(directory=str(case_dir), project=server['project'],
                               execution_mode=config['execution_mode'], members=members,
                               worker_file=str(metadata / 'src/suite/worker.jl')))
    return [server['julia'], '--threads=1', '--project=' + server['project'],
            str(metadata / 'src/suite/ensemble_runner.jl'), str(settings)]


def validate_ensemble(folder, config):
    from .report import validate
    folder = Path(folder)
    summary = json.loads((folder / 'ensemble.json').read_text())
    root_entries = json.loads((folder / 'results.json').read_text())
    root_layout = json.loads((folder / 'layout.json').read_text())
    count = config['ensemble_size']
    placement = json.loads((folder / 'ensemble_launch.json').read_text())['members']
    ids = set(range(1, count + 1))
    if (len(root_entries) != count or len(root_layout) != count or
            {e['ensemble_member'] for e in root_entries} != ids or
            {e['ensemble_member'] for e in root_layout} != ids):
        raise ValueError('Incomplete ensemble results or layout')
    completed = summary['completed']
    if (summary['execution_mode'] != config['execution_mode'] or len(completed) != count or
            {c['id'] for c in completed} != ids or len({c['pid'] for c in completed}) != count or
            len({c['worker'] for c in completed}) != count):
        raise ValueError('Ensemble dispatcher or worker placement differs from configuration')
    measurements, layouts, elapsed = [], [], []
    for index in range(1, count + 1):
        child = folder / f'member_{index}'
        child_config = member_configuration(config, index)
        if json.loads((child / 'configuration.json').read_text()) != child_config:
            raise ValueError('Ensemble member configuration mismatch')
        # Every member uses the same validation as the existing single-GPU runs.
        measurements.append(validate(child, child_config, ensemble_member=True))
        entry = json.loads((child / 'results.json').read_text())[0]
        elapsed.append(sum(entry['window_seconds']))
        entry['ensemble_member'] = index
        if entry != next(e for e in root_entries if e['ensemble_member'] == index):
            raise ValueError('Ensemble aggregate differs from original member results')
        layout = json.loads((child / 'layout.json').read_text())[0]
        requested = next(m for m in placement if m['id'] == index)
        # CUDA.uuid prints the UUID alone; nvidia-smi adds a GPU- prefix.
        if (layout['gpu_uuid'].removeprefix('GPU-') != requested['gpu_uuid'].removeprefix('GPU-') or
                layout['affinity'] != str(requested['cpu'])):
            raise ValueError('Ensemble member used a different GPU or host core than assigned')
        layout['ensemble_member'] = index
        if layout != next(e for e in root_layout if e['ensemble_member'] == index):
            raise ValueError('Ensemble aggregate layout differs from member layout')
        layouts.append(layout)
    if len({(l['hostname'], l['gpu_uuid']) for l in layouts}) != count:
        raise ValueError('Ensemble members share a GPU')
    timed, dispatch, setup = (summary[k] for k in ('timed_seconds', 'dispatch_seconds', 'setup_seconds'))
    if (any(not isinstance(t, (float, int)) or not math.isfinite(t) or t <= 0 for t in (timed, dispatch, setup)) or
            dispatch < timed or timed + 1e-5 < max(elapsed)):
        raise ValueError('Invalid ensemble wall times')
    for name in ('ready', 'timing_started', 'timed'):
        events = [e for e in summary['events'] if e[0] == name]
        if len(events) != count or {e[1] for e in events} != ids:
            raise ValueError('Missing ensemble barrier/timing events')
    starts = {e[1]: e[2] for e in summary['events'] if e[0] == 'timing_started'}
    ends = {e[1]: e[2] for e in summary['events'] if e[0] == 'timed'}
    if any(ends[i] <= starts[i] for i in ids) or max(starts.values()) >= min(ends.values()):
        raise ValueError('All four simulations did not overlap')
    return dict(fastest=max(m['fastest'] for m in measurements), median=max(m['median'] for m in measurements),
                maximum=max(m['maximum'] for m in measurements), retained_substeps=[],
                nodes=len({l['hostname'] for l in layouts}),
                ensemble_timed_seconds=timed, ensemble_dispatch_seconds=dispatch, ensemble_setup_seconds=setup,
                ensemble_simulations_per_hour=count * 3600 / timed,
                ensemble_steps_per_second=count * config['samples'] * config['time_steps'] / timed,
                ensemble_member_measurements=measurements)


def ensemble_table(cases):
    lines = ['Each case runs four independent simulations, one GPU and one MPI rank per simulation. '
             'Each has two warmup steps and five windows of ten steps. All four finish warmup before '
             'a common timing gate opens. Timed makespan ends when the slowest simulation finishes its windows. '
             'Dispatch time includes model construction, compilation, warmup and final validation; '
             'worker/package initialization is recorded separately as setup time.', '',
             'Both variants use direct CUDA/MPI timestepping inside each model. The baseline submits four '
             'concurrent Distributed calls; Dagger submits four full-simulation tasks before fetching any. '
             'Simulations/hour = 4 × 3600 / timed makespan; each simulation represents a 50-step timing block. '
             'These are ensemble throughput measurements on a shared server.', '',
             '| Resolution per simulation | GPUs / simulations | Outcome | Timed makespan (s) | Dispatch time (s) | Simulations/hour |',
             '|---|---:|---|---:|---:|---:|']
    for case in cases:
        cfg, m = case['configuration'], case.get('measurement', {}) if case['state'] == 'COMPLETED' else {}
        grid = ' × '.join(map(str, cfg['global_resolution']))
        values = [f'{m[key]:.4f}' if key in m else '—' for key in
                  ('ensemble_timed_seconds', 'ensemble_dispatch_seconds', 'ensemble_simulations_per_hour')]
        lines.append(f"| [{grid}]({case['id']}/configuration.md) | 4 / 4 | {case['state']} | {' | '.join(values)} |")
        if case.get('details') and case['state'] != 'COMPLETED':
            lines += ['', f"{grid}: {case['details']}"]
    return lines


def write_ensemble_report(folder, cases):
    folder = Path(folder)
    (folder / 'plot.md').write_text('# Four independent single-GPU simulations\n\n' + '\n'.join(ensemble_table(cases)) + '\n')
    rows = []
    for c in cases:
        m = c.get('measurement', {}) if c['state'] == 'COMPLETED' else {}
        rows.append(dict(case=c['id'], resolution='x'.join(map(str, c['configuration']['global_resolution'])),
                         simulations=4, gpus=4, state=c['state'],
                         **{k: m.get(k, '') for k in ('ensemble_timed_seconds', 'ensemble_dispatch_seconds',
                                                     'ensemble_setup_seconds', 'ensemble_simulations_per_hour')}))
    if rows:
        with (folder / 'results.csv').open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)


def comparison_lines(rows, output, plotting):
    lines = ['Four independent models run concurrently on four GPUs. Each resolution is per model, '
             'with partition 1 × 1 × 1 and one MPI rank per model. Timed makespan covers all four 50-step '
             'timing blocks after a common post-warmup start gate. Dispatch time also includes construction, '
             'compilation, warmup and validation. Speedup = baseline / Dagger; equal time = 1. '
             'One ensemble batch is measured per variant and resolution.', '',
             '| Resolution per simulation | GPUs | Baseline / Dagger outcome | Timed makespan (s), baseline / Dagger | Timed speedup | Dispatch time (s), baseline / Dagger | Dispatch speedup |',
             '|---|---:|---|---:|---:|---:|---:|']
    paired = [r for r in rows if r['speedup_ensemble_timed'] != '']
    for row in rows:
        values = []
        for stat in ('timed', 'dispatch'):
            ratio = row[f'speedup_ensemble_{stat}']
            values.extend([f"{row[f'baseline_ensemble_{stat}']:.4f} / {row[f'dagger_ensemble_{stat}']:.4f}" if ratio != '' else '—',
                           f'{ratio:.4f}' if ratio != '' else '—'])
        lines.append(f"| {row['resolution'].replace('x', ' × ')} | 4 | {row['baseline_state']} / {row['dagger_state']} | {' | '.join(values)} |")
        if row['speedup_ensemble_timed'] == '':
            lines += ['', row['details']]
    if paired and plotting:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        with matplotlib.rc_context({'svg.fonttype': 'none', 'svg.hashsalt': 'ocean-ensemble'}):
            fig, axes = plt.subplots(1, 2, figsize=(12, 4), constrained_layout=True)
            x = list(range(len(paired)))
            for mode in ('baseline', 'dagger'):
                axes[0].plot(x, [r[f'{mode}_ensemble_timed'] for r in paired], 'o-', label=mode)
            for stat in ('timed', 'dispatch'):
                axes[1].plot(x, [r[f'speedup_ensemble_{stat}'] for r in paired], 'o-', label=stat)
            axes[1].axhline(1, linestyle=':', color='black', label='Equal time (1)')
            axes[0].set_ylabel('Four-model timed makespan (s)')
            axes[1].set_ylabel('Speedup: baseline / Dagger')
            for axis in axes:
                axis.set_xticks(x, [r['resolution'].replace('x', ' × ') for r in paired])
                axis.grid(alpha=0.2)
                axis.legend()
            target = Path(output) / 'comparisons/gpu_ensemble.svg'
            target.parent.mkdir(exist_ok=True)
            fig.savefig(target, metadata={'Date': None})
            plt.close(fig)
        lines += ['', '![Ensemble makespan and speedup](comparisons/gpu_ensemble.svg)', '']
    return lines + ['']
