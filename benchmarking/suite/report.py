"""Validate rank artifacts and generate comparable suite reports."""
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import statistics
from .plan import GPU_BASELINES, SERIES

TERMINAL = {'COMPLETED', 'FAILED', 'CANCELLED', 'TIMEOUT', 'OUT_OF_MEMORY', 'NODE_FAIL',
            'PREEMPTED', 'BOOT_FAIL', 'DEADLINE', 'REVOKED', 'INVALID_RESULTS',
            'SUBMISSION_FAILED', 'RESOURCE_LIMIT', 'GEOMETRY_LIMIT', 'INTERRUPTED', 'NOT_RUN'}
CATEGORIES = ('Gc', 'Gu', 'Gv', 'Others')


def kernel_categories(config):
    return ('Gc', 'Gu', 'Gv', 'Gw', 'Others') if config.get('model_type') == 'NonhydrostaticModel' else CATEGORIES


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
        nonhydrostatic = config.get('model_type') == 'NonhydrostaticModel'
        substeps_valid = (entry['retained_free_surface_substeps'] is None if nonhydrostatic
                          else isinstance(entry['retained_free_surface_substeps'], int) and entry['retained_free_surface_substeps'] > 0)
        if nonhydrostatic and (entry.get('model_type') != 'NonhydrostaticModel' or
                               entry.get('free_surface') != 'RigidLid' or
                               entry.get('pressure_solver') != config['pressure_solver'] or
                               entry.get('pressure_solver_converged') is not True):
            raise ValueError('Unexpected nonhydrostatic model or unconverged pressure solver')
        if nonhydrostatic and config.get('pressure_preconditioner'):
            solves = entry.get('pressure_solves', [])
            # set!(NonhydrostaticModel) projects the initial velocities once.
            expected_solves = 1 + 3 * (config['warmup_steps'] + config['samples'] * config['time_steps'])
            if entry.get('pressure_preconditioner') != config['pressure_preconditioner'] or len(solves) != expected_solves:
                raise ValueError('Missing pressure stage checks or unexpected preconditioner')
            for solve in solves:
                residual, tolerance = solve['final_residual'], solve['tolerance']
                if (solve['converged'] is not True or not math.isfinite(residual) or
                        not math.isfinite(tolerance) or tolerance < 0 or residual > tolerance or
                        not 0 <= solve['iterations'] <= config['pressure_max_iterations']):
                    raise ValueError('Invalid pressure residual or iteration count')
            if config.get('pressure_check_true_residual'):
                true_residual = entry.get('pressure_final_true_residual')
                if (not isinstance(true_residual, (int, float)) or not math.isfinite(true_residual) or
                        true_residual < 0 or true_residual > solves[-1]['tolerance']):
                    raise ValueError('Invalid recomputed pressure residual')
            if config.get('pressure_preconditioner') == 'LocalFFTPreconditioner' and config.get('pressure_preconditioner_check'):
                if entry.get('pressure_preconditioner_validation', {}).get('passed') is not True:
                    raise ValueError('Missing preconditioner symmetry/definiteness check')
        if (entry['configuration'] != config or entry['grid_size'] != expected or
                entry['float_type'] != 'Float64' or entry['finite_state'] is not True or
                entry['metadata']['num_threads'] != 1 or not substeps_valid):
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
                  retained_substeps=sorted({e['retained_free_surface_substeps'] for e in entries if e['retained_free_surface_substeps'] is not None}))
    result['nodes'] = len({l['hostname'] for l in layout})
    memory = [e.get('gpu_memory_used_bytes') for e in entries]
    if gpu and any(m is not None for m in memory):
        if any(not isinstance(m, int) or m <= 0 for m in memory):
            raise ValueError('Incomplete or invalid GPU device memory measurements')
        result['gpu_memory_used_bytes'] = max(memory)
        result['gpu_memory_max_gib'] = max(memory) / 2**30
    if config['profile']:
        categories = kernel_categories(config)
        totals = dict.fromkeys(categories, 0)
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
                prefix = 'compute_' if config.get('model_type') == 'NonhydrostaticModel' else 'compute_hydrostatic_free_surface_'
                category = next((c for c in categories[:-1] if prefix + c in row['Name']), 'Others')
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
            and 'measurement' in c and ('scaling' in c['series'] or c['series'] == 'gpu_partition_super_fine')
            and c['ranks'] == c['configuration'].get('baseline_ranks', GPU_BASELINES.get(c['series'], 1))}


