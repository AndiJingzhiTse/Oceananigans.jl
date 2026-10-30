# Benchmarking

One shared controller runs `HydrostaticFreeSurfaceModel` and `NonhydrostaticModel`.
Server files define the workloads; model construction, execution, validation and
reporting stay in shared code. Run commands from the repository root.

[Workflow requirements](requirements.md) define the requested common local/Slurm
entry point, selectable model/mode combinations and replaceable Dagger adapter.
They distinguish future requirements from currently implemented capabilities.

## File structure

```text
benchmarking/
├── README.md
├── requirements.md                     Shared workflow and integration contract
├── Project.toml                         Julia benchmark package dependencies
├── server/
│   ├── README.md                        Server plans and the four-run matrix
│   ├── rondeau/
│   │   ├── config.json                  Resources, launcher and environment
│   │   ├── series.json                  Exact grids, GPU counts and partitions
│   │   ├── README.md                    Human-readable server plan
│   │   └── history/                     Superseded study instructions
│   ├── nibi/                            config.json, series.json, README.md
│   ├── rorqual/                         config.json, series.json, README.md
│   ├── fir/                             config.json, series.json, README.md
│   └── Andi-5070ti/                     Retained local config; no new server plan
├── scripts/
│   ├── benchmark_suite.py               Shared local/Slurm controller
│   ├── compare_dagger.py                Existing local whole-window wrapper study
│   ├── run_benchmarks.jl                Configurable model and I/O benchmarks
│   ├── generate_bathymetry.jl           Optional bathymetry preparation
│   └── env/                            Shared Julia/MPI/module setup
├── src/
│   ├── OceananigansBenchmarks.jl
│   ├── earth_ocean.jl                   Shared benchmark model construction
│   └── suite/
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
    │       ├── README.md                Current plan and retained-result status
    │       ├── baseline/<series>/<case>/
    │       ├── dagger/<series>/<case>/
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

The full selection contains the four combinations below. The requested workflow
must also allow any subset: one or both models, baseline or Dagger or both, and
explicit mixed combinations. See [the requirements](requirements.md) for the
shared local/Slurm workflow; the current CLI selects one combination per invocation.

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

**The new Dagger execution method is deferred until the user's next instructions.**
This reorganization creates plans and documents destinations; it launches no new
benchmarks. The existing whole-window `Dagger.@spawn` implementation is retained
as a historical wrapper method. `--execution-mode dagger --plan` can record the
matching planned configurations; it does not choose or validate a new integration.
The earlier hydrostatic Rondeau study was stopped while waiting for GPUs; see its
[historical runbook](server/rondeau/history/hydrostatic_dagger_2026-10-30.md).

## Plan without running

Server resource/software settings moved from `scripts/configs/<server>.json` to
`server/<server>/config.json`. A `series_file` path is resolved relative to that
config. Resolved definitions are embedded in `suite.json` and saved beside the
executable snapshot as `run_metadata/series.json`; later edits do not change
an existing study's cases. Review cluster accounts, modules and capacities before
any future submission. Cluster environment preparation remains in `scripts/env/`.
The retained `Andi-5070ti` profile is outside the new four-server GPU plans.

```bash
export TMPDIR="$PWD/.runtime/tmp"
mkdir -p "$TMPDIR"
export TMP="$TMPDIR" TEMP="$TMPDIR" OMPI_MCA_orte_tmpdir_base="$TMPDIR"
export PYTHONDONTWRITEBYTECODE=1

python3 benchmarking/scripts/benchmark_suite.py \
  --config benchmarking/server/rondeau/config.json \
  --model HydrostaticFreeSurfaceModel --execution-mode baseline \
  --output .runtime/benchmark_studies/new-plan/hydrostatic_free_surface_models/rondeau/baseline \
  --plan
```

Change `--model` to `NonhydrostaticModel` and `--execution-mode` to `dagger`
to prepare each of the other three combinations in its own study directory.
Use `--series` for a configured subset. A new plan refuses unconfigured series;
legacy definitions remain available to read/refresh historical studies.
The default publication destination includes the execution mode.

The existing baseline controller supports `--run` for local execution and
`--submit` for Slurm, followed by `--resume --watch`. These are future execution
steps, not part of this reorganization. Rondeau has no scheduler: check live GPU
usage and wait for occupied GPUs without holding resources. The existing local
paired wrapper controller supports cooperative `--wait-for-gpus` checks and source
guards; it is not a Slurm submission controller. Do not switch branches or edit
library/benchmark/server definitions while jobs from this checkout run.

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
```

These tests cover exact server workloads, both models and execution modes,
geometry/resource limits, immutable snapshots, launch commands, validation,
publication and comparison references without launching production jobs.
`Manifest.toml` and `LocalPreferences.toml`, when present, are local environment
records. Optional bathymetry data under `data/` is ignored by Git.
`run_benchmarks.jl` also supports the existing model and I/O benchmark CI;
`generate_bathymetry.jl` is the optional NumericalEarth bathymetry helper.
