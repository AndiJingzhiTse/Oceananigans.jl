"""Compare matched direct and Dagger timing windows, including failed cases."""
import csv
import json
from pathlib import Path

from .plan import SERIES


def comparison_rows(study):
    rows = []
    for series in SERIES:
        variants = {}
        for mode in ('baseline', 'dagger'):
            path = Path(study) / mode / series / 'suite.json'
            data = json.loads(path.read_text()) if path.exists() else {'cases': []}
            variants[mode] = {c['id']: c for c in data['cases']}
        for case_id in sorted(set(variants['baseline']) | set(variants['dagger'])):
            base, dagger = (variants[m].get(case_id, {}) for m in ('baseline', 'dagger'))
            cfg = base.get('configuration', dagger.get('configuration', {}))
            row = dict(series=series, case=case_id, ranks=base.get('ranks', dagger.get('ranks')),
                       resolution='x'.join(map(str, cfg.get('global_resolution', []))),
                       partition='x'.join(map(str, cfg.get('partition', []))),
                       grid_type=cfg.get('grid_type', ''), profile=cfg.get('profile', False),
                       baseline_state=base.get('state', 'MISSING'), dagger_state=dagger.get('state', 'MISSING'),
                       baseline_fastest='', dagger_fastest='', baseline_median='', dagger_median='',
                       speedup_fastest='', speedup_median='',
                       details='; '.join(f'{m}: {c.get("details", "")}' for m, c in
                                         (('baseline', base), ('dagger', dagger))))
            configurations = [{k: v for k, v in c.get('configuration', {}).items()
                               if k != 'execution_mode'} for c in (base, dagger)]
            if base.get('state') == dagger.get('state') == 'COMPLETED':
                if configurations[0] != configurations[1]:
                    row['details'] = 'Incompatible configurations; no timing ratio'
                elif 'measurement' in base and 'measurement' in dagger:
                    for stat in ('fastest', 'median'):
                        row['baseline_' + stat] = base['measurement'][stat]
                        row['dagger_' + stat] = dagger['measurement'][stat]
                        row['speedup_' + stat] = base['measurement'][stat] / dagger['measurement'][stat]
            rows.append(row)
    return rows


def write_comparison(study, output, plotting=True):
    study, output = Path(study), Path(output)
    output.mkdir(parents=True, exist_ok=True)
    rows = comparison_rows(study)
    if rows:
        with (output / 'comparison.csv').open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
    lines = ['# Rondeau: nonhydrostatic baseline versus Dagger', '',
             'Dagger submits one task per timing window, restricted to the current MPI process and its sole Julia computation thread. '
             'Oceananigans retains its existing MPI domain decomposition. Both paths synchronize CUDA before completing a window.', '',
             'Speedup = baseline seconds per step / Dagger seconds per step. Above 1 favors Dagger; the equal-time reference is 1. '
             'Fastest and median timings are the maximum rank statistic. Only completed, validated pairs with matching configurations have ratios.', '',
             'Nsight timings are compared only against the matching profiled variant. Shared-machine activity can affect timings; '
             'these are paired runs, not exclusive-node measurements.', '',
             f'Raw study and execution logs: `{study}`.', '',
             '[Baseline records](baseline/plot.md) · [Dagger records](dagger/plot.md) · [All outcomes as CSV](comparison.csv)', '']
    for mode in ('baseline', 'dagger'):
        destination = output / mode
        destination.mkdir(exist_ok=True)
        selected = [{k: r[k] for k in ('series', 'case', 'ranks', 'resolution', 'partition', 'grid_type',
                                      mode + '_state', 'details')} for r in rows]
        (destination / 'status.json').write_text(json.dumps(selected, indent=2) + '\n')
    for series in SERIES:
        selected = [r for r in rows if r['series'] == series]
        paired = [r for r in selected if r['speedup_median'] != '']
        lines += [f'## {series}', '']
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
    (output / 'plot.md').write_text('# Rondeau nonhydrostatic benchmarks\n\n'
        '[Baseline versus Dagger: all series](comparison.md)\n\n'
        '[Baseline](baseline/plot.md) · [Dagger](dagger/plot.md)\n')
    return rows
