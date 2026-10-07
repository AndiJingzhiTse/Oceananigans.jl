"""Validate rank artifacts and generate comparable suite reports."""
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics

TERMINAL = {'COMPLETED', 'FAILED', 'CANCELLED', 'TIMEOUT', 'OUT_OF_MEMORY', 'NODE_FAIL',
            'PREEMPTED', 'BOOT_FAIL', 'DEADLINE', 'REVOKED', 'INVALID_RESULTS',
            'SUBMISSION_FAILED', 'RESOURCE_LIMIT', 'GEOMETRY_LIMIT', 'INTERRUPTED'}
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
    memory = [e.get('gpu_memory_used_bytes') for e in entries]
    if gpu and any(m is not None for m in memory):
        if any(not isinstance(m, int) or m <= 0 for m in memory):
            raise ValueError('Incomplete or invalid GPU device memory measurements')
        result['gpu_memory_used_bytes'] = max(memory)
        result['gpu_memory_max_gib'] = max(memory) / 2**30
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


def scaling_baselines(cases):
    return {c['series']: c for c in cases if c['state'] == 'COMPLETED'
            and 'measurement' in c and 'scaling' in c['series']
            and c['ranks'] == c['configuration'].get('baseline_ranks', 1)}


def efficiencies(case, baseline):
    if not baseline or 'measurement' not in case:
        return None, None
    divisor = 1 if case['configuration'].get('scaling_type') == 'weak' else case['ranks'] / baseline['ranks']
    return tuple(baseline['measurement'][s] / (case['measurement'][s] * divisor)
                 for s in ('fastest', 'median'))


def write_report(folder, cases, plotting=True, reference_suites=()):
    successful = [c for c in cases if c['state'] == 'COMPLETED' and 'measurement' in c]
    baselines = scaling_baselines(cases)
    rows = []
    for case in cases:
        cfg, measurement = case.get('configuration', {}), case.get('measurement', {})
        baseline = baselines.get(case['series'])
        row = dict(series=case['series'], case=case['id'].split('/')[-1], ranks=case['ranks'],
                   partition='x'.join(map(str, case.get('partition') or [])),
                   resolution='x'.join(map(str, cfg.get('global_resolution', [1440, 720, 200]))),
                   grid_type='LatitudeLongitudeGrid', state=case['state'], job_id=case['job_id'],
                   fastest=measurement.get('fastest'), median=measurement.get('median'),
                   efficiency_fastest=None, efficiency_median=None, details=case['details'])
        row['efficiency_fastest'], row['efficiency_median'] = efficiencies(case, baseline)
        rows.append(row)
    with (folder / 'results.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, rows[0].keys(), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    lines = ['# Full benchmark suite', '',
             'LatitudeLongitudeGrid without bathymetry; Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.',
             'Δt=60 s on the standard grids; larger horizontal grids reduce Δt in proportion to grid spacing (see each configuration).',
             '30 requested free-surface substeps; two untimed steps and five ten-step windows.',
             'One MPI rank per CPU core or GPU, one Julia computation thread per rank. CPU extended halos=false; GPU=true.',
             'Window boundaries synchronize MPI ranks and GPUs. Fastest/median statistics use the maximum across ranks.',
             'Strong efficiency = baseline time × baseline ranks / (time × ranks); weak efficiency = baseline time / time.',
             'Standard baselines use one rank; the larger GPU grids use 4 and 16 ranks. Missing baselines have no efficiency estimate.',
             'Reference lines show ideal inverse-rank strong timing, constant weak timing, and 100% efficiency.',
             'Resolution plots show previous-grid / next-grid time; doubling each grid dimension ideally gives 1/8.',
             'Profiled timings are separate; Nsight captures CUDA/NVTX/MPI after warmup. Kernel shares sum durations across ranks, not elapsed wall time.', '']
    for series in dict.fromkeys(c['series'] for c in cases):
        series_rows = [r for r in rows if r['series'] == series]
        completed = [r for r in series_rows if r['state'] == 'COMPLETED']
        lines += [f'## {series}', '', f"Highest completed count: **{max((r['ranks'] for r in completed), default=0)} ranks**.", '']
        if series in baselines:
            lines += [f"Efficiency baseline: **{baselines[series]['ranks']} measured ranks**.", '']
        if plotting and completed:
            plot_series(folder, series, series_rows)
            lines += [f'![{series}]({series}.svg)', '']
        lines += ['| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |',
                  '|---|---:|---|---|---|---|---:|---:|---|---|']
        for row in series_rows:
            fast = f"{row['fastest']:.6f}" if row['fastest'] is not None else '—'
            med = f"{row['median']:.6f}" if row['median'] is not None else '—'
            efficiency = f"{100*row['efficiency_fastest']:.1f}% / {100*row['efficiency_median']:.1f}%" if row['efficiency_fastest'] is not None else '—'
            detail = row['details'].replace('|', '/').replace('\n', ' ')
            lines.append(f"| {row['case']} | {row['ranks']} | {row['partition']} | {row['resolution']} | {row['grid_type']} | {row['state']} | {fast} | {med} | {efficiency} | {detail} |")
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
    lines += scaling_tables(folder, cases, reference_suites, plotting=plotting)
    (folder / 'plot.md').write_text('\n'.join(lines) + '\n')


