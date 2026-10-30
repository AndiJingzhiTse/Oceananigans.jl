"""Machine reports and publication of completed series measurements."""
import copy
import csv
import fcntl
import json
from pathlib import Path
import shutil
import tempfile
import tarfile

from .report import efficiencies, scaling_baselines
from .plan import MODEL_FOLDERS

MACHINES = ('Andi-5070ti', 'fir', 'nibi', 'rondeau', 'rorqual')


def write_series_report(folder, cases):
    """Report accepted records using their actual settings, including old formats."""
    from .report import plot_series, plot_kernels
    folder = Path(folder)
    if not cases:
        return
    series = cases[0]['series']
    if series == 'gpu_ensemble':
        from .ensemble import write_ensemble_report
        return write_ensemble_report(folder, cases)
    accepted = [c for c in cases if c['state'] == 'COMPLETED' and 'measurement' in c]
    baselines = scaling_baselines(accepted)
    rows = []
    for case in sorted(accepted, key=lambda c: (c['ranks'], c['id'])):
        cfg, measured = case['configuration'], case['measurement']
        fastest, median = efficiencies(case, baselines.get(series))
        rows.append(dict(case=case['id'], ranks=case['ranks'], state='COMPLETED',
                         fastest=measured['fastest'], median=measured['median'],
                         efficiency_fastest=fastest, efficiency_median=median,
                         resolution='x'.join(map(str, cfg['global_resolution']))))
    lines = [f'# {folder.parent.name}: {series}', '',
             'Latest accepted measurement for each case. Configuration links record '
             'the actual grid, partition, numerical methods, timing protocol and validation limits.', '']
    if rows:
        plot_name = 'gpu_partition_timings' if series == 'gpu_partition_super_fine' and any(
            r['efficiency_fastest'] is None for r in rows) else series
        plot_series(folder, plot_name, rows)
        if plot_name != series:
            (folder / f'{plot_name}.svg').replace(folder / f'{series}.svg')
        lines += [f'![Timing and scaling]({series}.svg)', '']
        with (folder / 'results.csv').open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
    profiles = [c for c in accepted if 'kernel_nanoseconds' in c['measurement']]
    if profiles:
        plot_kernels(folder, series, profiles)
        lines += [f'![Kernel duration shares]({series}_kernels.svg)', '']
    lines += ['| Case | MPI ranks | Fastest s/step | Median s/step | Validation |',
              '|---|---:|---:|---:|---|']
    for case in accepted:
        measured = case['measurement']
        lines.append(f"| [{case['id']}]({case['id']}/configuration.md) | {case['ranks']} | "
                     f"{measured['fastest']:.6f} | {measured['median']:.6f} | "
                     f"{case.get('validation', 'Current suite checks')} |")
    (folder / 'plot.md').write_text('\n'.join(lines) + '\n')


def machine_cases(folder):
    """Load series manifests with case paths relative to their machine."""
    cases = []
    for path in sorted(Path(folder).glob('*/suite.json')):
        for case in json.loads(path.read_text()).get('cases', []):
            case = copy.deepcopy(case)
            case['id'] = path.parent.name + '/' + case['id'].split('/')[-1]
            cases.append(case)
    return cases


