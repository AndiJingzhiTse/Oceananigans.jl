"""Server-independent definitions for the seven standard benchmark series."""
import math

GRIDS = {'default': [360, 180, 50], 'fine': [720, 360, 100], 'super_fine': [1440, 720, 200]}
SERIES = ('cpu_mpi_scaling_super_fine', 'gpu_scaling_super_fine', 'cpu_resolution',
          'gpu_resolution', 'cpu_partition_cores_super_fine',
          'gpu_nsight_scaling_super_fine', 'gpu_partition_super_fine')


def doubling(maximum, cpu=False):
    values, count = ([1], 3) if cpu else ([], 1)
    while count <= maximum:
        values.append(count)
        count *= 2
    return values


def balanced_sizes(length, parts):
    quotient, remainder = divmod(length, parts)
    return [quotient + (i < remainder) for i in range(parts)]


def partition_for(ranks, grid, extended=False):
    minimum = 23 if extended and ranks > 1 else 7
    options = []
    for x in range(1, ranks + 1):
        if ranks % x:
            continue
        y = ranks // x
        if grid[0] // x < minimum or grid[1] // y < minimum:
            continue
        xs, ys = balanced_sizes(grid[0], x), balanced_sizes(grid[1], y)
        imbalance = max(xs) * max(ys) / (min(xs) * min(ys))
        options.append((imbalance, abs(math.log((grid[0] / x) / (grid[1] / y))), x, y))
    if not options:
        raise ValueError(f'{ranks} ranks have no horizontal partition with at least {minimum} local cells per direction')
    _, _, x, y = min(options)
    return [x, y, 1]


def configuration(series, ranks, grid_name='super_fine', partition=None):
    grid = GRIDS[grid_name]
    gpu = series.startswith('gpu_')
    partition = partition or partition_for(ranks, grid, extended=gpu)
    if len(partition) != 3 or math.prod(partition) != ranks or partition[2] != 1 or min(partition) < 1:
        raise ValueError('Expected a horizontal partition with exactly one part per MPI rank')
    xs, ys = balanced_sizes(grid[0], partition[0]), balanced_sizes(grid[1], partition[1])
    minimum = 23 if gpu and ranks > 1 else 7
    if min(xs) < minimum or min(ys) < minimum:
        raise ValueError(f'Partition {partition} has fewer than {minimum} local cells per horizontal direction')
    return dict(series=series, device='GPU' if gpu else 'CPU', ranks=ranks,
                threads_per_rank=1, grid_name=grid_name, global_resolution=list(grid),
                grid_type='LatitudeLongitudeGrid', partition=partition, x_sizes=xs, y_sizes=ys,
                float_type='Float64', momentum_advection='WENOVectorInvariantDefault',
                tracer_advection='WENO7', closure='CATKE', tracers=['T', 'S'],
                timestepper='SplitRungeKutta3', dt=60, free_surface_substeps=30,
                extend_free_surface_halos=gpu, warmup_steps=2, samples=5, time_steps=10,
                profile=series == 'gpu_nsight_scaling_super_fine')


def build_plan(server, selected=SERIES):
    cases = []
    for series in selected:
        gpu = series.startswith('gpu_')
        maximum = server['max_gpus' if gpu else 'max_cpu_cores']
        if series.endswith('resolution'):
            specs = [(1, name, None) for name in GRIDS]
        elif series == 'cpu_partition_cores_super_fine':
            specs = [(192, 'super_fine', [x, 192 // x, 1])
                     for x in range(192, 0, -1) if 192 % x == 0]
        elif series == 'gpu_partition_super_fine':
            specs = [(n, 'super_fine', p) for n, partitions in
                     ((2, ([2, 1, 1], [1, 2, 1])), (4, ([4, 1, 1], [2, 2, 1], [1, 4, 1])))
                     for p in partitions]
        else:
            specs = [(n, 'super_fine', None) for n in doubling(maximum, cpu=not gpu)]
            # Include the next doubling as an explicit resource boundary.
            last = specs[-1][0] if specs else 0
            next_count = 3 if not gpu and last == 1 else max(1, last * 2)
            specs.append((next_count, 'super_fine', None))
        for ranks, grid_name, partition in specs:
            label = ('x'.join(map(str, partition)) if partition else
                     grid_name if series.endswith('resolution') else f'{ranks}_ranks')
            case = dict(id=f'{series}/{label}', series=series, ranks=ranks,
                        grid_name=grid_name, partition=partition, state='PLANNED', details='', job_id='')
            try:
                case['configuration'] = configuration(series, ranks, grid_name, partition)
                case['partition'] = case['configuration']['partition']
                if ranks > maximum:
                    case.update(state='RESOURCE_LIMIT', details=f'Requires {ranks}; configured capacity is {maximum}')
            except ValueError as error:
                case.update(state='GEOMETRY_LIMIT', details=str(error))
            cases.append(case)
            if case['state'] == 'GEOMETRY_LIMIT' and 'scaling' in series:
                break
    return cases


def allocation_groups(cases):
    """Keep partition comparisons on the same allocated resource set."""
    groups = {}
    for case in cases:
        if case['state'] != 'PLANNED':
            continue
        key = f"{case['series']}/{case['ranks']}_ranks" if 'partition' in case['series'] else case['id']
        groups.setdefault(key, []).append(case)
    return groups
