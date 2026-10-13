"""Validate rank artifacts and generate comparable suite reports."""
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics
from .plan import GRIDS

TERMINAL = {'COMPLETED', 'FAILED', 'CANCELLED', 'TIMEOUT', 'OUT_OF_MEMORY', 'NODE_FAIL',
            'PREEMPTED', 'BOOT_FAIL', 'DEADLINE', 'REVOKED', 'INVALID_RESULTS',
            'SUBMISSION_FAILED', 'RESOURCE_LIMIT', 'GEOMETRY_LIMIT', 'MEMORY_ESTIMATE_LIMIT', 'INTERRUPTED'}
CATEGORIES = ('Gc', 'Gu', 'Gv', 'Others')


def validate(case_dir, config):
    entries = json.loads((case_dir / 'results.json').read_text())
    ranks = config['ranks']
    if len(entries) != ranks or {e['rank'] for e in entries} != set(range(ranks)):
        raise ValueError('Missing or duplicate rank results')
    layout = json.loads((case_dir / 'layout.json').read_text())
    gpu = config['device'] == 'GPU'
    if len(layout) != ranks or {l['rank'] for l in layout} != set(range(ranks)):
        raise ValueError('Incomplete resource layout')
    identifiers = [(l['hostname'], l['gpu_uuid'] if gpu else l['physical_core']) for l in layout]
    if len(set(identifiers)) != ranks or any(l['threads'] != 1 for l in layout):
        raise ValueError('Shared computation resources or unexpected thread count')
    if gpu and any(not l['gpu_uuid'] for l in layout):
        raise ValueError('Missing GPU UUID')
    if not gpu and any(not str(l['affinity']).isdigit() or not l['physical_core'] for l in layout):
        raise ValueError('CPU rank is not pinned to one core')
    for entry in entries:
        # Oceananigans rank ordering is z fastest, then y, then x.
        rank = entry['rank']
        py = config['partition'][1]
        expected = [config['x_sizes'][rank // py], config['y_sizes'][rank % py], config['global_resolution'][2]]
        if (entry['configuration'] != config or entry['grid_size'] != expected or
                entry['float_type'] != 'Float64' or entry['finite_state'] is not True or
                entry['metadata']['num_threads'] != 1 or entry['retained_free_surface_substeps'] <= 0):
            raise ValueError('Unexpected model, resolution, thread count or nonfinite fields')
        windows = entry['window_seconds']
        if len(windows) != config['samples'] or any(not math.isfinite(w) or w <= 0 for w in windows):
            raise ValueError('Invalid or incomplete timing windows')
        statistics_expected = (min(windows), statistics.median(windows), max(windows))
        for key, elapsed in zip(('time_per_step_seconds', 'time_per_step_median_seconds', 'time_per_step_max_seconds'), statistics_expected):
            if not math.isclose(entry[key], elapsed / config['time_steps'], rel_tol=1e-10):
                raise ValueError('Timing aggregate differs from actual windows')
    result = dict(fastest=max(e['time_per_step_seconds'] for e in entries),
                  median=max(e['time_per_step_median_seconds'] for e in entries),
                  maximum=max(e['time_per_step_max_seconds'] for e in entries),
                  retained_substeps=sorted({e['retained_free_surface_substeps'] for e in entries}))
    result['nodes'] = len({l['hostname'] for l in layout})
    memories = [e.get('gpu_memory_used_bytes') for e in entries]
    if gpu and all(m is not None for m in memories):
        if any(not isinstance(m, int) or m <= 0 for m in memories):
            raise ValueError('Invalid GPU device memory measurement')
        result['gpu_memory_max_gib'] = max(memories) / 2**30
    if config['profile']:
        totals = dict.fromkeys(CATEGORIES, 0)
        traces = []
        for rank in range(ranks):
            folder = case_dir / f'rank_{rank}'
            if (folder / 'exit_code.txt').read_text().strip() != '0':
                raise ValueError('Profile export failed')
            trace = Path((folder / 'trace_path.txt').read_text().strip())
            size = int((folder / 'trace_bytes.txt').read_text())
            checksum = (folder / 'trace_sha256.txt').read_text().split()[0]
            if size <= 0 or trace.stat().st_size != size:
                raise ValueError('Raw trace missing or changed')
            # Hash once per completed case; refresh reuses its validation marker.
            digest = hashlib.sha256()
            with trace.open('rb') as stream:
                for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
                    digest.update(block)
            if digest.hexdigest() != checksum:
                raise ValueError('Raw trace checksum mismatch')
            with (folder / 'summary_cuda_gpu_kern_sum.csv').open() as stream:
                kernels = list(csv.DictReader(stream))
            if not kernels:
                raise ValueError('Empty kernel profile')
            rank_total = 0
            for row in kernels:
                duration = int(row['Total Time (ns)'].replace(',', ''))
                if duration < 0 or int(row['Instances'].replace(',', '')) <= 0:
                    raise ValueError('Invalid kernel profile')
                category = next((c for c in CATEGORIES[:-1] if f'compute_hydrostatic_free_surface_{c}' in row['Name']), 'Others')
                totals[category] += duration
                rank_total += duration
            if rank_total <= 0:
                raise ValueError('No captured kernels')
            traces.append(dict(rank=rank, path=str(trace), bytes=size, sha256=checksum))
        with (case_dir / 'raw_traces.csv').open('w', newline='') as stream:
            writer = csv.DictWriter(stream, traces[0].keys(), lineterminator='\n')
            writer.writeheader()
            writer.writerows(traces)
        result['kernel_nanoseconds'] = totals
    return result


def write_report(folder, cases, plotting=True, server=None):
    successful = [c for c in cases if c['state'] == 'COMPLETED' and 'measurement' in c]
    baselines = {}
    for case in sorted(successful, key=lambda c: c['ranks']):
        if 'scaling' in case['series']:
            if case['series'] == 'gpu_weak_scaling_super_fine' and case['ranks'] != 1:
                continue
            baselines.setdefault(case['series'], case)
    rows = []
    for case in cases:
        cfg, measurement = case.get('configuration', {}), case.get('measurement', {})
        baseline = baselines.get(case['series'])
        row = dict(series=case['series'], case=case['id'].split('/')[-1], ranks=case['ranks'],
                   partition='x'.join(map(str, case.get('partition') or [])),
                   resolution='x'.join(map(str, cfg.get('global_resolution', GRIDS.get(case['grid_name'], [1440, 720, 200])))),
                   grid_type='LatitudeLongitudeGrid', state=case['state'], job_id=case['job_id'],
                   fastest=measurement.get('fastest'), median=measurement.get('median'),
                   efficiency_fastest=None, efficiency_median=None, details=case['details'],
                   nodes=measurement.get('nodes', math.ceil(case['ranks'] / (server or {}).get('gpus_per_node', 8)) if cfg.get('device') == 'GPU' else None),
                   dt=cfg.get('dt'), window_steps=cfg.get('time_steps'),
                   throughput_cells_per_second=math.prod(cfg['global_resolution']) / measurement['median'] if measurement else None,
                   gpu_memory_max_gib=measurement.get('gpu_memory_max_gib'))
        if baseline and measurement:
            weak = case['series'] == 'gpu_weak_scaling_super_fine'
            factor = 1 if weak else baseline['ranks'] / case['ranks']
            if weak and math.prod(cfg['global_resolution']) / case['ranks'] != math.prod(baseline['configuration']['global_resolution']):
                raise ValueError('Weak-scaling work per GPU changed')
            row['efficiency_fastest'] = baseline['measurement']['fastest'] / measurement['fastest'] * factor
            row['efficiency_median'] = baseline['measurement']['median'] / measurement['median'] * factor
        rows.append(row)
    with (folder / 'results.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, rows[0].keys(), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    lines = ['# Full benchmark suite', '',
             'LatitudeLongitudeGrid without bathymetry; Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.',
             '30 requested free-surface substeps; two untimed steps, five windows. Window lengths and Δt are recorded per case: scaling studies following DRAC use 100 steps; other cases use ten.',
             'One MPI rank per CPU core or GPU, one Julia computation thread per rank. CPU extended halos=false; GPU=true.',
             'Window boundaries synchronize MPI ranks and GPUs. Fastest/median statistics use the maximum across ranks.',
             'Strong efficiency uses the smallest validated GPU/rank count in each series, identified below. Weak efficiency uses one GPU: T₁/Tₙ, with constant interior cells/GPU; missing weak baselines have no efficiency estimate.',
             'Profiled timings are separate; Nsight captures CUDA/NVTX/MPI after warmup. Kernel shares sum durations across ranks, not elapsed wall time.', '']
    for series in dict.fromkeys(c['series'] for c in cases):
        series_rows = [r for r in rows if r['series'] == series]
        completed = [r for r in series_rows if r['state'] == 'COMPLETED']
        lines += [f'## {series}', '', f"Highest completed count: **{max((r['ranks'] for r in completed), default=0)} ranks**.", '']
        if series in baselines:
            lines += [f"Efficiency baseline: **{baselines[series]['ranks']} ranks** ({baselines[series]['id']}).", '']
        if plotting and completed:
            plot_series(folder, series, series_rows)
            lines += [f'![{series}]({series}.svg)', '']
        lines += ['| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Δt (s) / steps per window | Details |',
                  '|---|---:|---|---|---|---|---:|---:|---|---|---|']
        for row in series_rows:
            fast = f"{row['fastest']:.6f}" if row['fastest'] is not None else '—'
            med = f"{row['median']:.6f}" if row['median'] is not None else '—'
            efficiency = f"{100*row['efficiency_fastest']:.1f}% / {100*row['efficiency_median']:.1f}%" if row['efficiency_fastest'] is not None else '—'
            detail = row['details'].replace('|', '/').replace('\n', ' ')
            lines.append(f"| {row['case']} | {row['ranks']} | {row['partition']} | {row['resolution']} | {row['grid_type']} | {row['state']} | {fast} | {med} | {efficiency} | {row['dt']} / {row['window_steps']} | {detail} |")
        profiles = [c for c in successful if c['series'] == series and 'kernel_nanoseconds' in c['measurement']]
        if profiles:
            if plotting:
                plot_kernels(folder, series, profiles)
                lines += ['', f'![Kernel duration shares]({series}_kernels.svg)']
            lines += ['', '| Profile | Gc | Gu | Gv | Others |', '|---|---:|---:|---:|---:|']
            for profile in profiles:
                totals = profile['measurement']['kernel_nanoseconds']
                shares = ' | '.join(f'{100*totals[k]/sum(totals.values()):.2f}%' for k in CATEGORIES)
                lines.append(f"| {profile['id'].split('/')[-1]} | {shares} |")
        for case in (c for c in successful if c['series'] == series):
            cfg = case['configuration']
            local = f"{min(cfg['x_sizes'])}–{max(cfg['x_sizes'])} × {min(cfg['y_sizes'])}–{max(cfg['y_sizes'])} × {cfg['global_resolution'][2]}"
            lines += ['', f"[{case['id'].split('/')[-1]} configuration]({case['id']}/configuration.md): local resolution **{local}**, retained free-surface substeps {case['measurement']['retained_substeps']}."]
    (folder / 'plot.md').write_text('\n'.join(lines) + '\n')
    write_scaling_table(folder, rows, baselines)


def plot_series(folder, series, rows):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'svg.hashsalt': 'benchmark-suite', 'svg.fonttype': 'none'})
    rows = [r for r in rows if r['state'] == 'COMPLETED']
    scaling = 'scaling' in series
    fig, axes = plt.subplots(1, 2 if scaling else 1, figsize=(11 if scaling else 8, 4.5), squeeze=False)
    ax = axes[0, 0]
    x = [r['ranks'] for r in rows] if scaling else list(range(len(rows)))
    ax.plot(x, [r['fastest'] for r in rows], 'o-', label='Fastest')
    ax.plot(x, [r['median'] for r in rows], 's--', label='Median')
    ax.set(ylabel='Seconds per step', title=series)
    if scaling:
        ax.set(xlabel='MPI ranks', xscale='log', yscale='log')
        eff = [r for r in rows if r['efficiency_fastest'] is not None]
        axes[0, 1].plot([r['ranks'] for r in eff], [100*r['efficiency_fastest'] for r in eff], 'o-', label='Fastest')
        axes[0, 1].plot([r['ranks'] for r in eff], [100*r['efficiency_median'] for r in eff], 's--', label='Median')
        axes[0, 1].set(xlabel='MPI ranks', ylabel='Efficiency (%)', xscale='log')
        axes[0, 1].legend()
    else:
        ax.set_xticks(x, [r['case'] for r in rows], rotation=30, ha='right')
    ax.legend()
    fig.tight_layout()
    path = folder / f'{series}.svg'
    fig.savefig(path, metadata={'Date': None})
    path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines()) + '\n')
    plt.close(fig)