def efficiencies(case, baseline):
    if not baseline or 'measurement' not in case:
        return None, None
    cfg, base_cfg = case['configuration'], baseline['configuration']
    weak = cfg.get('scaling_type') == 'weak' or case['series'] == 'gpu_weak_scaling_super_fine'
    common = ('device', 'threads_per_rank', 'momentum_advection', 'tracer_advection', 'closure',
              'timestepper', 'warmup_steps', 'samples', 'time_steps', 'profile', 'pressure_preconditioner')
    if any(cfg.get(k) != base_cfg.get(k) for k in common):
        return None, None
    if not weak and any(cfg.get(k) != base_cfg.get(k) for k in ('global_resolution', 'dt')):
        return None, None
    divisor = 1 if (case['configuration'].get('scaling_type') == 'weak' or case['series'] == 'gpu_weak_scaling_super_fine') else case['ranks'] / baseline['ranks']
    return tuple(baseline['measurement'][s] / (case['measurement'][s] * divisor)
                 for s in ('fastest', 'median'))


def report_cases(folder, cases, reference_suites=(), replacement_suites=()):
    roots = [(cases, Path(folder))]
    for path in reference_suites:
        root = Path(path)
        roots.append((json.loads((root / 'suite.json').read_text())['cases'], root))
    for path in reversed(replacement_suites):
        root = Path(path)
        roots.insert(0, (json.loads((root / 'suite.json').read_text())['cases'], root))
    selected = []
    seen = set()
    for source, root in roots:
        for series in dict.fromkeys(c['series'] for c in source):
            if series not in seen:
                selected.extend((c, root) for c in source if c['series'] == series)
                seen.add(series)
    return selected


