# Benchmarking

One shared controller runs `HydrostaticFreeSurfaceModel` and `NonhydrostaticModel`.
Server files define the workloads; model construction, execution, validation and
reporting stay in shared code. Run commands from the repository root.

[Workflow requirements](requirements.md) define the requested common local/Slurm
entry point, selectable model/mode combinations and replaceable Dagger adapter.
The shared workflow implements these selections through backend and execution adapters.

## File structure

```text
benchmarking/
├── benchmarking_guide.md               Commands, workloads and result layout
├── requirements.md                     Shared workflow and integration contract
├── Project.toml                         Julia benchmark package dependencies
├── server/
│   ├── server_benchmark_plans.md        Server plans and model/mode selections
│   ├── rondeau/
│   │   ├── config.json                  Resources, launcher and environment
│   │   ├── series.json                  Exact grids, GPU counts and partitions
│   │   ├── rondeau_gpu_benchmarks.md    Human-readable server plan
│   │   └── history/                     Superseded study instructions
│   ├── nibi/                            config.json, series.json, nibi_gpu_benchmarks.md
│   ├── rorqual/                         config.json, series.json, rorqual_gpu_benchmarks.md
│   ├── fir/                             config.json, series.json, fir_gpu_benchmarks.md
│   └── Andi-5070ti/                     config.json, andi_5070ti_local_profile.md
├── scripts/
│   ├── benchmark_suite.py               Shared local/Slurm controller
│   ├── compare_dagger.py                Compatibility wrapper for the shared workflow
│   ├── run_benchmarks.jl                Configurable model and I/O benchmarks
│   ├── generate_bathymetry.jl           Optional bathymetry preparation
│   └── env/                            Shared Julia/MPI/module setup
├── src/
│   ├── OceananigansBenchmarks.jl
│   ├── earth_ocean.jl                   Shared benchmark model construction
│   └── suite/
│       ├── workflow.py                 Persisted model/mode studies and comparisons
│       ├── backends.py                 Local and Slurm allocation/launch adapters
│       ├── execution.py                Execution adapter discovery and snapshots
│       ├── execution/                  Direct and Dagger Julia adapters
│       ├── servers.py                  Server workload loader and schema checks
│       ├── plan.py                     Common case and resource planning
│       ├── rank.sh                     MPI launcher and profiler capture
│       ├── worker.jl                   Model validation and timestep timing
│       ├── report.py                   Timing/efficiency reports and plots
│       ├── variants.py                 Matched baseline/Dagger comparisons
│       ├── storage.py                  Verified evidence archival
│       └── catalog.py                  Validated result publication
├── test/                               Controller/planner regression tests
└── results/
    ├── hydrostatic_free_surface_models/
    │   └── <server>/
    │       ├── <server>_hydrostatic_results_guide.md
    │       ├── baseline/
    │       │   ├── <server>_hydrostatic_baseline_records.md
    │       │   └── <series>/<case>/
    │       ├── dagger/
    │       │   ├── <server>_hydrostatic_dagger_records.md
    │       │   └── <series>/<case>/
    │       ├── comparison.md            Generated after matched measurements
    │       ├── comparison.csv           Generated all-outcome comparison
    │       └── comparisons/             Generated timing and speedup plots
    └── non_hydrostatic_models/
        └── <server>/                    Same baseline/Dagger layout
```

`server/` stores configuration and series definitions. Scientific measurements
remain in `results/<model_family>/<server>/`. Both model families retain the
five existing machines, including the local `Andi-5070ti` results. Historical
series directly inside a results server folder keep their original locations
and provenance; they are not automatically relabeled as runs of the new plan.

Active studies, isolated environments and temporary files belong under the sole
checkout's `.runtime/` directory. Set `TMPDIR`, `TMP`, `TEMP` and OpenMPI's
`OMPI_MCA_orte_tmpdir_base` there before setup, tests or execution. Never use
`/tmp`, `/var/tmp` or `/local_scratch`. Short `~/.ocean-tmp/` aliases may resolve
into project-local runtime directories for MPI socket pathname limits.

