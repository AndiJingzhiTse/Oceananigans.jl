"""Server-independent definitions for the standard benchmark series."""
import math

GRIDS = {'default': [360, 180, 50], 'fine': [720, 360, 100], 'super_fine': [1440, 720, 200],
         'super_super_fine': [2880, 1440, 200], 'super_super_super_fine': [5760, 2880, 200]}
RESOLUTION_GRIDS = ('default', 'fine', 'super_fine')
GPU_BASELINES = {'gpu_scaling_super_super_fine': 4, 'gpu_scaling_super_super_super_fine': 16}
MODEL_FOLDERS = {'HydrostaticFreeSurfaceModel': 'hydrostatic_free_surface_models',
                 'NonhydrostaticModel': 'non_hydrostatic_free_surface_models'}
SERIES = ('cpu_mpi_scaling_super_fine', 'gpu_scaling_super_fine', 'cpu_resolution',
          'gpu_resolution', 'cpu_partition_cores_super_fine',
          'gpu_nsight_scaling_super_fine', 'gpu_partition_super_fine',
          'gpu_scaling_super_super_fine', 'gpu_scaling_super_super_super_fine',
          'gpu_weak_scaling_super_fine')


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


def configuration(series, ranks, grid_name='super_fine', partition=None, global_resolution=None,
                  model_type='HydrostaticFreeSurfaceModel'):
    if model_type not in MODEL_FOLDERS:
        raise ValueError('Unknown benchmark model: ' + model_type)
    grid = global_resolution if global_resolution is not None else GRIDS[grid_name]
    gpu = series.startswith('gpu_')
    partition = partition or partition_for(ranks, grid, extended=gpu)
    if len(partition) != 3 or math.prod(partition) != ranks or partition[2] != 1 or min(partition) < 1:
        raise ValueError('Expected a horizontal partition with exactly one part per MPI rank')
    xs, ys = balanced_sizes(grid[0], partition[0]), balanced_sizes(grid[1], partition[1])
    minimum = 23 if gpu and ranks > 1 else 7
    if min(xs) < minimum or min(ys) < minimum:
        raise ValueError(f'Partition {partition} has fewer than {minimum} local cells per horizontal direction')
    hydrostatic = model_type == 'HydrostaticFreeSurfaceModel'
    return dict(series=series, model_type=model_type, device='GPU' if gpu else 'CPU', ranks=ranks,
                threads_per_rank=1, grid_name=grid_name, global_resolution=list(grid),
                grid_type='LatitudeLongitudeGrid', partition=partition, x_sizes=xs, y_sizes=ys,
                float_type='Float64', momentum_advection='WENOVectorInvariantDefault' if hydrostatic else 'WENO7',
                tracer_advection='WENO7', closure='CATKE' if hydrostatic else 'ScalarDiffusivity', tracers=['T', 'S'],
                viscosity=None if hydrostatic else 1e-3, diffusivity=None if hydrostatic else 1e-5,
                coriolis='HydrostaticSphericalCoriolis', buoyancy='SeawaterBuoyancy(TEOS10)',
                timestepper='SplitRungeKutta3' if hydrostatic else 'RungeKutta3',
                free_surface='SplitExplicitFreeSurface' if hydrostatic else 'RigidLid',
                pressure_solver=None if hydrostatic else 'ConjugateGradientPoissonSolver',
                pressure_preconditioner=None if hydrostatic else 'DiagonallyDominantPreconditioner',
                pressure_max_iterations=None if hydrostatic else 5000,
                pressure_reltol=None if hydrostatic else math.sqrt(2.220446049250313e-16),
                pressure_abstol=None if hydrostatic else math.sqrt(2.220446049250313e-16),
                pressure_diagnostics=False, initial_condition_seed=None if hydrostatic else 1234,
                dt=60 * min(1, 1440 / grid[0]), free_surface_substeps=30 if hydrostatic else None,
                extend_free_surface_halos=gpu if hydrostatic else False,
                warmup_steps=2, samples=5, time_steps=10,
                profile=series == 'gpu_nsight_scaling_super_fine',
                scaling_type='weak' if series == 'gpu_weak_scaling_super_fine' else
                             'strong' if 'scaling' in series else 'comparison',
                baseline_ranks=GPU_BASELINES.get(series, 1))