def write_model_comparison(path, folder, cases, comparison_suites):
    """Compare validated case timings, keeping each model's measured baseline separate."""
    path, folder = Path(path), Path(folder)
    current_model = next(c['configuration'].get('model_type', 'HydrostaticFreeSurfaceModel')
                         for c in cases if 'configuration' in c)
    current = [(c, folder) for c in cases]
    references = report_cases(path.parent, [], replacement_suites=comparison_suites)
    models = {'HydrostaticFreeSurfaceModel': [], 'NonhydrostaticModel': []}
    models[current_model] = current
    for case, root in references:
        model = case.get('configuration', {}).get('model_type', 'HydrostaticFreeSurfaceModel')
        if model == current_model:
            raise ValueError('Comparison suites must belong to the other model')
        models[model].append((case, root))
    baselines = {model: scaling_baselines([c for c, _ in items]) for model, items in models.items()}
    indices = {model: {c['id']: (c, root) for c, root in items} for model, items in models.items()}
    hydro, nonhydro = indices.values()
    pairs = []
    match_fields = ('device', 'ranks', 'grid_type', 'float_type', 'global_resolution', 'partition',
                    'threads_per_rank', 'dt', 'warmup_steps', 'samples', 'time_steps', 'profile')
    for key in dict.fromkeys([*hydro, *nonhydro]):
        h, n = hydro.get(key), nonhydro.get(key)
        mismatch = [k for k in match_fields if h and n and
                    h[0].get('configuration', {}).get(k) != n[0].get('configuration', {}).get(k)]
        valid = (h and n and not mismatch and all(c['state'] == 'COMPLETED' and
                                                'measurement' in c for c, _ in (h, n)))
        pairs.append((key, h, n, mismatch, bool(valid)))
    def link(root, case):
        target = root / case['id'] / ('configuration.md' if 'configuration' in case else 'limit.md')
        return Path(os.path.relpath(target, path.parent)).as_posix()
    def value(item, statistic):
        if item and item[0]['state'] == 'COMPLETED' and 'measurement' in item[0]:
            return item[0]['measurement'][statistic]
        return None
    def number(value):
        return f'{value:.6f}' if value is not None else '—'
    lines = ['# Hydrostatic and nonhydrostatic performance on Rorqual', '',
             'H = HydrostaticFreeSurfaceModel; N = NonhydrostaticModel. Only completed, validated measurements supply timings.',
             'Ratios are N seconds/step divided by H seconds/step: 1 means equal time, above 1 means N takes longer. They compare full configurations, not an isolated change in the model equations.',
             'Shared settings: latitude–longitude grid without bathymetry, Float64, T/S, TEOS10 buoyancy, traditional spherical Coriolis, global/local resolution and partition, one thread/rank, Δt, and timing windows.',
             'H uses WENOVectorInvariant momentum, WENO7 tracers, CATKE, SplitRungeKutta3 and a split-explicit free surface (30 requested substeps; extended halos on GPU).',
             'N uses WENO7 momentum/tracers, ScalarDiffusivity (ν=1e-3, κ=1e-5 m²/s), RungeKutta3, a rigid lid, and a three-dimensional ConjugateGradientPoissonSolver. Free-surface substeps are not applicable.',
             'Pressure preconditioners, tolerances, iteration caps and initial-condition seeds are recorded in each configuration; solver pilots remain separate from production timings.',
             'The physics and numerical-method differences above are intentional. CATKE can also introduce a TKE tracer beyond T/S. Per-case links retain actual settings, placement, solver checks, and source/environment provenance.',
             'Each series comes entirely from its selected run; a pending rerun does not borrow an older baseline. Efficiencies use each model’s own measured baseline and are not cross-model timing ratios.', '',
             'Ideal strong/weak MPI efficiency is 100%. Source plots include expected ratios and ideal timing/efficiency references. Profiled timings are compared only with profiled timings.', '',
             '## Selected runs', '']
    for model, items in models.items():
        for root in dict.fromkeys(root for _, root in items):
            target = Path(os.path.relpath(root / 'plot.md', path.parent)).as_posix()
            lines.append(f'- {model}: [{root.name}]({target})')
    lines += ['', '## Series overview', '',
              '| Series | H completed | N completed | Matched completed pairs | N/H median time ratio range |',
              '|---|---:|---:|---:|---|']
    for series in SERIES:
        selected = [p for p in pairs if p[0].split('/')[0] == series]
        completed = [sum(c['series'] == series and c['state'] == 'COMPLETED' and 'measurement' in c
                         for c, _ in items) for items in models.values()]
        ratios = [value(n, 'median') / value(h, 'median') for _, h, n, _, valid in selected if valid]
        span = f'{min(ratios):.3f}–{max(ratios):.3f}' if ratios else '—'
        lines.append(f'| `{series}` | {completed[0]} | {completed[1]} | {len(ratios)} | {span} |')
    for series in SERIES:
        lines += ['', f'## {series}', '',
                  '| Case | Ranks | Global grid | Partition | H outcome | N outcome | H fastest / median s/step | N fastest / median s/step | N/H fastest / median | H / N median efficiency | Pair status |',
                  '|---|---:|---|---|---|---|---:|---:|---:|---:|---|']
        for key, h, n, mismatch, valid in (p for p in pairs if p[0].split('/')[0] == series):
            case = (n or h)[0]
            cfg = case.get('configuration', {})
            grid = ' × '.join(map(str, cfg.get('global_resolution', []))) or 'See limit'
            partition = ' × '.join(map(str, case.get('partition') or [])) or '—'
            statuses = [f"[{item[0]['state']}]({link(item[1], item[0])})" if item else 'NOT RUN' for item in (h, n)]
            timings = [' / '.join(number(value(item, statistic)) for statistic in ('fastest', 'median')) for item in (h, n)]
            ratios = ' / '.join(f'{value(n, statistic)/value(h, statistic):.3f}' for statistic in ('fastest', 'median')) if valid else '—'
            efficiency = []
            for model, item in zip(models, (h, n)):
                _, eff = efficiencies(item[0], baselines[model].get(series)) if value(item, 'median') is not None else (None, None)
                efficiency.append(f'{100*eff:.1f}%' if eff is not None else '—')
            status = 'Matched workload and timing protocol' if valid else 'Unmatched: ' + ', '.join(mismatch) if mismatch else 'Awaiting validated pair'
            lines.append(f"| {key.split('/')[-1]} | {case['ranks']} | {grid} | {partition} | {statuses[0]} | {statuses[1]} | {timings[0]} | {timings[1]} | {ratios} | {' / '.join(efficiency)} | {status} |")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text('\n'.join(lines) + '\n')
    temporary.replace(path)


