# Benchmarking

One shared controller runs benchmark series for `HydrostaticFreeSurfaceModel`
(default) or `NonhydrostaticModel`. Run commands from the repository root.

## Folder structure

Shared code and instructions live at the top level. Model-specific measurements
live under `results/`.

```text
benchmarking/
├── .gitignore
├── README.md                          Instructions and series definitions
├── Project.toml                       Benchmark package and dependency requirements
├── Manifest.toml                      Resolved local dependency versions, when present
├── LocalPreferences.toml              Local CUDA/MPI preferences, when present
├── scripts/
│   ├── benchmark_suite.py             Shared controller for both model types
│   ├── run_benchmarks.jl              Configurable hydrostatic and I/O benchmarks
│   ├── generate_bathymetry.jl         Optional bathymetry preparation
│   ├── configs/
│   │   ├── Andi-5070ti.json
│   │   ├── fir.json
│   │   ├── nibi.json
│   │   ├── rondeau.json
│   │   └── rorqual.json
│   └── env/
│       ├── setup.sh                   Cluster environment setup entry point
│       ├── setup_environment.jl       Creates the isolated Julia environment
│       ├── modules.sh                 Cluster software modules
│       └── drac_mpi.jl                System OpenMPI initialization
├── src/
│   ├── OceananigansBenchmarks.jl      Julia benchmark package entry point
│   ├── earth_ocean.jl                 Benchmark model construction
│   ├── metadata.jl
│   ├── result.jl
│   ├── timestepping.jl
│   ├── utils.jl
│   └── suite/
│       ├── plan.py                    Series configurations and resource planning
│       ├── rank.sh                    MPI rank launcher and profiler capture
│       ├── worker.jl                  Shared model validation and timing worker
│       ├── report.py                  Validation, timing reports and plots
│       └── catalog.py                 Result publication and machine reports
├── test/
│   └── test_suite.py
└── results/                           Curated measurements; layout below
```

`Project.toml` defines the benchmark environment selected by
`julia --project=benchmarking`. `Manifest.toml` records the resolved dependency
versions, and `LocalPreferences.toml` configures the local CUDA/MPI installation.
The optional generated bathymetry files go into `data/bathymetry/` and are ignored
by Git.

### Results by model and machine

```text
results/
├── hydrostatic_free_surface_models/
│   ├── Andi-5070ti/
│   ├── fir/
│   ├── nibi/
│   ├── rondeau/
│   └── rorqual/
└── non_hydrostatic_models/
    ├── Andi-5070ti/
    ├── fir/
    ├── nibi/
    ├── rondeau/
    └── rorqual/
```

Each machine uses the following layout. `<series>` is a series name such as
`gpu_scaling_super_fine`; `<case>` is a configuration such as `4_ranks`, `default`,
or `2x2x1`. Optional evidence files depend on what the original run recorded.

```text
<machine>/
├── plot.md                            Combined report for this machine and model
└── <series>/                          One folder for each available series
    ├── plot.md                        Series report
    ├── results.csv                    Timing and efficiency table
    ├── <series>.svg                   Timing/scaling plot
    ├── <series>_kernels.svg           Kernel shares, when available
    ├── suite.json                     Accepted cases and their measurement metadata
    └── <case>/                        One folder per retained configuration
        ├── configuration.json         Model, grid, partition and numerical settings
        ├── configuration.md           Readable settings and validation limits
        ├── results.json               Original per-rank measurements
        ├── layout.json                Rank placement, when available
        ├── rank_<n>/                  Per-rank profiler summaries, when available
        └── provenance/
            ├── record.json            Original run, measurement date and result hash
            ├── revision.txt           Source revision, when recorded
            ├── Project.toml           Original environment requirements, when saved
            ├── Manifest.toml          Original resolved dependencies, when saved
            ├── LocalPreferences.toml  Original machine preferences, when saved
            └── source.tar.gz          Source snapshot for newly published cases
```

Historical placement records may instead be named `cpu_layout.json` or
`gpu_layout.json`. Additional profile summaries, capture references and execution
metadata remain alongside the case measurements. Raw Nsight captures and SQLite
databases are ignored by Git.

Scratch studies follow the same machine → series → case hierarchy, with a
`run_metadata/` folder inside each series containing executable source snapshots
and environment records. Allocation scripts and execution logs stay in the scratch
study; publication copies accepted measurements and provenance into `results/`.

Both model folders contain the same five machines: `Andi-5070ti`, `fir`, `nibi`,
`rondeau`, and `rorqual`. Machine folders with no accepted measurements contain a
`plot.md` stating that status. Results retain the latest accepted measurement for
each configuration. Source revisions, environment records and original run dates
remain with the cases. Older attempts and controllers are available in Git history.

## Series

Use `--series` with a comma-separated subset. The standard default selects the
ten series below; Rondeau NonhydrostaticModel uses the smaller plan described after the table.

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

Rondeau's GPU-only NonhydrostaticModel plan (also used by the paired Dagger runner):