## Server GPU series

The authoritative files are [server/rondeau/series.json](server/rondeau/series.json),
[server/nibi/series.json](server/nibi/series.json),
[server/rorqual/series.json](server/rorqual/series.json) and
[server/fir/series.json](server/fir/series.json).
Their definitions apply identically to both model types and both execution modes.
CPU series and ensembles are excluded from these server plans.

| Series | Rondeau | Nibi, Rorqual, Fir |
|---|---|---|
| `gpu_resolution` | 1 GPU: default, fine | 1 GPU: default, fine, super_fine |
| `gpu_scaling_default` | default: 1, 2, 4 GPUs | default: 1, 2, 4, 8, 16 GPUs |
| `gpu_scaling_fine` | fine: 1, 2, 4 GPUs | fine: 1, 2, 4, 8, 16 GPUs |
| `gpu_nsight_scaling_default` | default: 1, 2, 4 GPUs | default: 1, 2, 4, 8, 16 GPUs |
| `gpu_nsight_scaling_fine` | fine: 1, 2, 4 GPUs | fine: 1, 2, 4, 8, 16 GPUs |
| `gpu_partition_fine` | Excluded | fine: four explicit partitions below |
| `gpu_weak_scaling` | default / 1 GPU; fine / 4 GPUs | default / 1 GPU; fine / 4 GPUs; super_fine / 16 GPUs |

Rondeau has no partition benchmark series.

Nibi, Rorqual and Fir partitions: **16 × 1 × 1, 8 × 2 × 1, 4 × 4 × 1,
2 × 8 × 1**.

Other scaling cases choose a balanced horizontal partition with one rank per GPU.
Weak cases use 1 × 1 × 1, 2 × 2 × 1 and 4 × 4 × 1 respectively.
The listed cases are exact bounds: no automatic extension or additional
larger-grid series. Lower resource limits mark unavailable cases `RESOURCE_LIMIT`
without changing the prescribed GPU counts or dropping configurations.

| Grid | Global resolution (Nx × Ny × Nz) | Δt (simulated seconds) |
|---|---|---:|
| default | 360 × 180 × 50 | 60 |
| fine | 720 × 360 × 100 | 60 |
| super_fine | 1440 × 720 × 200 | 60 |

These weak cases have **3,240,000; 6,480,000; 12,960,000 cells/GPU**: work per
GPU doubles at each step. Their efficiency reference is
`(baseline time / measured time) × (cells/GPU / baseline cells/GPU)`.
This is a linear cell-count reference; solver work need not scale linearly.
It is not constant-work-per-GPU weak scaling.

## Selectable model and execution combinations

The shared workflow supports any subset of the four combinations below. Select
models with `--models`, modes with `--modes`, explicit pairs with `--combinations`,
or all four with `--all`. The same entry point handles local and Slurm execution.

| Model | Execution | Result destination |
|---|---|---|
| HydrostaticFreeSurfaceModel | baseline | `results/hydrostatic_free_surface_models/<server>/baseline/` |
| HydrostaticFreeSurfaceModel | Dagger | `results/hydrostatic_free_surface_models/<server>/dagger/` |
| NonhydrostaticModel | baseline | `results/non_hydrostatic_models/<server>/baseline/` |
| NonhydrostaticModel | Dagger | `results/non_hydrostatic_models/<server>/dagger/` |

The series themselves define the baseline workloads. Reuse their grids, ranks,
partitions, model parameters, initial seeds, timestep and timing protocol for the
Dagger run. Do not duplicate the series definitions for each variant or model.
Compare Dagger against the matching baseline **within the same model and server**.
Speedup is baseline time / Dagger time; equal time is 1. Compare profiled cases
only against profiled cases. Failures and missing measurements have no ratio.

