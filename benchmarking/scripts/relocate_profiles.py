#!/usr/bin/env python3
"""Move the paired study's closed Nsight captures with SHA-256 verification."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from suite.storage import atomic_json, copy_verified


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--results', type=Path, required=True)
    parser.add_argument('--old-root', type=Path, default=Path('/tmp/benchmark_traces'))
    args = parser.parse_args()
    series = 'gpu_nsight_scaling_super_fine'
    for mode in ('baseline', 'dagger'):
        identity = hashlib.sha256(str(args.study.resolve() / mode).encode()).hexdigest()[:16]
        root = args.old_root / 'non_hydrostatic_models' / 'rondeau' / identity / series / series
        target = args.results.resolve() / mode / series
        target.mkdir(parents=True, exist_ok=True)
        manifest = target / 'profile_manifest.json'
        records = json.loads(manifest.read_text()) if manifest.exists() else []
        for source in sorted(root.rglob('*.nsys-rep')):
            destination = target / 'raw_profiles' / source.relative_to(root)
            record = copy_verified(source, destination, remove=True)
            records = [r for r in records if r['path'] != record['path']] + [record]
            atomic_json(manifest, records)
            print(f"Verified and moved {record['bytes'] / 2**30:.3f} GiB: {destination}", flush=True)
            # A failed profiled run may not have reached trace_path.txt export.
            case, rank = source.relative_to(root).parts[:2]
            rank_dir = args.study / mode / series / case / rank
            rank_dir.mkdir(parents=True, exist_ok=True)
            (rank_dir / 'trace_path.txt').write_text(str(destination) + '\n')
            (rank_dir / 'trace_bytes.txt').write_text(str(record['bytes']) + '\n')
            (rank_dir / 'trace_sha256.txt').write_text(record['sha256'] + '  ' + str(destination) + '\n')
        (target / 'profiles.md').write_text('# Retained Nsight captures\n\n'
            'Raw `.nsys-rep` captures are in `raw_profiles/<case>/rank_<n>/`. '
            'They are stored locally and excluded from Git; `profile_manifest.json` records '
            'their old and new locations, byte sizes and SHA-256 checksums.\n\n'
            'These profiled runs failed application validation or allocation. Captures are retained '
            'as diagnostic evidence and do not constitute accepted performance measurements.\n')
    # Remove only empty directories; leave any unrelated or unrecognized file intact.
    for folder in sorted(args.old_root.rglob('*'), key=lambda p: len(p.parts), reverse=True):
        if folder.is_dir():
            try:
                folder.rmdir()
            except OSError:
                pass
    try:
        args.old_root.rmdir()
    except OSError:
        pass


if __name__ == '__main__':
    main()
