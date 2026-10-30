#!/usr/bin/env python3
"""Matched Nibi H100 baseline/Dagger scaling for both model families."""
import argparse
import copy
import csv
import fcntl
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / 'benchmarking/scripts'))
import benchmark_suite as runner
from suite.plan import MODEL_FOLDERS
from suite.variants import comparison_rows

SERIES = ('gpu_scaling_fine', 'gpu_scaling_super_fine')
COUNTS = (1, 2, 4, 8, 16)


def report(root, suites):
    setup_log = REPO / '.runtime/nibi_dagger/slurm_setup.out'
    if setup_log.exists():
        (root / 'setup.out').write_text(setup_log.read_text(errors='replace'))
    for folder, data in suites.values():
        runner.refresh(folder, data)
    rows = comparison_rows(root, SERIES)
    with (root / 'comparison.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    lines = ['# Nibi H100 baseline versus Dagger', '',
             'Matched pairs run sequentially in the same allocation, alternating order by GPU count. '
             'One MPI rank and one Julia computation thread per assigned H100. '
             'Dagger submits and fetches one synchronized task per timing window on the current process/thread.', '',
             'Two untimed steps, then five ten-step windows. Fastest and median seconds/step are '
             'the maximum across ranks of each rank statistic. Speedup = baseline / Dagger; ideal equal time = 1. '
             'Only completed validated pairs with matching configurations enter comparisons. '
             'Each variant uses its measured one-GPU baseline for strong-scaling efficiency.', '',
             '| Series | GPUs | Global resolution | MPI partition | Grid | Baseline | Dagger | Median s/step baseline / Dagger | Speedup |',
             '|---|---:|---|---|---|---|---|---|---:|']
    for r in rows:
        timing = f"{r['baseline_median']:.6g} / {r['dagger_median']:.6g}" if r['speedup_median'] != '' else '—'
        speed = f"{r['speedup_median']:.4f}" if r['speedup_median'] != '' else '—'
        lines.append(f"| {r['series']} | {r['ranks']} | {r['resolution']} | {r['partition']} | {r['grid_type']} | {r['baseline_state']} | {r['dagger_state']} | {timing} | {speed} |")
    paired = [r for r in rows if r['speedup_median'] != '']
    if paired:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        for series in SERIES:
            selected = [r for r in paired if r['series'] == series]
            if not selected:
                continue
            fig, axes = plt.subplots(1, 3, figsize=(15, 4), constrained_layout=True)
            for mode in ('baseline', 'dagger'):
                axes[0].plot([r['ranks'] for r in selected], [r[mode + '_median'] for r in selected], 'o-', label=mode)
                baseline = next((r[mode + '_median'] for r in rows if r['series'] == series and r['ranks'] == 1 and r[mode + '_median'] != ''), None)
                if baseline:
                    axes[0].plot(COUNTS, [baseline / n for n in COUNTS], '--', label=mode + ' ideal inverse-rank')
                    axes[1].plot([r['ranks'] for r in selected], [100 * baseline / (r[mode + '_median'] * r['ranks']) for r in selected], 'o-', label=mode)
            axes[1].axhline(100, linestyle='--', color='gray', label='Ideal efficiency 100%')
            axes[2].plot([r['ranks'] for r in selected], [r['speedup_median'] for r in selected], 'o-', label='baseline / Dagger')
            axes[2].axhline(1, linestyle='--', color='gray', label='Equal time 1')
            for ax, ylabel in zip(axes, ('Median seconds/step', 'MPI efficiency (%)', 'Speedup')):
                ax.set_xlabel('GPUs / MPI ranks')
                ax.set_ylabel(ylabel)
                ax.legend()
                ax.grid(alpha=0.3)
            fig.savefig(root / f'{series}_comparison.svg', metadata={'Date': None})
            plt.close(fig)
            lines += ['', f'![{series}]({series}_comparison.svg)']
    (root / 'comparison.md').write_text('\n'.join(lines) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', default='2026-10-30')
    parser.add_argument('--submit', action='store_true')
    parser.add_argument('--refresh', action='store_true')
    parser.add_argument('--commit', action='store_true')
    parser.add_argument('--dependency', help='Slurm setup job which must complete successfully')
    args = parser.parse_args()
    runtime = REPO / '.runtime/nibi_dagger'
    temporary = REPO / '.runtime/tmp'
    temporary.mkdir(parents=True, exist_ok=True)
    os.environ.update({k: str(temporary) for k in ('TMPDIR', 'TMP', 'TEMP', 'OMPI_MCA_orte_tmpdir_base')})
    runtime.mkdir(parents=True, exist_ok=True)
    with (runtime / 'controller.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX if args.refresh else fcntl.LOCK_EX | fcntl.LOCK_NB)
        for model, family in MODEL_FOLDERS.items():
            root = REPO / 'benchmarking/results' / family / 'nibi/dagger' / args.date
            root.mkdir(parents=True, exist_ok=True)
            suites = {}
            for mode in ('baseline', 'dagger'):
                for series in SERIES:
                    folder = root / mode / series
                    if (folder / 'suite.json').exists():
                        data = json.loads((folder / 'suite.json').read_text())
                    elif args.refresh:
                        raise ValueError(f'Missing plan: {folder}')
                    else:
                        server = runner.load_server(REPO / 'benchmarking/scripts/configs/nibi.json', model)
                        server.update(max_gpus=16, project=str(runtime / 'environment'),
                                      environment_script=str(REPO / 'benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/modules.sh'),
                                      execution_mode=mode, gpu_scaling_partition='balanced',
                                      full_gpu_nodes=False, gpu_time='06:00:00', partition_time='06:00:00',
                                      trace_root=str(root / mode / 'raw_profiles'))
                        server['environment'].update({k: str(temporary) for k in ('TMPDIR', 'TMP', 'TEMP', 'OMPI_MCA_orte_tmpdir_base')})
                        data = runner.prepare(folder, server, (series,))
                        data['cases'] = [c for c in data['cases'] if c['ranks'] in COUNTS]
                        runner.atomic_json(folder / 'suite.json', data)
                    suites[mode, series] = (folder, data)
            if args.submit:
                if args.dependency:
                    if not args.dependency.isdigit():
                        raise ValueError('Dependency must be a numeric Slurm job ID')
                    for folder, data in suites.values():
                        data['server']['gpu_sbatch_extra'] = ['--dependency=afterok:' + args.dependency]
                        runner.atomic_json(folder / 'suite.json', data)
                for series in SERIES:
                    for index, count in enumerate(COUNTS):
                        paired = []
                        for mode in (('baseline', 'dagger') if index % 2 == 0 else ('dagger', 'baseline')):
                            folder, data = suites[mode, series]
                            case = next(c for c in data['cases'] if c['ranks'] == count)
                            paired.append((folder, data, case))
                        if any(c['state'] != 'PLANNED' for _, _, c in paired):
                            continue
                        allocation = root / 'allocations' / series / f'{count}_gpus'
                        allocation.mkdir(parents=True, exist_ok=True)
                        scripts = [runner.group_script(folder, data['server'], [case]) for folder, data, case in paired]
                        script = allocation / 'paired.sh'
                        script.write_text('#!/usr/bin/env bash\nfailed=0\n' + '\n'.join('bash ' + shlex.quote(str(p)) + ' || failed=1' for p in scripts) + '\nexit "$failed"\n')
                        command = runner.sbatch_command(paired[0][1]['server'], [paired[0][2], paired[1][2]], script)
                        result = runner.command(command)
                        (allocation / 'submission.txt').write_text(shlex.join(command) + '\n' + result.stdout)
                        job = next((s.split(';')[0] for s in reversed(result.stdout.splitlines()) if s.split(';')[0].isdigit()), '')
                        state = 'PENDING' if result.returncode == 0 and job else 'SUBMISSION_FAILED'
                        for folder, data, case in paired:
                            case.update(state=state, job_id=job, details='Matched sequential allocation; see ' + str(allocation))
                            runner.atomic_json(folder / 'suite.json', data)
                        print(model, series, count, state, job, flush=True)
            report(root, suites)
            schedule_path = root / 'scheduling.json'
            if args.submit and not schedule_path.exists():
                ids = sorted({c['job_id'] for _, data in suites.values() for c in data['cases'] if c['job_id']})
                if ids:
                    finalizer = root / 'finalize.sh'
                    finalizer.write_text('#!/usr/bin/env bash\nset -eo pipefail\nsource ' +
                        shlex.quote(str(REPO / 'benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/modules.sh')) +
                        '\n' + shlex.join(['python3', str(Path(__file__).resolve()), '--date', args.date, '--refresh', '--commit']) + '\n')
                    cmd = ['sbatch', '--parsable', '--account=def-fpoulin', '--nodes=1', '--ntasks=1',
                           '--cpus-per-task=1', '--mem=4G', '--time=00:30:00', '--job-name=nibi_dagger_report',
                           '--dependency=afterany:' + ':'.join(ids), '--output=' + str(root / 'finalize.out'), str(finalizer)]
                    result = runner.command(cmd)
                    runner.atomic_json(schedule_path, dict(command=cmd, output=result.stdout, returncode=result.returncode))
                    if result.returncode:
                        raise RuntimeError('Finalizer submission failed: ' + result.stdout)
        if args.commit:
            with (REPO / '.git/benchmark_artifacts.lock').open('a') as artifact_lock:
                fcntl.flock(artifact_lock, fcntl.LOCK_EX)
                if runner.command(['git', '-C', REPO, 'diff', '--cached', '--quiet']).returncode:
                    raise RuntimeError('Unrelated staged changes; refusing automatic commit')
                for family in MODEL_FOLDERS.values():
                    destination = REPO / 'benchmarking/results' / family / 'nibi/dagger'
                    subprocess.run(['git', '-C', str(REPO), 'add', '--', str(destination)], check=True)
                    logs = list(destination.rglob('*.out'))
                    if logs:
                        subprocess.run(['git', '-C', str(REPO), 'add', '-f', '--', *map(str, logs)], check=True)
                if runner.command(['git', '-C', REPO, 'diff', '--cached', '--quiet']).returncode:
                    subprocess.run(['git', '-C', str(REPO), 'commit', '-m', 'Record Nibi paired baseline and Dagger benchmark outcomes'], check=True)


if __name__ == '__main__':
    main()