def write_report(folder, cases, plotting=True, reference_suites=(), replacement_suites=()):
    combined = report_cases(folder, cases, reference_suites, replacement_suites)
    case_roots = {c['id']: root for c, root in combined}
    display_series = {c['series'] for c in cases}
    cases = [c for c, _ in combined if c['series'] in display_series]
    successful = [c for c in cases if c['state'] == 'COMPLETED' and 'measurement' in c]
    nonhydrostatic = any(c.get('configuration', {}).get('model_type') == 'NonhydrostaticModel' for c in cases)
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
    protocols = sorted({(c['configuration']['warmup_steps'], c['configuration']['samples'],
                         c['configuration']['time_steps']) for c in cases if 'configuration' in c})
    timing_protocol = '; '.join(f'{w} untimed steps, {s} windows of {t} steps' for w, s, t in protocols)
    lines = ['# Benchmark suite', '',
             ('NonhydrostaticModel; rigid lid; LatitudeLongitudeGrid without bathymetry; Float64, WENO7 momentum/tracers, ScalarDiffusivity (ν=1e-3, κ=1e-5 m²/s), T/S, RungeKutta3. Pressure: ConjugateGradientPoissonSolver; traditional spherical Coriolis and TEOS10 buoyancy.' if nonhydrostatic else
              'HydrostaticFreeSurfaceModel; LatitudeLongitudeGrid without bathymetry; Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.'),
             'Δt=60 s on the standard grids; larger horizontal grids reduce Δt in proportion to grid spacing (see each configuration).',
             ('No free-surface substeps or extended free-surface halos.' if nonhydrostatic else '30 requested free-surface substeps.'),
             f'Actual timing protocols: {timing_protocol}.',
             ('One MPI rank per CPU core or GPU, one Julia computation thread per rank. Hydrostatic geometry bounds are retained to match partitions between models.' if nonhydrostatic else 'One MPI rank per CPU core or GPU, one Julia computation thread per rank. CPU extended halos=false; GPU=true.'),
             'Window boundaries synchronize MPI ranks and GPUs. Fastest/median statistics use the maximum across ranks.',
             'Strong efficiency = baseline time × baseline ranks / (time × ranks); weak efficiency = baseline time / time.',
             'Standard baselines use one rank; the larger GPU grids use 4 and 16 ranks. Missing baselines have no efficiency estimate.',
             'Reference lines show ideal inverse-rank strong timing, constant weak timing, and 100% efficiency.',
             'Resolution plots show previous-grid / next-grid time; doubling each grid dimension ideally gives 1/8.',
             'Profiled timings are separate; Nsight captures CUDA/NVTX/MPI after warmup. Kernel shares sum durations across ranks, not elapsed wall time.', '']
    for source in replacement_suites:
        relative = Path(os.path.relpath(Path(source) / 'plot.md', folder)).as_posix()
        lines += [f"Selected rerun: [{Path(source).name}]({relative}). Replaced series use that run's measurements and baseline; earlier raw records remain in their original directories.", '']
    for series in dict.fromkeys(c['series'] for c in cases):
        series_rows = [r for r in rows if r['series'] == series]
        completed = [r for r in series_rows if r['state'] == 'COMPLETED']
        lines += [f'## {series}', '', f"Highest completed count: **{max((r['ranks'] for r in completed), default=0)} ranks**.", '']
        if series in baselines:
            lines += [f"Efficiency baseline: **{baselines[series]['ranks']} measured ranks**.", '']
        if series == 'gpu_partition_super_fine' and series not in baselines:
            lines += ['MPI efficiency awaits the measured 1 × 1 × 1 baseline.', '']
        if plotting and (completed or series == 'gpu_partition_super_fine'):
            plotted_rows = [] if series == 'gpu_partition_super_fine' and series not in baselines else series_rows
            plot_series(folder, series, plotted_rows)
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
            categories = list(profiles[0]['measurement']['kernel_nanoseconds'])
            lines += ['', '| Profile | ' + ' | '.join(categories) + ' |', '|---|' + '---:|' * len(categories)]
            for profile in profiles:
                totals = profile['measurement']['kernel_nanoseconds']
                shares = ' | '.join(f'{100*totals[k]/sum(totals.values()):.2f}%' for k in categories)
                lines.append(f"| {profile['id'].split('/')[-1]} | {shares} |")
        for case in (c for c in successful if c['series'] == series):
            cfg = case['configuration']
            local = f"{min(cfg['x_sizes'])}–{max(cfg['x_sizes'])} × {min(cfg['y_sizes'])}–{max(cfg['y_sizes'])} × {cfg['global_resolution'][2]}"
            configuration_path = Path(os.path.relpath(case_roots[case['id']] / case['id'] / 'configuration.md', folder)).as_posix()
            solver_note = ('rigid lid; free-surface substeps not applicable' if cfg.get('model_type') == 'NonhydrostaticModel'
                           else f"retained free-surface substeps {case['measurement']['retained_substeps']}")
            lines += ['', f"[{case['id'].split('/')[-1]} configuration]({configuration_path}): local resolution **{local}**, {solver_note}."]
    if nonhydrostatic:
        lines += ['', '## Pressure convergence checks', '',
                  'Validation pilots are separate from production comparisons. Each new accepted result checks every pressure stage and the independently recomputed final residual.', '',
                  '| Case | Preconditioner | Recorded solves | Maximum iterations | Last residual / tolerance | Recomputed final residual | Outcome |',
                  '|---|---|---:|---:|---|---|---|']
        for case in cases:
            cfg = case.get('configuration', {})
            if cfg.get('model_type') != 'NonhydrostaticModel':
                continue
            source = case_roots[case['id']] / case['id']
            result, failure = source / 'results.json', source / 'rank_0/pressure_failure.json'
            records, true_residual = [], None
            try:
                if result.exists() and case['state'] in TERMINAL:
                    entry = json.loads(result.read_text())[0]
                    records, true_residual = entry.get('pressure_solves', []), entry.get('pressure_final_true_residual')
                elif failure.exists():
                    records = [json.loads(failure.read_text())]
            except (ValueError, IndexError):
                # Failed/interrupted exports can leave partial JSON evidence.
                records = []
            iterations = max((r['iterations'] for r in records), default=None)
            residual = (' / '.join(f'{v:.3e}' if isinstance(v, (int, float)) and math.isfinite(v)
                                  else 'nonfinite' for v in (records[-1]['final_residual'], records[-1]['tolerance']))
                        if records else '—')
            recomputed = f'{true_residual:.3e}' if true_residual is not None else '—'
            lines.append(f"| {case['id']} | {cfg.get('pressure_preconditioner', 'historical default')} | {len(records) or '—'} | {iterations if iterations is not None else '—'} | {residual} | {recomputed} | {case['state']} |")
    lines += scaling_tables(folder, cases, reference_suites, plotting=plotting,
                            combined=combined)
    (folder / 'plot.md').write_text('\n'.join(lines) + '\n')


