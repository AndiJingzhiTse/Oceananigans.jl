"""Preserve closed benchmark artifacts before removing their temporary copies."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat


def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def atomic_json(path, value):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)


def runtime_environment(destination):
    destination = Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=True, mode=0o700)
    # MPI's Unix sockets need a short pathname. This alias contains no data:
    # its target and every temporary file remain inside the results tree.
    alias = Path.home() / '.ocean-tmp' / hashlib.sha256(str(destination).encode()).hexdigest()[:12]
    alias.parent.mkdir(exist_ok=True, mode=0o700)
    if not alias.is_symlink():
        alias.symlink_to(destination, target_is_directory=True)
    if alias.resolve() != destination:
        raise ValueError(f'Temporary-directory alias points elsewhere: {alias}')
    return {name: str(alias) for name in ('TMPDIR', 'TMP', 'TEMP', 'OMPI_MCA_orte_tmpdir_base')}


def copy_verified(source, destination, remove=False):
    source, destination = Path(source), Path(destination)
    before = source.stat()
    destination.parent.mkdir(parents=True, exist_ok=True)
    checksum = None
    if not destination.exists():
        partial = destination.with_name(destination.name + '.copying')
        value = hashlib.sha256()
        with source.open('rb') as incoming, partial.open('wb') as outgoing:
            for block in iter(lambda: incoming.read(8 * 1024 * 1024), b''):
                value.update(block)
                outgoing.write(block)
            outgoing.flush()
            os.fsync(outgoing.fileno())
        checksum = value.hexdigest()
        if partial.stat().st_size != before.st_size or digest(partial) != checksum:
            raise ValueError(f'Copy verification failed: {source}')
        shutil.copystat(source, partial)
        partial.replace(destination)
    else:
        checksum = digest(source)
        if destination.stat().st_size != before.st_size or digest(destination) != checksum:
            raise ValueError(f'Destination differs from source: {destination}')
    after = source.stat()
    if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
        raise ValueError(f'Source changed during copy: {source}')
    record = dict(source=str(source), path=str(destination), bytes=before.st_size, sha256=checksum)
    if remove:
        source.unlink()
    return record


def archive_finished_case(folder, case, destination, allocation_closed=False):
    source = Path(folder) / case['id']
    closed = allocation_closed or (source / 'finished.txt').exists() or (case['state'] in ('TIMEOUT', 'INTERRUPTED') and
                                                     (source / 'started.txt').exists())
    if case['state'] in ('RUNNING', 'PLANNED') or not closed:
        return False
    archive = Path(destination) / case['series'] / 'run_records' / case['id']
    manifest = archive / 'archive_manifest.json'
    if manifest.exists():
        return True
    records = []
    for path in sorted(source.rglob('*')):
        if path.is_file() and not path.is_symlink():
            records.append(copy_verified(path, archive / path.relative_to(source)))
    archive.mkdir(parents=True, exist_ok=True)
    atomic_json(manifest, dict(state=case['state'], details=case.get('details', ''), files=records))
    index = Path(destination) / case['series'] / 'run_records_manifest.json'
    entries = json.loads(index.read_text()) if index.exists() else {}
    entries[case['id']] = dict(path=str(archive), state=case['state'], files=records)
    atomic_json(index, entries)
    return True


def archive_runtime(source, destination):
    """Call only after the owning process group has exited."""
    source, destination = Path(source), Path(destination)
    if not source.exists():
        return []
    records = []
    for path in sorted(source.rglob('*')):
        target = destination / path.relative_to(source)
        mode = path.lstat().st_mode
        if stat.S_ISREG(mode):
            records.append(copy_verified(path, target, remove=True))
        elif stat.S_ISLNK(mode):
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.is_symlink():
                target.symlink_to(os.readlink(path))
            if os.readlink(target) != os.readlink(path):
                raise ValueError(f'Symlink differs: {path}')
            path.unlink()
        elif not stat.S_ISDIR(mode):
            records.append(dict(source=str(path), type=stat.filemode(mode), bytes=0))
    destination.mkdir(parents=True, exist_ok=True)
    atomic_json(destination / 'runtime_manifest.json', records)
    shutil.rmtree(source)
    return records
