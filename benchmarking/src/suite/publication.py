"""Common result evidence and safe commits for either execution backend."""
import subprocess
from .storage import digest


def profile_manifest(destination, atomic_json):
    files = [dict(path=str(path), bytes=path.stat().st_size, sha256=digest(path))
             for path in sorted((destination / 'raw_profiles').rglob('*')) if path.is_file()]
    if files:
        atomic_json(destination / 'profile_manifest.json', files)


def annotate_failures(folder, data, atomic_json):
    for case in data['cases']:
        if case['state'] not in ('FAILED', 'OUT_OF_MEMORY'):
            continue
        case_dir = folder / case['id']
        logs = [case_dir / 'job.out', *case_dir.glob('rank_*/profile.out')]
        messages = []
        for log in logs:
            if log.exists():
                messages.extend(line for line in log.read_text(errors='replace').splitlines()
                                if any(marker in line for marker in ('OutOfGPUMemoryError', 'OutOfMemoryError',
                                    'Out of GPU memory', 'Pressure solve failed', 'Recomputed pressure residual', 'ERROR:')))
        memory_errors = [line for line in messages if any(marker in line for marker in
                         ('OutOfGPUMemoryError', 'OutOfMemoryError', 'Out of GPU memory'))]
        if messages:
            case['details'] = 'Execution failed; ' + (memory_errors or messages)[0][:1000]
        if memory_errors:
            case['state'] = 'OUT_OF_MEMORY'
    atomic_json(folder / 'suite.json', data)


def commit_records(destination, repo):
    # Only the study's designated result tree is staged. Never stage user edits
    # elsewhere or consume an existing staged change.
    if subprocess.run(['git', '-C', str(repo), 'diff', '--cached', '--quiet']).returncode:
        raise RuntimeError('Index contains unrelated staged changes; refusing automatic commit')
    relative = str(destination.relative_to(repo))
    subprocess.run(['git', '-C', str(repo), 'add', '-u', '--', relative], check=True)
    # New curated JSON/Markdown files are ignored globally. Add scientific
    # records explicitly while keeping captures and closed raw logs out of Git.
    paths = [str(p.relative_to(repo)) for p in destination.rglob('*') if p.is_file()
             and (p.relative_to(destination).parts[0] in {'baseline', 'dagger', 'comparisons'} or
                  len(p.relative_to(destination).parts) == 1)
             and (p.suffix in {'.json', '.md', '.csv', '.svg', '.toml', '.txt'} or p.name == 'source.tar.gz')
             and not {'raw_profiles', 'run_records', '.runtime', '__pycache__'}.intersection(p.relative_to(destination).parts)
             and not p.name.endswith(('.lock', '.tmp')) and p.stat().st_size < 64 * 1024**2]
    for offset in range(0, len(paths), 100):
        subprocess.run(['git', '-C', str(repo), 'add', '-f', '--', *paths[offset:offset + 100]], check=True)
    if subprocess.run(['git', '-C', str(repo), 'diff', '--cached', '--quiet']).returncode:
        subprocess.run(['git', '-C', str(repo), 'commit', '-m',
                        f'Record {destination.name} {destination.parent.name} baseline and Dagger outcomes'], check=True)
