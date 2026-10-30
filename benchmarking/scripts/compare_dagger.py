#!/usr/bin/env python3
"""Compatibility entry point for paired runs through the shared workflow."""
import argparse
from pathlib import Path
import subprocess

import benchmark_suite as runner
from suite.plan import MODEL_FOLDERS


def profile_manifest(destination):
    from suite.publication import profile_manifest as write_manifest
    return write_manifest(destination, runner.atomic_json)


def annotate_failures(folder, data):
    from suite.publication import annotate_failures as annotate
    return annotate(folder, data, runner.atomic_json)


def commit_records(destination):
    from suite.publication import commit_records as commit
    return commit(destination, runner.REPO)


def free_gpu_uuids():
    from suite.backends import free_gpu_uuids as available
    return available(runner.command)


def pending_pairs(studies, selected):
    pairs = []
    for order, series in enumerate(selected):
        cases = sorted(studies['baseline', series][1]['cases'], key=lambda c: (c['ranks'], c['id']))
        for index, case in enumerate(cases):
            modes = ('baseline', 'dagger') if index % 2 == 0 else ('dagger', 'baseline')
            if any(next(c for c in studies[mode, series][1]['cases'] if c['id'] == case['id'])['state'] == 'PLANNED'
                   for mode in modes):
                pairs.append((case['ranks'], order, index, series, case, modes))
    return sorted(pairs, key=lambda item: item[:3])


def source_fingerprint():
    paths = ('src', 'Project.toml', 'benchmarking/src', 'benchmarking/Project.toml', 'benchmarking/server')
    if subprocess.run(['git', '-C', str(runner.REPO), 'diff', '--quiet', 'HEAD', '--', *paths]).returncode:
        raise RuntimeError('Benchmark source has uncommitted changes; stop the study before editing code')
    return dict(zip(paths, subprocess.check_output(
        ['git', '-C', str(runner.REPO), 'rev-parse', *['HEAD:' + p for p in paths]], text=True).splitlines()))


def verify_source(expected, study):
    try:
        if source_fingerprint() != expected:
            raise RuntimeError('Source changed; stop this study before switching branches or changing physics')
    except RuntimeError as error:
        runner.atomic_json(study / 'progress.json', dict(state='STOPPED_SOURCE_CHANGE', details=str(error)))
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--study', type=Path, required=True, help='Fresh scratch directory, or an existing study to resume')
    parser.add_argument('--publish', type=Path, required=True)
    parser.add_argument('--project', type=Path, required=True, help='Shared isolated Julia environment including Dagger')
    parser.add_argument('--plan', action='store_true')
    parser.add_argument('--refresh', action='store_true')
    parser.add_argument('--commit', action='store_true')
    parser.add_argument('--series', help='Comma-separated subset; existing other series remain in comparisons')
    parser.add_argument('--model', choices=tuple(MODEL_FOLDERS), default='NonhydrostaticModel')
    parser.add_argument('--gpu-only', action='store_true', help='Select GPU series only; reject CPU selections')
    parser.add_argument('--wait-for-gpus', action='store_true', help='Use idle GPUs and wait without holding devices when busy')
    args = parser.parse_args()
    # Compatibility spelling only: all planning, execution, monitoring and
    # publication now use the scheduler-independent workflow.
    from suite.workflow import main as workflow_main
    translated = ['--study', str(args.study), '--config', str(args.config),
                  '--project', str(args.project), '--models', args.model, '--modes', 'both']
    for flag in ('plan', 'refresh', 'commit', 'gpu_only'):
        if getattr(args, flag):
            translated.append('--' + flag.replace('_', '-'))
    if args.refresh:
        translated = ['--study', str(args.study), '--refresh'] + (['--commit'] if args.commit else [])
    elif not args.plan:
        translated.append('--execute')
    if args.series and not args.refresh:
        translated += ['--series', args.series]
    return workflow_main(runner, translated, flat_study=True, publish_server=args.publish)


if __name__ == '__main__':
    main()
