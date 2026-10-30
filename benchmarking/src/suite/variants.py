"""Compare matched direct and Dagger timing windows, including failed cases."""
import csv
import json
import math
from pathlib import Path

from .plan import ALL_SERIES
from .execution import comparable_configuration


def comparison_rows(study, selected=ALL_SERIES, references=None):
    rows = []
    for series in selected:
        variants = {}
        sources = {}
        retained = {}
        for mode in ('baseline', 'dagger'):
            path = Path(study) / mode / series / 'suite.json'
            data = json.loads(path.read_text()) if path.exists() else {'cases': []}
            variants[mode] = {c['id']: c for c in data['cases']}
            sources[mode] = {c['id']: str(path) for c in data['cases']}
            retained[mode] = {}
            if references:
                reference = Path(references) / mode / series / 'suite.json'
                if reference.exists() and reference.resolve() != path.resolve():
                    retained[mode] = {c['id']: c for c in json.loads(reference.read_text())['cases']}
        local_ids = tuple(dict.fromkeys((*variants['baseline'], *variants['dagger'])))
        for mode in ('baseline', 'dagger'):
            for case_id in local_ids:
                if case_id not in variants[mode] and case_id in retained[mode]:
                    variants[mode][case_id] = retained[mode][case_id]
                    sources[mode][case_id] = str(Path(references) / mode / series / 'suite.json')
        for case_id in dict.fromkeys((*variants['baseline'], *variants['dagger'])):
            base, dagger = (variants[m].get(case_id, {}) for m in ('baseline', 'dagger'))
            cfg = base.get('configuration', dagger.get('configuration', {}))
            row = dict(series=series, case=case_id, ranks=base.get('ranks', dagger.get('ranks')),
                       resolution='x'.join(map(str, cfg.get('global_resolution', []))),
                       partition='x'.join(map(str, cfg.get('partition', []))),
                       grid_type=cfg.get('grid_type', ''), profile=cfg.get('profile', False),
                       baseline_state=base.get('state', 'MISSING'), dagger_state=dagger.get('state', 'MISSING'),
                       baseline_source=sources['baseline'].get(case_id, ''), dagger_source=sources['dagger'].get(case_id, ''),
                       baseline_method=base.get('configuration', {}).get('execution_adapter', {}).get('id', 'legacy'),
                       dagger_method=dagger.get('configuration', {}).get('execution_adapter', {}).get('id', 'legacy'),
                       baseline_fastest='', dagger_fastest='', baseline_median='', dagger_median='',
                       speedup_fastest='', speedup_median='',
                       baseline_ensemble_timed='', dagger_ensemble_timed='', speedup_ensemble_timed='',
                       baseline_ensemble_dispatch='', dagger_ensemble_dispatch='', speedup_ensemble_dispatch='',
                       details='; '.join(f'{m}: {c.get("details", "")}' for m, c in
                                         (('baseline', base), ('dagger', dagger))).rstrip())
            configurations = [comparable_configuration(c.get('configuration', {})) for c in (base, dagger)]
            if base.get('state') == dagger.get('state') == 'COMPLETED':
                if configurations[0] != configurations[1]:
                    row['details'] = 'Incompatible configurations; no timing ratio'
                elif 'measurement' in base and 'measurement' in dagger:
                    for stat in ('fastest', 'median'):
                        row['baseline_' + stat] = base['measurement'][stat]
                        row['dagger_' + stat] = dagger['measurement'][stat]
                        row['speedup_' + stat] = base['measurement'][stat] / dagger['measurement'][stat]
                    if cfg.get('ensemble_size'):
                        for stat in ('timed', 'dispatch'):
                            for mode, case in (('baseline', base), ('dagger', dagger)):
                                row[f'{mode}_ensemble_{stat}'] = case['measurement'][f'ensemble_{stat}_seconds']
                            row[f'speedup_ensemble_{stat}'] = row[f'baseline_ensemble_{stat}'] / row[f'dagger_ensemble_{stat}']
            rows.append(row)
    return rows