def plot_kernels(folder, series, cases):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'svg.hashsalt': 'benchmark-suite', 'svg.fonttype': 'none'})
    fig, ax = plt.subplots(figsize=(8, 4.5))
    labels = [str(c['ranks']) for c in cases]
    bottom = [0.0] * len(cases)
    for category in CATEGORIES:
        totals = [c['measurement']['kernel_nanoseconds'] for c in cases]
        shares = [100*t[category]/sum(t.values()) for t in totals]
        ax.bar(labels, shares, bottom=bottom, label=category)
        bottom = [a+b for a,b in zip(bottom,shares)]
    ax.set(xlabel='GPU MPI ranks', ylabel='Summed kernel duration share (%)', title=series)
    ax.legend(ncol=4)
    fig.tight_layout()
    path = folder / f'{series}_kernels.svg'
    fig.savefig(path, metadata={'Date': None})
    path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines()) + '\n')
    plt.close(fig)


def write_scaling_table(folder, rows, baselines):
    lines = ['# GPU scaling — DRAC-style comparison', '',
             'Measured values use the slowest rank’s median seconds per step. Throughput is global interior cells/median time.',
             'Strong efficiency = Tbaseline × Nbaseline / (Tn × N). Weak efficiency = T₁/Tn; interior cells/GPU remain fixed.',
             'GPU memory is the maximum device-used GiB across ranks after timing, including CUDA context and any cached allocations; it is not a peak model-only allocation.',
             'Pending/failed rows retain their state and no invented measurements. [Reference methodology](../../../../../Oceananigans-DRAC/docs/drac.md).', '']
    groups = [('Strong scaling', [r for r in rows if r['series'] in ('gpu_scaling_super_fine','gpu_scaling_super_super_fine','gpu_scaling_super_super_super_fine')]),
              ('Weak scaling', [r for r in rows if r['series'] == 'gpu_weak_scaling_super_fine'])]
    for title, selected in groups:
        lines += [f'## {title}', '', '| Resolution (cells) | GPUs | Nodes | Partition | Δt (s) | Median s/step | Efficiency | Throughput (cells/s) | Memory/GPU (GiB) | State |',
                  '|---|---:|---:|---|---:|---:|---:|---:|---:|---|']
        for row in selected:
            timing = f"{row['median']:.6f}" if row['median'] is not None else '—'
            efficiency = f"{100*row['efficiency_median']:.1f}%" if row['efficiency_median'] is not None else '—'
            throughput = f"{row['throughput_cells_per_second']:.3e}" if row['throughput_cells_per_second'] is not None else '—'
            memory = f"{row['gpu_memory_max_gib']:.2f}" if row['gpu_memory_max_gib'] is not None else '—'
            lines.append(f"| {row['resolution']} | {row['ranks']} | {row['nodes']} | {row['partition']} | {row['dt']} | {timing} | {efficiency} | {throughput} | {memory} | {row['state']} |")
        for series in dict.fromkeys(r['series'] for r in selected):
            if series in baselines:
                lines += ['', f"{series} baseline: **{baselines[series]['ranks']} GPUs**."]
    lines += ['', 'Full configuration, local resolutions, failure details, source revisions and job IDs are in [plot.md](plot.md) and each case directory.',
              'Time steps decrease with the finest horizontal spacing (60, 30, 15, … s); efficiency compares wall time per model step, not equal simulated duration.']
    (folder / 'scaling.md').write_text('\n'.join(lines) + '\n')