def scaling_tables(folder, cases, reference_suites, plotting=False):
    combined = [(c, folder) for c in cases]
    for path in reference_suites:
        root = Path(path)
        reference = json.loads((root / 'suite.json').read_text())
        combined += [(c, root) for c in reference['cases']]
    if not any(c['series'].startswith('gpu_scaling_') or c['series'] == 'gpu_weak_scaling_super_fine'
               for c, _ in combined):
        return []
    baselines = scaling_baselines([c for c, _ in combined])
    lines = ['', '## GPU scaling comparison (DRAC table format)', '',
             'Reference: Oceananigans-DRAC/docs/drac.md, section 8. These are Rorqual measurements, not the reference’s Nibi timings.',
             'This suite uses five ten-step windows; the reference uses five 100-step windows. Tables use median seconds per step.',
             'LatitudeLongitudeGrid; partitions are Px × Py × Pz. Nodes are measured from rank placement.',
             'Throughput = global interior cells / median step time. Memory is maximum device-used GiB across ranks after timing, including CUDA context and buffers; it is not peak memory.',
             'Missing memory measurements and unfinished timings are shown as —.', '']
    if plotting and plot_scaling_efficiency(folder, [c for c, _ in combined]):
        lines += ['Median efficiencies use each strong grid’s measured baseline and the weak study’s one-GPU baseline; the dotted reference is ideal 100% efficiency.', '',
                  '![Strong and weak scaling efficiency](gpu_scaling_efficiency.svg)', '']
    for weak in (False, True):
        selected = [(c, root) for c, root in combined if 'configuration' in c
                    and c['state'] not in {'RESOURCE_LIMIT', 'GEOMETRY_LIMIT'}
                    and (c['series'] == 'gpu_weak_scaling_super_fine' if weak
                         else c['series'].startswith('gpu_scaling_'))]
        if not selected:
            continue
        selected.sort(key=lambda item: (math.prod(item[0]['configuration']['global_resolution']), item[0]['ranks']))
        lines += ['### Weak scaling' if weak else '### Strong scaling', '',
                  'Weak efficiency = one-GPU baseline time / measured time; ideal = 100%. Interior cells/GPU = 207,360,000.' if weak else
                  'Strong efficiency = baseline time × baseline GPUs / (measured time × GPUs); ideal = 100%. Baselines: super_fine 1 GPU, super_super_fine 4 GPUs, super_super_super_fine 16 GPUs.', '',
                  '| Grid | Global resolution (cells) | GPUs | Nodes | Partition | Δt (s) | Median s/step | Efficiency | Throughput (cells/s) | Memory/GPU (GiB) | State |',
                  '|---|---|---:|---:|---|---:|---:|---:|---:|---:|---|']
        for case, root in selected:
            cfg = case['configuration']
            measurement = case.get('measurement', {}) if case['state'] == 'COMPLETED' else {}
            median = measurement.get('median')
            nodes = measurement.get('nodes')
            layout_path = root / case['id'] / 'layout.json'
            if median is not None and nodes is None and layout_path.exists():
                nodes = len({l['hostname'] for l in json.loads(layout_path.read_text())})
            _, efficiency = efficiencies(case, baselines.get(case['series'])) if median is not None else (None, None)
            cells = math.prod(cfg['global_resolution'])
            resolution = ' × '.join(map(str, cfg['global_resolution']))
            partition = ' × '.join(map(str, cfg['partition']))
            elapsed = f'{median:.6f}' if median is not None else '—'
            percent = f'{100*efficiency:.1f}%' if efficiency is not None else '—'
            throughput = f'{cells / median:.3e}' if median is not None else '—'
            memory = measurement.get('gpu_memory_used_bytes')
            gib = f'{memory / 2**30:.2f}' if memory is not None else '—'
            lines.append(f"| {cfg['grid_name']} | {resolution} ({cells:,}) | {case['ranks']} | {nodes if nodes is not None else '—'} | {partition} | {cfg['dt']:g} | {elapsed} | {percent} | {throughput} | {gib} | {case['state']} |")
        lines.append('')
    return lines