def scaling_tables(folder, cases, reference_suites, plotting=False, combined=None):
    combined = combined if combined is not None else report_cases(folder, cases, reference_suites)
    if not any(c['series'].startswith('gpu_scaling_') or c['series'] == 'gpu_weak_scaling_super_fine'
               for c, _ in combined):
        return []
    baselines = scaling_baselines([c for c, _ in combined])
    lines = ['', '## GPU scaling comparison (DRAC table format)', '',
             'Reference: Oceananigans-DRAC/docs/drac.md, section 8. These are Rorqual measurements, not the reference’s Nibi timings.',
             'Timing protocols are recorded per case; the reference uses five 100-step windows. Tables use median seconds per step.',
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
            if memory is None and measurement.get('gpu_memory_max_gib') is not None:
                memory = measurement['gpu_memory_max_gib'] * 2**30
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
    partition_efficiency = series == 'gpu_partition_super_fine'
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
    elif partition_efficiency:
        ax.plot(x, [100*r['efficiency_fastest'] for r in rows], 'o-', label='Fastest')
        ax.plot(x, [100*r['efficiency_median'] for r in rows], 's--', label='Median')
        ax.axhline(100, color='black', linestyle=':', label='Ideal: 100%')
        if not rows:
            ax.text(0.5, 0.5, 'Awaiting measured 1 × 1 × 1 baseline',
                    transform=ax.transAxes, ha='center')
    else:
        ax.plot(x, [r['fastest'] for r in rows], 'o-', label='Fastest')
        ax.plot(x, [r['median'] for r in rows], 's--', label='Median')
    ax.set(ylabel='MPI efficiency (%) vs 1 × 1 × 1' if partition_efficiency else
                  'Previous-grid / next-grid time' if resolution else 'Seconds per step', title=series)
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
    for category in cases[0]['measurement']['kernel_nanoseconds']:
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