The default Dagger adapter uses the existing whole-function wrapper. It has the
same model and numerical kernels as baseline. [Execution adapters](execution_adapters.md)
describes the replaceable interface, dependencies and method provenance. Baseline
execution does not load Dagger. No new internal Dagger parallelization is claimed.
The earlier hydrostatic Rondeau study remains stopped; see its
[historical runbook](server/rondeau/history/hydrostatic_dagger_2026-10-30.md).

## Plan and execute the shared workflow

Set project-controlled temporary storage before setup, testing or execution:

```bash
export TMPDIR="$PWD/.runtime/tmp"
mkdir -p "$TMPDIR"
export TMP="$TMPDIR" TEMP="$TMPDIR" OMPI_MCA_orte_tmpdir_base="$TMPDIR"
export PYTHONDONTWRITEBYTECODE=1
```

Plan both models and both execution modes:

```bash
python3 benchmarking/scripts/benchmark_suite.py \
  --study .runtime/benchmark_studies/rondeau-study \
  --config benchmarking/server/rondeau/config.json \
  --models both --modes both --plan
```

The same command works for Nibi, Fir or Rorqual by selecting that server's config
and a new study directory. No executable scripts need editing. The config's
`backend` chooses local execution or Slurm submission. For a fresh study,
`--execute` replaces `--plan` to prepare and execute through that backend.
For an already reviewed plan, use the same resume command on every server:

```bash
python3 benchmarking/scripts/benchmark_suite.py \
  --study .runtime/benchmark_studies/rondeau-study --resume --watch
```

Local execution waits for idle GPUs without holding devices and runs cases
serially. Paired modes reuse physical GPU UUIDs, with alternating order between
cases. Slurm execution records `sbatch` requests and launches workers with `srun`
inside the allocation. Without `--watch`, submission returns after queueing;
captured finalizers refresh the full study and publish validated results when
allocations end. `--refresh` updates reports without launching jobs. Resume uses
saved selections and settings and never resubmits live or queued cases.

Selection examples (add the chosen flags when creating the study):

| Desired runs | Flags |
|---|---|
| Both models, baseline only | `--models both --modes baseline` |
| Both models, Dagger only | `--models both --modes dagger` |
| Hydrostatic model, both modes | `--models hydrostatic --modes both` |
| All four combinations | `--all` |
| Hydrostatic baseline plus nonhydrostatic Dagger | `--combinations hydrostatic:baseline,nonhydrostatic:dagger` |

The default selection is hydrostatic baseline. `--models` also accepts the full
Julia model names. `--series` selects a configured subset. Dagger-only selection
does not add a baseline job; comparisons can use compatible retained baseline
records, with their source paths included in the comparison CSV.

`study.json` records selections, source fingerprints, adapter snapshots, status
and output destinations. Each `<model_family>/<server>/<mode>/<series>/suite.json`
records cases and resource requests. Captured code, environments and workload
files keep queued jobs independent of later helper edits. Source/configuration
checks before and after execution exclude measurements if the library or captured
worker/adapter changes. Stop a study before switching branches or editing source.

Use `--project /absolute/environment` to select a shared isolated Julia environment
for the chosen modes. Prepare cluster environments with the shared setup helper;
selecting the Dagger adapter installs its declared dependencies in that isolated
environment, without changing the root package project:

```bash
bash benchmarking/scripts/env/setup.sh nibi \
  --adapter benchmarking/src/suite/execution/dagger
```

The Julia helper `scripts/env/setup_environment.jl ENVIRONMENT [--adapter DIRECTORY]`
also supports local setup; existing/default MPI preferences are retained when
`EBROOTOPENMPI` is unset. Review the config's accounts, modules, MPI and environment
paths before future cluster runs. Local runs require no Slurm commands.

Publication defaults to `benchmarking/results/`. `--publish` overrides this **root**
for a shared study; the workflow appends `<model_family>/<server>/<mode>/`.
Each model/server folder gets baseline/Dagger comparisons. `--reference-root`
selects a different retained result root. `--commit` commits scientific records
without raw profiles or unrelated changes. Plans never publish performance data.

