"""Read bounded, model-independent workloads from benchmarking/server/."""
import json
from pathlib import Path


SERVER_ROOT = Path(__file__).resolve().parents[2] / 'server'
GPU_SERIES = ('gpu_resolution', 'gpu_scaling_default', 'gpu_scaling_fine',
              'gpu_nsight_scaling_default', 'gpu_nsight_scaling_fine',
              'gpu_partition_fine', 'gpu_weak_scaling')


def load_series(path):
    data = json.loads(Path(path).read_text())
    if data.get('schema_version') != 1:
        raise ValueError('Unsupported server series schema')
    if data.get('models') != ['HydrostaticFreeSurfaceModel', 'NonhydrostaticModel']:
        raise ValueError('Server series must support both benchmark models')
    if data.get('execution_modes') != ['baseline', 'dagger']:
        raise ValueError('Server series must support baseline and dagger')
    definitions = data.get('series', {})
    if not definitions or set(definitions) - set(GPU_SERIES):
        raise ValueError('Server series must be a nonempty subset of supported GPU series')
    kinds = dict(zip(GPU_SERIES, ('resolution', 'strong_scaling', 'strong_scaling',
                                'profiled_scaling', 'profiled_scaling', 'partition', 'weak_scaling')))
    grids = {'default', 'fine', 'super_fine'}
    for name, spec in definitions.items():
        if spec.get('kind') != kinds[name]:
            raise ValueError(f'Invalid kind for {name}')
        if spec['kind'] == 'resolution':
            if (not spec.get('grids') or not set(spec['grids']) <= grids or
                    len(spec['grids']) != len(set(spec['grids'])) or spec.get('gpus') != [1]):
                raise ValueError('Resolution series requires named grids on one GPU')
        elif spec['kind'] == 'weak_scaling':
            if not spec.get('cases'):
                raise ValueError('Weak scaling requires explicit grid/GPU cases')
            validate_counts([case.get('gpus') for case in spec['cases']])
            for case in spec['cases']:
                if case.get('grid') not in grids:
                    raise ValueError('Unknown weak-scaling grid')
                validate_counts([case.get('gpus')])
                validate_partition(case.get('partition'), case['gpus'])
        else:
            if spec.get('grid') not in grids:
                raise ValueError(f'Unknown grid for {name}')
            if spec['kind'] == 'partition':
                if not spec.get('partitions'):
                    raise ValueError('Partition series requires explicit partitions')
                for partition in spec['partitions']:
                    validate_partition(partition)
                if len(spec['partitions']) != len({tuple(p) for p in spec['partitions']}):
                    raise ValueError('Partitions must be unique')
            else:
                validate_counts(spec.get('gpus'))
    return definitions


def validate_counts(counts):
    if (not isinstance(counts, list) or not counts or
            any(type(n) is not int or n < 1 for n in counts) or
            len(counts) != len(set(counts))):
        raise ValueError('GPU counts must be unique positive integers')


def validate_partition(partition, ranks=None):
    if (not isinstance(partition, list) or len(partition) != 3 or
            any(type(n) is not int or n < 1 for n in partition) or partition[2] != 1 or
            (ranks is not None and partition[0] * partition[1] != ranks)):
        raise ValueError('Expected a horizontal partition matching the GPU count')


def series_definitions(server):
    # Loaded definitions are embedded in suite.json so queued jobs and resumed
    # studies keep their original workload even after the server files change.
    if server.get('series_definitions') is not None:
        return server['series_definitions']
    path = SERVER_ROOT / server.get('machine', '') / 'series.json'
    return load_series(path) if path.is_file() else {}
