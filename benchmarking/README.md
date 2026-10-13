# Benchmarking

One shared controller runs benchmark series for `HydrostaticFreeSurfaceModel`
(default) or `NonhydrostaticModel`. Run commands from the repository root.

```text
benchmarking/
├── README.md                 Instructions and series definitions
├── Project.toml              Julia benchmark environment
├── scripts/                  Shared entry points, machine profiles, environment setup
├── src/                      Julia benchmark models; suite planner, worker and reports
├── test/                     Tests of planning, validation, launching and reporting
└── results/
    ├── hydrostatic_free_surface_models/
    └── non_hydrostatic_models/
        └── <machine>/
            ├── plot.md       Combined machine report
            └── <series>/
                ├── plot.md, results.csv, plots
                ├── suite.json
                └── <case>/   Configuration, per-rank results and provenance
```

Both model folders contain the same five machines: `Andi-5070ti`, `fir`, `nibi`,
`rondeau`, and `rorqual`. Machine folders with no accepted measurements contain a
`plot.md` stating that status. Results retain the latest accepted measurement for
each configuration. Source revisions, environment records and original run dates
remain with the cases. Older attempts and controllers are available in Git history.

## Series

Use `--series` with a comma-separated subset; the default selects all ten series.

| Series | Measurement |
|---|---|
| `cpu_mpi_scaling_super_fine` | Strong scaling: 1 rank, then 3, 6, 12, …, one rank per physical CPU core |
| `gpu_scaling_super_fine` | Strong scaling: 1, 2, 4, … GPUs |
| `cpu_resolution` | CPU timing at default, fine and super_fine resolutions |
| `gpu_resolution` | GPU timing at default, fine and super_fine resolutions |
| `cpu_partition_cores_super_fine` | Horizontal MPI partitions on four full CPU nodes |
| `gpu_nsight_scaling_super_fine` | GPU strong scaling with Nsight CUDA/NVTX/MPI profiling |
| `gpu_partition_super_fine` | Horizontal MPI partitions; includes a measured one-GPU baseline |
| `gpu_scaling_super_super_fine` | Strong scaling on the larger grid, starting at four GPUs |
| `gpu_scaling_super_super_super_fine` | Strong scaling on the largest grid, starting at sixteen GPUs |
| `gpu_weak_scaling_super_fine` | Weak scaling: 1, 4, 16, … GPUs; fixed interior cells per GPU |

| Grid | Global resolution (Nx × Ny × Nz) | Δt (simulated seconds) |
|---|---|---:|
| `default` | 360 × 180 × 50 | 60 |
| `fine` | 720 × 360 × 100 | 60 |
| `super_fine` | 1440 × 720 × 200 | 60 |
| `super_super_fine` | 2880 × 1440 × 200 | 30 |
| `super_super_super_fine` | 5760 × 2880 × 200 | 15 |

Standard workloads use a LatitudeLongitudeGrid without bathymetry, Float64,
T/S tracers, TEOS10 buoyancy and traditional spherical Coriolis. Each run uses two
untimed steps followed by five windows of ten steps, with one Julia computation
thread per MPI rank. Partition comparisons record local resolution and actual
resource placement. Weak scaling retains 207,360,000 interior cells per GPU.

Hydrostatic runs use WENOVectorInvariantDefault momentum advection, WENO7 tracer
advection, CATKE, SplitRungeKutta3 and a split-explicit free surface with 30 requested
substeps. CPU runs disable extended free-surface halos; GPU runs enable them.
Record the actual retained substeps in the results.

Nonhydrostatic runs use a rigid lid, WENO7 momentum/tracer advection,
ScalarDiffusivity (ν = 1e-3, κ = 1e-5 m²/s), RungeKutta3 and a
ConjugateGradientPoissonSolver with a LocalFFTPreconditioner by default. They
have no free-surface substeps. Every pressure stage must converge, and the final
true residual is checked independently. Solver pilots and small-grid validation
cases are stored in separate validation series and do not supply production baselines.

Some retained historical series use different grids, thread counts or profiling
scopes. Their configuration records and report labels describe the original
settings. Historical results lacking modern finite-state or placement evidence
are explicitly labeled; their acceptance is limited to complete rank records and
finite timing aggregates. Legacy code has been removed.

## Setup

For a local machine, install Julia 1.10 or newer, an MPI launcher for distributed
runs, CUDA for NVIDIA GPU runs, and Python with Matplotlib for reports. Instantiate
the separate Julia benchmark environment:

```bash
julia --project=benchmarking -e 'using Pkg; Pkg.develop(path="."); Pkg.instantiate()'
```

Machine profiles live in [scripts/configs](scripts/configs/). The local
Andi-5070ti and Rondeau profiles detect the available CPU/GPU capacity. Fir, Nibi and Rorqual profiles describe Slurm capacities, accounts,
wall-time limits, scratch environments and GPU allocation settings. Review these
settings against the resources assigned to your job before submitting.