| Series | Configuration |
|---|---|
| `gpu_weak_scaling` (first) | 360 × 180 × 50 / 1 GPU; 720 × 360 × 100 / 2 GPUs; 1440 × 720 × 200 / 4 GPUs |
| `gpu_scaling_fine` | 720 × 360 × 100; 1, 2, 4 GPUs |
| `gpu_nsight_scaling_default` | 360 × 180 × 50; 1, 2, 4 GPUs, profiled |
| `gpu_resolution` | 360 × 180 × 50, 720 × 360 × 100, 1440 × 720 × 200; 1 GPU |

The requested `gpu_weak_scaling` sequence increases cells per GPU in the ratio
1:4:16, rather than holding them fixed. Its timing reference scales linearly with
cells per GPU; its reported efficiency is `(baseline time / time) ×
(cells per GPU / baseline cells per GPU)`. This reference does not account for
changes in pressure-solver iteration count. Each variant runs one case at a time;
baseline and Dagger alternate order between cases. CPU benchmarks were cancelled
and removed from this study. The Rondeau plan stops at
the listed sizes, overriding the general extension guidance below.

Each benchmark series must be performed to the maximum feasible scale for the
available resources. This applies to both model types, CPU and GPU runs, and
profiled series. For scaling studies, include the largest valid resource count
in the series' progression that the available CPUs or GPUs support. For example,
with 300 GPUs available, the final GPU scaling case should use 256 GPUs.

For resolution series, keep increasing the grid resolution until the next larger
grid cannot run because system memory or GPU VRAM is insufficient. Retain the
largest completed, validated resolution. The built-in `default`, `fine`, and
`super_fine` cases are starting points; extend the resolution plan when they still
fit in memory. The current planner does not automatically search for the memory
limit.

Check the planned cases before submission and extend the series plan or update
the machine resource limits as needed to reach these scales. Record the highest
completed resource count or resolution and the observed reason further scaling
could not complete. Preserve failed attempts and memory-limit evidence in the
scratch study; only completed, validated measurements enter curated results.

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

### Matched baseline and Dagger runs

Raw Nsight captures belong in the results tree, under each variant's
`<series>/raw_profiles/`. Captures stay on disk and are
excluded from Git; `profile_manifest.json` records relocated paths, sizes and
SHA-256 checksums. Captures from failed runs remain diagnostic evidence and
are not accepted timing results.

The paired controller archives closed case files, including CPU logs and
failure evidence, in `<variant>/<series>/run_records/<case>/`. Its versioned
`run_records_manifest.json` records file checksums. Future processes use a
case-specific `.runtime/` directory in the local scratch study for `TMPDIR`,
`TMP`, `TEMP` and OpenMPI session files. On exit, leftover runtime files are
verified, archived into the case's run records, and removed from `.runtime/`.
An active MPI session must finish before its temporary files are moved.
Short symlinks in `~/.ocean-tmp/` point into these directories to keep MPI
Unix socket names within the operating system's pathname limit.

Standard controller launches also default profiler output and temporary
storage to the results tree instead of `/tmp`. Explicit machine environment
settings can override these paths.

`--execution-mode baseline` (the default) calls the timestep window directly.
`--execution-mode dagger` submits the same window as one `Dagger.@spawn` task
and fetches its completion. The task stays on the current MPI process and its
sole Julia computation thread; CUDA runs explicitly select the assigned device
and synchronize the task's stream before completion. This measures wrapping
overhead with the existing Oceananigans MPI decomposition. It does not expose
parallelism inside a timestep to Dagger.

Install Dagger in an isolated environment alongside the local Oceananigans and
OceananigansBenchmarks packages. Use that same environment for both variants;
the baseline does not import Dagger. CPU rank launchers hide CUDA devices before
Julia starts, so CPU Dagger initialization cannot allocate GPU contexts. The paired
local runner uses the machine's nonhydrostatic plan and alternates variant order:

```bash
python3 benchmarking/scripts/compare_dagger.py \
  --config benchmarking/scripts/configs/rondeau.json \
  --project /absolute/path/to/isolated/environment \
  --study /local_scratch/$USER/benchmark_studies/nonhydrostatic_dagger/rondeau \
  --publish benchmarking/results/non_hydrostatic_models/rondeau
```

Accepted records go into `baseline/<series>/` and `dagger/<series>/`.
`comparison.md` and `comparison.csv` include every series and all outcomes;
ratios and plots require completed pairs with identical configurations except
for execution mode. Speedup is baseline time divided by Dagger time, with an
equal-time reference of 1. Nsight runs remain separate from unprofiled timings.
Raw failures and resource limits stay in scratch and are summarized in each
variant's `status.json`. Repeating the command resumes only unstarted cases;
`--refresh` regenerates reports without running cases. `--plan` prepares all
cases without executing. Optional `--commit` commits the designated result
tree after each completed outcome and refuses an already populated Git index.

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