def build_plan(server, selected=SERIES):
    cases = []
    for series in selected:
        gpu = series.startswith('gpu_')
        maximum = server['max_gpus' if gpu else 'max_cpu_cores']
        if series.endswith('resolution'):
            specs = [(1, name, None) for name in RESOLUTION_GRIDS]
        elif series == 'cpu_partition_cores_super_fine':
            specs = [(192, 'super_fine', [x, 192 // x, 1])
                     for x in range(192, 0, -1) if 192 % x == 0]
        elif series == 'gpu_partition_super_fine':
            specs = [(n, 'super_fine', [x, n // x, 1]) for n in (1, 2, 4, 8, 16, 32, 64)
                     for x in range(n, 0, -1) if n % x == 0]
        elif series == 'gpu_weak_scaling_super_fine':
            counts = doubling(maximum)[::2]
            counts.append(counts[-1] * 4 if counts else 1)
            specs = [(n, 'super_fine' if n == 1 else f'weak_{n}_ranks',
                      [math.isqrt(n), math.isqrt(n), 1]) for n in counts]
        else:
            grid_name = series.removeprefix('gpu_scaling_') if series in GPU_BASELINES else 'super_fine'
            baseline = GPU_BASELINES.get(series, 1)
            specs = [(n, grid_name, None) for n in doubling(maximum, cpu=not gpu) if n >= baseline]
            # Include the next doubling as an explicit resource boundary.
            last = specs[-1][0] if specs else 0
            next_count = 3 if not gpu and last == 1 else max(baseline, last * 2)
            specs.append((next_count, grid_name, None))
        for ranks, grid_name, partition in specs:
            label = (f'{ranks}_ranks' if series == 'gpu_weak_scaling_super_fine' else
                     'x'.join(map(str, partition)) if partition else
                     grid_name if series.endswith('resolution') else f'{ranks}_ranks')
            case = dict(id=f'{series}/{label}', series=series, ranks=ranks,
                        grid_name=grid_name, partition=partition, state='PLANNED', details='', job_id='')
            try:
                weak_grid = ([1440 * math.isqrt(ranks), 720 * math.isqrt(ranks), 200]
                             if series == 'gpu_weak_scaling_super_fine' else None)
                if series.startswith('gpu_scaling_') and server.get('gpu_scaling_partition') == 'x':
                    partition = [ranks, 1, 1]
                case['configuration'] = configuration(series, ranks, grid_name, partition, weak_grid,
                                                      server.get('model_type', 'HydrostaticFreeSurfaceModel'))
                if server.get('model_type') == 'NonhydrostaticModel':
                    for key in ('pressure_preconditioner', 'pressure_max_iterations', 'pressure_diagnostics'):
                        if key in server:
                            case['configuration'][key] = server[key]
                case['partition'] = case['configuration']['partition']
                if ranks > maximum:
                    case.update(state='RESOURCE_LIMIT', details=f'Requires {ranks}; configured capacity is {maximum}')
            except ValueError as error:
                case.update(state='GEOMETRY_LIMIT', details=str(error))
            cases.append(case)
            if case['state'] == 'GEOMETRY_LIMIT' and 'scaling' in series:
                break
    return cases


def allocation_groups(cases, separate_partitions=False):
    """Keep partition comparisons on the same allocated resource set."""
    groups = {}
    for case in cases:
        if case['state'] != 'PLANNED':
            continue
        key = (f"{case['series']}/{case['ranks']}_ranks"
               if 'partition' in case['series'] and not separate_partitions else case['id'])
        groups.setdefault(key, []).append(case)
    return groups
