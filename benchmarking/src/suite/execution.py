"""Versioned execution adapters; independent of servers and launch backends."""
import hashlib
import json
from pathlib import Path
import shutil

ADAPTER_ROOT = Path(__file__).with_name('execution')
TIMING_CONTRACT = 'oceananigans/timestep_window/v1'


def adapter_directory(server):
    return Path(server.get('dagger_adapter') or ADAPTER_ROOT / 'dagger') if server['execution_mode'] == 'dagger' else ADAPTER_ROOT / 'baseline'


def describe_adapter(server):
    directory = adapter_directory(server).resolve()
    manifest = json.loads((directory / 'adapter.json').read_text())
    if manifest.get('api_version') != 1 or manifest.get('mode') != server['execution_mode']:
        raise ValueError('Execution adapter API/mode is incompatible')
    if any(not isinstance(manifest.get(k), str) or not manifest[k] for k in ('id', 'version', 'timing_contract')):
        raise ValueError('Execution adapter requires id, version and timing_contract')
    if not (directory / 'adapter.jl').is_file():
        raise ValueError('Execution adapter requires adapter.jl')
    checksum = hashlib.sha256()
    for path in sorted(directory.rglob('*')):
        if path.is_symlink():
            raise ValueError('Execution adapter sources must not be symlinks')
        if path.is_file() and '__pycache__' not in path.parts:
            checksum.update(path.relative_to(directory).as_posix().encode() + b'\0')
            checksum.update(path.read_bytes())
    options = server.get('dagger_options', {}) if server['execution_mode'] == 'dagger' else {}
    if not isinstance(options, dict):
        raise ValueError('Dagger adapter options must be a JSON object')
    return dict(manifest, source_sha256=checksum.hexdigest(), options=options)


def snapshot_adapter(metadata, server):
    source = adapter_directory(server)
    descriptor = describe_adapter(server)
    if descriptor != server['execution_adapter']:
        raise ValueError('Execution adapter changed while preparing the study')
    target = metadata / 'src/suite/adapter'
    shutil.copytree(source, target, ignore=shutil.ignore_patterns('__pycache__'))
    (metadata / 'execution_adapter.json').write_text(json.dumps(descriptor, indent=2) + '\n')


def comparable_configuration(config):
    """Adapter identity may differ; workload and timing meaning must match."""
    result = {k: v for k, v in config.items() if k not in ('execution_mode', 'execution_adapter')}
    result['timing_contract'] = config.get('execution_adapter', {}).get('timing_contract', TIMING_CONTRACT)
    return result