On Fir, Nibi or Rorqual, prepare an isolated scratch environment on the login node:

```bash
bash benchmarking/scripts/env/setup.sh rorqual
```

The shared setup loads the cluster modules, develops this checkout and the
benchmark package into `/scratch/$USER/oceananigans_benchmark_environments/<machine>`,
and selects the system OpenMPI library. The MPI hook resets `OPAL_PREFIX` after
NetCDF/CUDA dependencies are loaded. Cluster preferences stay outside the root
package project. Submit compute work through Slurm; login-node GPU visibility
does not describe the compute nodes.

## Plan and run

A study directory contains one folder per selected series and a machine `plot.md`.
Use a fresh scratch directory for each repeat study. `--plan` records settings
and immutable source/environment snapshots without running compute jobs.
Omitting `--output` creates a unique scratch study and publishes accepted cases
to the matching model/machine results folder. Profiler captures use a separate
directory for each study.

```bash
python3 benchmarking/scripts/benchmark_suite.py \
  --config benchmarking/scripts/configs/rorqual.json \
  --model HydrostaticFreeSurfaceModel \
  --output /scratch/$USER/benchmark_studies/2026-10-13/rorqual \
  --series cpu_resolution,gpu_scaling_super_fine --plan
```

Resume that plan to submit its remaining cases. `--watch` refreshes scheduler
states and reports until all selected cases reach a terminal state. Slurm jobs
also submit a reporting finalizer using the captured source snapshot.

```bash
python3 benchmarking/scripts/benchmark_suite.py \
  --output /scratch/$USER/benchmark_studies/2026-10-13/rorqual \
  --series cpu_resolution,gpu_scaling_super_fine --resume --watch
```

For a fresh nonhydrostatic study, submit directly:

```bash
python3 benchmarking/scripts/benchmark_suite.py \
  --config benchmarking/scripts/configs/rorqual.json \
  --model NonhydrostaticModel \
  --output /scratch/$USER/benchmark_studies/2026-10-13-nh/rorqual \
  --series cpu_resolution --submit --watch
```

For local execution inside assigned resources, use `--run` with a local profile.
Limit planning/execution with `--max-cpu-cores` or `--max-gpus` when appropriate.
`--refresh` regenerates existing study reports; `--revalidate` repeats artifact
checks. `--resume` never resubmits live jobs. Existing series require an explicit
resume/refresh or a fresh study directory.

## Publish accepted results

Publish from a completed scratch study into the appropriate model/machine folder:

```bash
python3 benchmarking/scripts/benchmark_suite.py \
  --output /scratch/$USER/benchmark_studies/2026-10-13-nh/rorqual \
  --series cpu_resolution --refresh \
  --publish benchmarking/results/non_hydrostatic_models/rorqual
```

`--publish` copies only completed, accepted cases. Failed or pending reruns leave
previous accepted cases intact, and older jobs cannot overwrite a newer accepted
measurement. Raw process logs and execution scripts remain in the scratch study;
published cases retain configurations, rank measurements, profile summaries and
provenance. Local Nsight capture/database files are ignored by Git. Their recorded
locations, sizes and checksums accompany the profile summaries.

Curated results are read-only inputs to new studies. Their machine `plot.md`
combines series reports and links to the actual case settings. `--commit` records
study/publication artifacts when their directories are inside a Git repository
with a configured identity and a clean index. With `--publish`, `--commit`
commits the curated results; the scratch study can stay outside the repository.

Timing validation checks complete rank results, finite fields, recorded model and
local/global grid settings, distinct computation resources, timing windows and
MPI/CUDA communication. Profile validation also checks capture hashes and kernel
summaries. Fastest and median seconds per step are the maximum rank statistics.
Strong efficiency is baseline time × baseline ranks / (time × ranks); weak
efficiency is baseline time / time. A missing or incompatible measured baseline
has no efficiency estimate. Profile timings remain separate from unprofiled timings.

For a cross-model comparison, add `--compare-with` pointing at the other model's
machine directory and `--comparison-report` pointing at a report inside the current
series folder. Comparisons use matched grids, partitions, resource counts and timing
protocols, and retain separate baselines for the two models.

## Other entry points and tests

[scripts/run_benchmarks.jl](scripts/run_benchmarks.jl) supports configurable
hydrostatic sweeps, simulation output, I/O and read benchmarks used by benchmark
CI. It uses the same Julia benchmark package under `src/`.
[scripts/generate_bathymetry.jl](scripts/generate_bathymetry.jl) prepares the optional
bathymetry datasets for those runs and requires NumericalEarth.jl.

Run the controller tests without compute allocations:

```bash
python3 -m unittest discover -s benchmarking/test -v
```

The tests exercise geometry planning, launch scripts, resource placement,
validation failures, restart behavior, source snapshots, report baselines and the
shared layout for both models.