def write_comparison(study, output, plotting=True, selected=ALL_SERIES, model_type='NonhydrostaticModel', machine='rondeau', references=None):
    study, output = Path(study), Path(output)
    output.mkdir(parents=True, exist_ok=True)
    rows = comparison_rows(study, selected, references)
    if rows:
        with (output / 'comparison.csv').open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
    model_label = 'hydrostatic' if model_type == 'HydrostaticFreeSurfaceModel' else 'nonhydrostatic'
    previous = output / 'previous_results.md'
    if model_type == 'HydrostaticFreeSurfaceModel' and (output / 'plot.md').exists() and not (output / 'comparison.md').exists():
        if not previous.exists():
            previous.write_text((output / 'plot.md').read_text())
    lines = [f'# {machine.capitalize()}: {model_label} baseline versus Dagger', '',
             'Each case records its execution adapter, version, source hash and options. '
             'Ratios require equivalent workload settings and timing contracts; adapter identity may differ. '
             'The CSV records the source of each measurement, including any retained reference.', '',
             'Speedup = baseline seconds per step / Dagger seconds per step. Above 1 favors Dagger; the equal-time reference is 1. '
             'Fastest and median timings are the maximum rank statistic. Only completed, validated pairs with matching configurations have ratios.', '',
             'Nsight timings are compared only against the matching profiled variant. Shared-machine activity can affect timings; '
             'these are paired runs, not exclusive-node measurements.', '',
             f'Raw study and execution logs: `{study}`.', '',
             '[Baseline records](baseline/plot.md) · [Dagger records](dagger/plot.md) · [All outcomes as CSV](comparison.csv)', '']
    if 'gpu_ensemble' in selected:
        lines += ['In gpu_ensemble, four independent single-GPU simulations run concurrently. '
                  'Dagger schedules four complete simulations; the baseline uses four concurrent Distributed calls. '
                  'Ensemble speedups compare total timed makespan and dispatch-to-completion time.', '']
    if 'gpu_weak_scaling' in selected:
        weak_rows = [r for r in rows if r['series'] == 'gpu_weak_scaling' and r['resolution']]
        sequence = '; '.join(f"{r['resolution'].replace('x', ' × ')} on {r['ranks']} GPU(s)"
                             for r in weak_rows)
        cells = ', '.join(f"{math.prod(map(int, r['resolution'].split('x'))) / r['ranks']:,.0f}"
                          for r in weak_rows)
        lines += [f'Requested GPU weak-scaling sequence: {sequence}. Cells/GPU: {cells}. '
                  'Efficiency uses a linear cell-count reference when work per GPU increases.', '']
    for mode in ('baseline', 'dagger'):
        destination = output / mode
        destination.mkdir(exist_ok=True)
        status_rows = [{k: r[k] for k in ('series', 'case', 'ranks', 'resolution', 'partition', 'grid_type',
                                      mode + '_state', 'details')} for r in rows]
        (destination / 'status.json').write_text(json.dumps(status_rows, indent=2) + '\n')
    for series in selected:
        selected = [r for r in rows if r['series'] == series]
        paired = [r for r in selected if r['speedup_median'] != '']
        lines += [f'## {series}', '']
        if series == 'gpu_ensemble':
            from .ensemble import comparison_lines
            lines += comparison_lines(selected, output, plotting)
            continue
        if paired and plotting:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            figures = output / 'comparisons'
            figures.mkdir(exist_ok=True)
            figure, axes = plt.subplots(1, 2, figsize=(12, 4), constrained_layout=True)
            indices = list(range(len(paired)))
            for mode in ('baseline', 'dagger'):
                axes[0].plot(indices, [r[mode + '_median'] for r in paired], 'o-', label=mode)
            axes[0].set_ylabel('Median seconds per step')
            axes[0].set_yscale('log')
            axes[0].legend()
            axes[1].plot(indices, [r['speedup_median'] for r in paired], 'o-', label='baseline / Dagger')
            axes[1].axhline(1, color='gray', linestyle='--', label='Equal time (1)')
            axes[1].set_ylabel('Median speedup')
            axes[1].legend()
            for ax in axes:
                ax.set_xticks(indices, [r['case'] for r in paired], rotation=45, ha='right')
                ax.grid(alpha=0.25)
            figure.suptitle(series + (' (Nsight profiled)' if paired[0]['profile'] else ''))
            with matplotlib.rc_context({'svg.hashsalt': 'oceananigans-dagger-comparison'}):
                figure.savefig(figures / f'{series}.svg', metadata={'Date': None})
            plt.close(figure)
            lines += [f'![Timing and speedup](comparisons/{series}.svg)', '']
        lines += ['| Case | Resolution / partition | Baseline outcome | Dagger outcome | Median s/step baseline / Dagger | Speedup |',
                  '|---|---|---|---|---:|---:|']
        for row in selected:
            timings = (f"{row['baseline_median']:.6g} / {row['dagger_median']:.6g}"
                       if row['speedup_median'] != '' else '—')
            speedup = f"{row['speedup_median']:.4f}" if row['speedup_median'] != '' else '—'
            lines.append(f"| {row['case']} | {row['resolution']} / {row['partition']} | "
                         f"{row['baseline_state']} | {row['dagger_state']} | {timings} | {speedup} |")
        if not paired:
            lines += ['', 'No completed, validated pair is available.']
        for row in selected:
            if row['speedup_median'] == '':
                lines += ['', f"{row['case']}: {row['details']}"]
        lines += ['']
    (output / 'comparison.md').write_text('\n'.join(lines) + '\n')
    (output / 'plot.md').write_text(f'# {machine.capitalize()} {model_label} benchmarks\n\n'
        '[Baseline versus Dagger: all series](comparison.md)\n\n'
        '[Baseline](baseline/plot.md) · [Dagger](dagger/plot.md)\n' +
        ('\n[Previously retained results](previous_results.md)\n' if previous.exists() else ''))
    return rows