`compare_dagger.py` is a compatibility wrapper selecting both modes through this
same workflow. Its old `--publish` argument still names a single model/server
folder, and its study layout remains flat for compatibility. It no longer has
an independent scheduler or a local-only execution restriction. Historical studies
must use their captured controller; do not resume superseded plans automatically.
The legacy single-suite `--output` interface remains for captured reports and
existing callers; use `--study` for new portable model/mode studies.

## Measurement and validation

Common settings: LatitudeLongitudeGrid without bathymetry, Float64, T/S tracers,
TEOS10 buoyancy and spherical Coriolis. One Julia computation thread per MPI
rank, one rank per GPU. Use two untimed warmup steps, then five synchronized
windows of ten steps. Report fastest and median seconds per step from the maximum
rank statistic. Hydrostatic T/S perturbations and nonhydrostatic initial fields
use seed 1234 plus rank, paired between execution modes.

Hydrostatic runs use WENOVectorInvariantDefault momentum advection, WENO7 tracer
advection, CATKE, SplitRungeKutta3 and a split-explicit free surface with 30 requested
substeps and extended GPU halos. Record the actual retained substeps.
Nonhydrostatic runs use a rigid lid, WENO7 momentum/tracer advection,
ScalarDiffusivity (ν = 1e-3, κ = 1e-5 m²/s), RungeKutta3 and a
ConjugateGradientPoissonSolver with LocalFFTPreconditioner by default.
Pressure stages must converge; check the final true residual independently.

Accepted measurements need complete rank records, finite fields, distinct GPUs,
MPI/CUDA communication checks, actual rank placement and timing windows. Record
global/local resolution, grid type, partition, hardware/software versions, source
revision, environment and exact command. Source/environment snapshots and status
files belong to each study. Profile results require verified captures and summaries.
Shared-server measurements do not establish exclusive-resource repeatability.

Strong efficiency = `baseline time × baseline GPUs / (time × GPUs)`.
Missing measured baselines have no efficiency estimate. The 16-GPU partition
series compares elapsed times among the listed partitions; it has no one-GPU
baseline inside that series. Resolution ratios use previous-grid / next-grid time,
with 1/8 as the linear cell-count reference for doubling all three dimensions.
Plots include the corresponding ideal/reference line. Keep profile timings separate.

## Retained artifacts

Each `baseline/<series>/` or `dagger/<series>/` may contain:

```text
<series>/
├── plot.md, results.csv, <series>.svg, suite.json
├── <case>/
│   ├── configuration.json, configuration.md
│   ├── results.json, layout.json
│   ├── rank_<n>/                        Profile summaries when applicable
│   └── provenance/                      Original revision, environment, source
├── raw_profiles/                        Large captures; ignored by Git
├── profile_manifest.json                Paths, bytes and SHA-256 checksums
├── run_records/                         Closed logs/evidence; ignored by Git
└── run_records_manifest.json            Verified execution evidence
```

Publish only completed, validated measurements. Failed reruns must not overwrite
accepted cases. Preserve historical timings and their original validation limits.
Temporary originals may be removed only after the owning process exits and the
archived copy is verified. Do not commit raw Nsight/SQLite files or pretend that
an empty Dagger destination contains measurements.

## Tests and other entry points

With the project-local temporary environment above:

```bash
python3 -m unittest discover -s benchmarking/test -v
julia --threads=1 --project=/path/to/environment benchmarking/test/test_execution_adapters.jl
```

These tests cover exact server workloads, both models and execution modes,
geometry/resource limits, immutable snapshots, launch commands, validation,
publication and comparison references without launching production jobs.
`Manifest.toml` and `LocalPreferences.toml`, when present, are local environment
records. Optional bathymetry data under `data/` is ignored by Git.
`run_benchmarks.jl` also supports the existing model and I/O benchmark CI;
`generate_bathymetry.jl` is the optional NumericalEarth bathymetry helper.