def plot_scaling_efficiency(folder, cases):
    baselines = scaling_baselines(cases)
    groups = {}
    for case in cases:
        if case['state'] != 'COMPLETED' or not (case['series'].startswith('gpu_scaling_')
                                              or case['series'] == 'gpu_weak_scaling_super_fine'):
            continue
        _, efficiency = efficiencies(case, baselines.get(case['series']))
        if efficiency is not None:
            groups.setdefault(case['series'], []).append((case['ranks'], 100 * efficiency))
    if 'gpu_weak_scaling_super_fine' not in groups:
        return False
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import StrMethodFormatter
    plt.rcParams.update({'svg.hashsalt': 'benchmark-suite', 'svg.fonttype': 'none'})
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for series, points in sorted(groups.items(), key=lambda item: baselines[item[0]]['ranks']):
        weak = series == 'gpu_weak_scaling_super_fine'
        points.sort()
        ax = axes[1 if weak else 0]
        baseline = baselines[series]
        grid = ' × '.join(map(str, baseline['configuration']['global_resolution']))
        label = '207,360,000 cells/GPU' if weak else f"{grid} ({baseline['ranks']}-GPU baseline)"
        ax.plot([p[0] for p in points], [p[1] for p in points], 'o-', label=label)
    for i, ax in enumerate(axes):
        ax.axhline(100, color='black', linestyle=':', label='Ideal: 100%')
        ax.set(xlabel='GPUs', ylabel='Median efficiency (%)',
               title='Weak scaling' if i else 'Strong scaling', xscale='log')
        ticks = sorted({x for line in ax.lines[:-1] for x in line.get_xdata()})
        ax.set_xticks(ticks)
        ax.xaxis.set_major_formatter(StrMethodFormatter('{x:g}'))
        ax.set_ylim(0, max(110, ax.get_ylim()[1]))
        ax.grid(alpha=0.2)
        ax.legend(fontsize=8, loc='lower left')
    fig.tight_layout()
    path = folder / 'gpu_scaling_efficiency.svg'
    fig.savefig(path, metadata={'Date': None})
    path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines()) + '\n')
    plt.close(fig)
    return True


def plot_series(folder, series, rows):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import StrMethodFormatter
    plt.rcParams.update({'svg.hashsalt': 'benchmark-suite', 'svg.fonttype': 'none'})
    rows = [r for r in rows if r['state'] == 'COMPLETED']
    scaling = 'scaling' in series
    weak = series == 'gpu_weak_scaling_super_fine'
    resolution = series.endswith('resolution')
    fig, axes = plt.subplots(1, 2 if scaling else 1, figsize=(11 if scaling else 8, 4.5), squeeze=False)
    ax = axes[0, 0]
    x = [r['ranks'] for r in rows] if scaling else list(range(len(rows)))
    if resolution:
        # Compare only adjacent planned grids; a failed intermediate grid must
        # not turn a fourfold refinement into a purported twofold refinement.
        all_rows = {r['case']: r for r in rows}
        pairs = [(all_rows[a], all_rows[b]) for a, b in
                 (('default', 'fine'), ('fine', 'super_fine'))
                 if a in all_rows and b in all_rows]
        x = list(range(len(pairs)))
        for statistic, marker, label in (('fastest', 'o-', 'Fastest'), ('median', 's--', 'Median')):
            ax.plot(x, [a[statistic] / b[statistic] for a, b in pairs], marker, label=label)
        ax.axhline(1/8, color='black', linestyle=':', label='Expected: 1/8')
        ax.set_xticks(x, [f"{a['case']} / {b['case']}" for a, b in pairs], rotation=20, ha='right')
    else:
        ax.plot(x, [r['fastest'] for r in rows], 'o-', label='Fastest')
        ax.plot(x, [r['median'] for r in rows], 's--', label='Median')
    ax.set(ylabel='Previous-grid / next-grid time' if resolution else 'Seconds per step', title=series)
    if scaling:
        ax.set(xlabel='MPI ranks', xscale='log', yscale='log')
        if weak:
            ax.set_yscale('linear')
            ax.yaxis.set_major_formatter(StrMethodFormatter('{x:g}'))
        baseline = next((r for r in rows if r['efficiency_fastest'] is not None
                         and math.isclose(r['efficiency_fastest'], 1)), None)
        if baseline:
            ideal = [baseline['fastest'] if weak else baseline['fastest'] * baseline['ranks'] / n for n in x]
            label = ('Ideal: constant time' if weak else 'Ideal: one-rank fastest / ranks'
                     if baseline['ranks'] == 1 else f"Ideal: {baseline['ranks']}-rank fastest × {baseline['ranks']} / ranks")
            ax.plot(x, ideal, ':', color='black', label=label)
        eff = [r for r in rows if r['efficiency_fastest'] is not None]
        axes[0, 1].plot([r['ranks'] for r in eff], [100*r['efficiency_fastest'] for r in eff], 'o-', label='Fastest')
        axes[0, 1].plot([r['ranks'] for r in eff], [100*r['efficiency_median'] for r in eff], 's--', label='Median')
        axes[0, 1].set(xlabel='MPI ranks', ylabel='Efficiency (%)', xscale='log')
        if weak:
            for axis in (ax, axes[0, 1]):
                axis.set_xticks(x)
                axis.xaxis.set_major_formatter(StrMethodFormatter('{x:g}'))
        axes[0, 1].axhline(100, color='black', linestyle=':', label='Ideal: 100%')
        axes[0, 1].legend()
    elif not resolution:
        ax.set_xticks(x, [r['case'] for r in rows], rotation=30, ha='right')
    if series == 'gpu_partition_super_fine':
        ax.set_ylim(bottom=0)
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