def write_machine_report(folder):
    folder = Path(folder)
    cases = machine_cases(folder)
    baselines = scaling_baselines(cases)
    lines = [f'# {folder.name} benchmarks', '',
             'Each series folder contains its configurations, measurements and provenance. '
             'Only completed measurements appear in timing tables and plots.', '',
             '| Series | Completed cases | Report |', '|---|---:|---|']
    series = sorted({c['series'] for c in cases})
    for name in series:
        completed = sum(c['series'] == name and c['state'] == 'COMPLETED' and 'measurement' in c for c in cases)
        lines.append(f'| `{name}` | {completed} | [Details]({name}/plot.md) |')
    if not series:
        lines += ['', 'No validated measurements are available for this machine and model.']
    for name in series:
        lines += ['', f'## {name}', '']
        if name == 'gpu_ensemble':
            from .ensemble import ensemble_table
            lines += ensemble_table([c for c in cases if c['series'] == name])
            continue
        for suffix in ('', '_kernels'):
            image = folder / name / f'{name}{suffix}.svg'
            if image.exists():
                lines += [f'![{name}{suffix}]({name}/{image.name})', '']
        lines += ['| Case | Ranks | Global resolution | Partition | Fastest / median s per step | Median MPI efficiency | Validation |',
                  '|---|---:|---|---|---:|---:|---|']
        selected = sorted((c for c in cases if c['series'] == name), key=lambda c: (c['ranks'], c['id']))
        for case in selected:
            if case['state'] != 'COMPLETED' or 'measurement' not in case:
                continue
            cfg, measurement = case.get('configuration', {}), case['measurement']
            grid = ' × '.join(map(str, cfg.get('global_resolution', []))) or 'See configuration'
            partition = ' × '.join(map(str, case.get('partition') or [])) or 'Not recorded'
            _, eff = efficiencies(case, baselines.get(name))
            efficiency = f'{100 * eff:.1f}%' if eff is not None else '—'
            validation = case.get('validation', 'Current suite checks')
            lines.append(f"| [{case['id'].split('/')[-1]}]({case['id']}/configuration.md) | {case['ranks']} | {grid} | {partition} | "
                         f"{measurement['fastest']:.6f} / {measurement['median']:.6f} | {efficiency} | {validation} |")
        if not any(c['state'] == 'COMPLETED' and 'measurement' in c for c in selected):
            lines += ['', 'No completed, validated measurements in this series.']
    with tempfile.NamedTemporaryFile(mode='w', dir=folder, prefix='.plot-', delete=False) as stream:
        stream.write('\n'.join(lines) + '\n')
        temporary = Path(stream.name)
    temporary.replace(folder / 'plot.md')


def publish_series(source, destination):
    """Publish completed cases, retaining older accepted cases if a rerun fails."""
    source, destination = Path(source), Path(destination)
    data = json.loads((source / 'suite.json').read_text())
    accepted = [c for c in data['cases'] if c['state'] == 'COMPLETED' and 'measurement' in c]
    if not accepted:
        return 0
    family = next((p.name for p in destination.parents if p.name in MODEL_FOLDERS.values()), None)
    expected = MODEL_FOLDERS[data['server'].get('model_type', 'HydrostaticFreeSurfaceModel')]
    if family and family != expected:
        raise ValueError('Publication destination belongs to the other model family')
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / '.suite.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return _publish_accepted(source, destination, data, accepted)


def _publish_accepted(source, destination, data, accepted):
    previous = json.loads((destination / 'suite.json').read_text()) if (destination / 'suite.json').exists() else {}
    if any(c['state'] not in {'COMPLETED'} for c in previous.get('cases', [])):
        raise ValueError('Publish into a curated results directory, not a live study')
    merged = {c['id']: c for c in previous.get('cases', [])}
    count = 0
    for case in accepted:
        entries = json.loads((source / case['id'] / 'results.json').read_text())
        measured_at = max(e.get('metadata', {}).get('timestamp', '') for e in entries)
        if case['id'] in merged and measured_at <= merged[case['id']].get('provenance', {}).get('measured_at', ''):
            continue
        target = destination / case['id']
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source / case['id'], target, ignore=shutil.ignore_patterns('*.sh', '*.sbatch', '*.py', '*.jl', '*.out'))
        case = copy.deepcopy(case)
        case['provenance'] = dict(source=str(source), submitted_at=data.get('submitted_at'), measured_at=measured_at)
        provenance = target / 'provenance'
        provenance.mkdir(exist_ok=True)
        (provenance / 'record.json').write_text(json.dumps(case['provenance'], indent=2) + '\n')
        for name in ('Project.toml', 'Manifest.toml', 'LocalPreferences.toml', 'revision.txt', 'working_tree.txt'):
            path = source / 'run_metadata' / name
            if path.is_file():
                shutil.copy2(path, provenance / name)
        # Capture the immutable executable snapshot as one provenance artifact.
        if (source / 'run_metadata/src').is_dir():
            with tarfile.open(provenance / 'source.tar.gz', 'w:gz') as archive:
                for name in ('src', 'scripts'):
                    archive.add(source / 'run_metadata' / name, arcname=name,
                                filter=lambda info: None if '__pycache__' in info.name else info)
                for path in (source / 'run_metadata').iterdir():
                    if path.is_file() and path.suffix in {'.jl', '.sh'}:
                        archive.add(path, arcname=path.name)
        merged[case['id']] = case
        count += 1
    data.update(cases=list(merged.values()), curated=True)
    temporary = destination / 'suite.json.tmp'
    temporary.write_text(json.dumps(data, indent=2) + '\n')
    temporary.replace(destination / 'suite.json')
    write_series_report(destination, data['cases'])
    return count
