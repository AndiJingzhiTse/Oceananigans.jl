# Oceananigans.jl — Agent Rules

## Project Overview

Oceananigans.jl is a Julia package for fast, friendly, flexible, ocean-flavored fluid dynamics on CPUs and GPUs.
It solves the incompressible (Boussinesq) Navier-Stokes equations with models including:
nonhydrostatic (with free surfaces), hydrostatic free-surface, and shallow water —
on RectilinearGrid, LatitudeLongitudeGrid, CubedSphereGrid, and ImmersedBoundaryGrid.

## Language & Environment

- **Julia 1.10+** | CPU and GPU (CUDA, AMD, Metal, OneAPI)
- **Key packages**: KernelAbstractions.jl, CUDA.jl, Enzyme.jl, Reactant.jl
- **Style**: ExplicitImports.jl for source code; `using Oceananigans` for examples/tests

## Rondeau Server

Obey to https://wiki.math.uwaterloo.ca/fluidswiki/index.php?title=info_specific_to_sutton,_rondeau,_pelee for server documentation

## Nibi Server

- Andi Tse's Nibi login username is `anditse`.
- Use `def-fpoulin` as the Slurm allocation account (`--account=def-fpoulin`).
  The login username `anditse` is not a Slurm allocation account.
- Submit compute work through Slurm. Check GPUs inside an allocation with
  `srun nvidia-smi -L`; the login node does not expose compute GPUs.
- GPU visibility inside a job may be limited to the assigned resources, so do not
  use it to infer the physical GPU count of the entire node or cluster.
- This interactive request successfully allocated one full H100 on Nibi:

  ```bash
  salloc --account=def-fpoulin \
         --nodes=1 --ntasks=1 --cpus-per-task=1 \
         --gres=gpu:h100:1 --mem=4G --time=00:10:00
  srun nvidia-smi -L
  ```

- Run `exit` when finished to release the interactive allocation.
- GPU availability changes over time. Query Slurm rather than treating a saved
  node listing as current availability.

## Critical Rules

### Kernel Functions (GPU compatibility)

- Use `@kernel` / `@index` (KernelAbstractions.jl)
- Kernels must be **type-stable** and **allocation-free**
- Use `ifelse` — never short-circuiting `if`/`else` in kernels
- No error messages, no Models inside kernels
- Mark functions called inside kernels with `@inline`
- **Never loop over grid points outside kernels** — use `launch!`

### Type Stability & Memory

- All structs must be concretely typed
- Type annotations are for **dispatch**, not documentation
- Minimize allocation; favor inline computation
- **Never hardcode Float64**: no literal `0.0` or `1.0` in kernels or constructors.
  Use `zero(grid)`, `one(grid)`, `convert(FT, 1//2)`, or rational literals

### Imports

- Source code: explicit imports (checked by tests)
- Examples/docs: rely on `using Oceananigans`; never explicitly import exported names

### Docstrings

- Use DocStringExtensions.jl with `$(TYPEDSIGNATURES)` when the signature does not include
  default values for args and/or kwargs.
- **ALWAYS `jldoctest` blocks, NEVER plain `julia` blocks** — doctests are tested; plain blocks rot
- Include `# output` with verifiable output; prefer `show` methods over boolean comparisons
- Use unicode for math (`Δt`, `η`, `ρ`), not LaTeX — LaTeX doesn't render in the REPL

### Model Constructors

- `grid` is positional: `NonhydrostaticModel(grid; closure=nothing)`
- `ShallowWaterModel(grid, gravitational_acceleration; ...)` — both positional
- Omit semicolon when there are no keyword arguments: `NonhydrostaticModel(grid)` not `NonhydrostaticModel(grid;)`

## Naming Conventions

- **Files**: snake_case matching the type they define — `nonhydrostatic_model.jl`
- **Types/Constructors**: PascalCase **only for true constructors** — `NonhydrostaticModel`
- **Functions**: snake_case — `time_step!`; functions that return values are never PascalCase
- **Kernels**: may prefix with underscore — `_compute_tendency_kernel`
- **Variables**: English long name or readable unicode math notation — never mix abbreviated and
  full forms (e.g., `cond` vs `condition`) to imply a difference; be specific

## Module Structure

```
src/
├── Oceananigans.jl            # Main module, exports
├── Architectures.jl           # CPU/GPU architecture abstractions
├── Grids/                     # Grid types and constructors
├── Fields/                    # Field types and operations
├── Operators/                 # Finite difference operators
├── BoundaryConditions/        # Boundary condition types
├── Models/                    # Model implementations
│   ├── NonhydrostaticModels/
│   ├── HydrostaticFreeSurfaceModels/
│   ├── ShallowWaterModels/
│   └── LagrangianParticleTracking/
├── TimeSteppers/              # Time stepping schemes
├── Solvers/                   # Poisson and tridiagonal solvers
├── TurbulenceClosures/        # LES and eddy viscosity models
├── Advection/                 # Advection schemes
├── BuoyancyFormulations/      # Buoyancy models
├── OutputWriters/             # File I/O
├── Simulations/               # High-level simulation interface
└── Utils/                     # Utilities and helpers
```

## Common Pitfalls

1. **Type instability** in kernels ruins GPU performance
2. **Overconstraining types**: use annotations for dispatch, not documentation
3. **Missing imports**: tests will catch this — add to `using` statements
4. **Plain `julia` blocks in docstrings**: always use `jldoctest`
5. **Subtle bugs from missing method imports**, especially in extensions
6. **Expecting unexported names**: consider exporting them rather than changing user scripts
7. **Extending `getproperty` to fix undefined property bugs**: fix on the caller side instead
8. **"Type is not callable" errors**: variable name shadows a function — rename or qualify
9. **Quick fixes that break correctness**: if a test fails after a change, revisit the original edit
10. **Commented-out code**: delete it. Git is the journal — don't leave commented code, debugging
    artifacts, or stale copy-paste remnants
11. **2D indexing on fields**: always use 3D indexing (`field[i, j, k]`). 2D indexing works by
    coincidence on some fields but is unsupported and will break
12. **Hardcoded Float64**: never use `0.0`, `1.0` in kernels or constructors; use `zero(grid)` etc.
13. **Scope creep in PRs**: keep changes focused on a single concern. Unrelated cleanup goes
    in a separate PR
14. **Modifying Project.toml dependencies**: never add, remove, or change `[deps]` or `[weakdeps]`
    in the root `Project.toml` unless the task absolutely requires it. Dependency changes have
    wide-reaching consequences — they affect CI, load time, and downstream compatibility.
    Only touch `[compat]` bounds when explicitly asked.

## Git Workflow

Follow [ColPrac](https://github.com/SciML/ColPrac). Feature branches, descriptive commits,
update tests and docs with code changes, check CI before merging.

Use one working checkout at `/u/ajtse/Oceananigans.jl`. Commit changes before
switching branches in that folder. Do not create additional worktrees or put
code, environments, benchmarks, logs, archives, or temporary files in
`/local_scratch`. This explicit workspace preference supersedes older storage
examples and historical benchmark paths.

Make a descriptive git commit for every finished task that changes repository
files, including code, documentation, instructions, and benchmark results.
Complete the relevant checks before committing, stage only files belonging
to that task, and leave unrelated user changes untouched. Report the commit
hash when the task is finished. For read-only tasks with no repository
changes, do not create an empty commit.

After finishing every task, leave the working tree clean. Commit the task's
changes and verify `git status --short` is empty: there should be no
uncommitted tracked changes or untracked files.
Include outstanding benchmark records in descriptive commits after checking
their contents; distinguish in-progress logs from completed measurements.
Do not discard or silently commit unrelated user edits to achieve a clean
tree. If such edits or files still being written by active jobs prevent a
clean tree, preserve them and explicitly report the remaining paths and why
they could not be cleared. Recheck the working tree immediately before the
final response.

## Temporary Files and Storage

**Never write repository-related files to `/tmp` or `/var/tmp`.** This applies
to benchmarks, tests, profiling, package setup, downloads, scripts, logs, and
temporary files created by child processes. Do not use symlinks whose targets
resolve to these system temporary directories.

Use project-controlled directories inside the sole working checkout. Use
`/u/ajtse/Oceananigans.jl/.runtime/tmp/` for temporary files, `.runtime/` for
ignored environments, studies and archives, and
`benchmarking/results/<model_family>/<machine>/` for retained artifacts.
Never use `/local_scratch`, including through a symlink. Historical provenance
may retain old paths as evidence; do not rewrite original measurements.
Before launching tools or tests, explicitly set `TMPDIR`, `TMP`, and `TEMP`
to an existing directory there. Configure library-specific temporary storage
as well, including `OMPI_MCA_orte_tmpdir_base` for OpenMPI, and verify that
child processes inherit the settings. An unset `SCRATCH` must never cause a
fallback to `/tmp`. Python `tempfile` and Julia temporary-file helpers must
also use the configured data-filesystem directory.

Set Nsight output paths and the benchmark `trace_root` explicitly. Retain
captures under `<variant>/<series>/raw_profiles/` inside the machine's results
folder, with paths, byte sizes, and SHA-256 checksums recorded in manifests.
Keep large raw captures out of Git. Use case-specific `.runtime/` directories
for active temporary files and `run_records/<case>/` for closed CPU/GPU logs
and other execution evidence. Short aliases under `~/.ocean-tmp/` are allowed
when they resolve into these directories and are needed for MPI socket limits.

Never move or delete temporary files belonging to a running process. After
the owning run exits, verify archived copies before removing their temporary
originals. Clean up only files belonging to the task; preserve unrelated users'
files and active sessions. Check the resolved output and temporary paths before
starting any long run.

## Benchmark Records

For standard benchmark series, use `benchmarking/scripts/benchmark_suite.py`
with a machine configuration under `benchmarking/scripts/configs/`. Shared planning,
execution and reporting live in `benchmarking/src/suite/`; tests are in
`benchmarking/test/`. One controller supports HydrostaticFreeSurfaceModel and
NonhydrostaticModel. Legacy controllers and launchers have been removed.
See `benchmarking/README.md` for the series table and setup instructions.

Curated results use `benchmarking/results/<model_family>/<machine>/<series>/`,
with a combined `plot.md` inside each machine folder. The two model families are
`hydrostatic_free_surface_models` and `non_hydrostatic_models`; each contains
Andi-5070ti, fir, nibi, rondeau and rorqual. Keep the latest accepted measurement
for each configuration, including its original provenance and validation limits.
Run repeat studies in a fresh scratch directory and use `--publish` to update
curated results after validation. Failed reruns must not replace accepted results.

Use these canonical global resolutions for named benchmark grids:

| Grid name | Global resolution (`Nx × Ny × Nz`) |
|---|---|
| `super_fine` | `1440 × 720 × 200` |
| `super_super_fine` | `2880 × 1440 × 200` |
| `super_super_super_fine` | `5760 × 2880 × 200` |
| `fine` | `720 × 360 × 100` |
| `default` | `360 × 180 × 50` |

For every benchmark run, record the **partition**, **resolution**, and
**grid type** actually used in the saved run metadata and the results report.
State the MPI partition explicitly as `Px × Py × Pz` (use `1 × 1 × 1` for
a single-rank run), the global resolution as `Nx × Ny × Nz`, and the grid
type (for example, `LatitudeLongitudeGrid` or `RectilinearGrid`). For
distributed runs, also record the local resolution per rank. In benchmark
series, associate these settings with each individual run so that its
configuration remains clear when results are compared or plotted.

### Common Benchmark Settings and Records

Unless the user specifies a different configuration, use `earth_ocean` on a
`LatitudeLongitudeGrid` without bathymetry, Float64,
`WENOVectorInvariantDefault` momentum advection, WENO7 tracer advection,
CATKE, T/S tracers, `SplitRungeKutta3`, Δt = 60 simulated seconds, and
30 requested free-surface substeps. Run two untimed warmup steps followed
by five timing windows of ten steps each. Record the actual retained
free-surface substeps and `extend_halos` setting; the CPU MPI scaling
configuration uses `extend_halos=false`, while the GPU configuration uses
`extend_halos=true`. Keep model and grid settings consistent within a
comparison, and record any intentional exceptions.

Record MPI ranks, Julia threads per rank, physical cores, nodes, actual
CPU/GPU affinity, hardware, Julia/package/MPI/CUDA/profiler versions as
applicable, source revision, environment snapshot, submission command,
requested resources and execution outcome alongside the required grid and
partition metadata. Validate complete rank results, resource placement,
finite model fields, and MPI communication before accepting measurements.
For GPU MPI runs, verify distinct GPUs and CUDA-aware MPI communication.

### Benchmark Reporting and Completion

For the Rondeau hydrostatic baseline/Dagger study, use the shared paired
controller with `--model HydrostaticFreeSurfaceModel --gpu-only --wait-for-gpus`.
Run the seven standard GPU series described in `benchmarking/hydrostatic_dagger.md`.
Publish under `hydrostatic_free_surface_models/rondeau/{baseline,dagger}/`.
Use project-local `.runtime/` storage, paired seeds and GPU assignments, and
the original whole-window wrapper. Do not change solver kernels or launch CPU
benchmark series. Wait for occupied GPUs without holding resources. Stop the
controller before changing branches or benchmark/library source.

Rondeau NonhydrostaticModel uses the GPU-only five-series plan documented in
`benchmarking/README.md`: `gpu_weak_scaling` first, `gpu_scaling_fine`,
`gpu_nsight_scaling_default`, `gpu_resolution`, and `gpu_ensemble`. The ensemble
runs four independent single-GPU models concurrently at default and fine
resolution. Compare concurrent Distributed calls against four full-simulation
Dagger tasks; retain both timed makespan and dispatch-to-completion time.
Each simulation keeps partition 1 × 1 × 1 and the shared numerical validation.
CPU benchmarks are cancelled
and removed from the Rondeau study; do not recreate or launch CPU suites there.
Use default/fine/super_fine resolutions only for these resolution studies.
The requested GPU weak sequence is default/1 GPU, fine/2 GPUs, super_fine/4 GPUs;
cells per GPU increase 1:4:16. Label its linear cell-count reference explicitly;
do not describe it as constant-work-per-GPU weak scaling. This machine-specific
plan supersedes the generic maximum-size and weak-sequence guidance below.
Hide CUDA devices before starting CPU Julia ranks, including Dagger CPU runs.

Report fastest and median seconds per step: divide each rank's minimum
and median window durations by the number of steps per window, then use
the maximum across ranks for each reported statistic. Plot timing and MPI
efficiency for strong-scaling studies, and timing comparisons for resolution
and partition studies. Normalize efficiency to the measured one-core or
one-GPU baseline: `efficiency = baseline_time * baseline_rank_count /
(measured_time * measured_rank_count)`. If that baseline fails, explicitly
identify any alternative measured baseline; do not invent missing timings.

Always draw the expected ratio or ideal efficiency on benchmark ratio and
efficiency plots, and draw ideal inverse-rank timing on strong-scaling plots
when a measured baseline exists. Label each reference and state the ratio's
numerator, denominator, and any normalization. Ideal MPI efficiency is 100%;
doubling ranks at fixed resolution gives next-count/previous-count time = 1/2.
For resolution studies, account for all grid dimensions: doubling Nx, Ny, and
Nz gives previous-grid/next-grid time = 1/8 under linear cell-count scaling.
Plot this raw time ratio with an expected 1/8 reference; do not apply a cube root.

For GPU weak scaling starting at `super_fine`, hold 207,360,000 interior cells
per GPU fixed: use 1, 4, 16, 64, … GPUs, double both horizontal dimensions at
each step, and retain 200 vertical levels. Weak efficiency is baseline step
time / measured step time, with ideal efficiency 100% and constant ideal step
time. Larger horizontal grids use Δt = 60 × 1440 / Nx seconds. Strong scaling
on `super_super_fine` and `super_super_super_fine` starts at memory-feasible
4- and 16-GPU baselines respectively; record those measured baselines explicitly.
Include a DRAC-style GPU comparison table with resolution, ranks, actual nodes,
partition, Δt, median seconds per step, efficiency, throughput, measured device
memory per GPU and outcome. Never substitute reference-cluster timings for
local measurements or invent unavailable memory statistics.

Only completed, validated measurements enter performance plots. Record
the highest completed count and the observed reason further scaling could
not complete. Distinguish scheduler queue/wait limits, submission/resource
limits, geometry limits, timeouts and application or memory failures. Keep
profiling measurements separate from unprofiled timings; record capture
scope and preserve trace locations, checksums and profile summaries.
Preserve raw results and failure evidence in the scratch study directory.
Publish completed measurements into the curated results tree, keeping older
accepted cases when a rerun fails. Commit each finished task and its benchmark
records under the Git Workflow rules above.

## Design Principles

- **Dispatch over conditionals**: use Julia's type system and multiple dispatch instead of
  `if`/`else` branching. Backend-specific code goes in `ext/` extensions, not `if` branches in `src/`
- **Use `on_architecture` for data transfers** — never manual `Array()` / `CuArray()` calls
- **Defaults serve the common case**: avoid `nothing` defaults when a concrete default (like `CPU()`)
  covers 80% of usage. Minimize boilerplate for the typical user.
- **Keyword argument names must be consistent** across related types and constructors
- **Always use explicit `return`** in functions longer than one expression
- **One operation per line** as default; break long expressions across lines

## Agent Behavior

- Prioritize type stability and GPU compatibility
- Follow established patterns in existing code
- Add tests for new functionality; update exports when adding public API
- Reference physics equations in comments when implementing dynamics

## Further Reading

Detailed reference docs are in `.agents/` — read on demand:

| Document | Content |
|----------|---------|
| `.agents/testing.md` | Full testing guidelines, running tests, debugging |
| `.agents/documentation.md` | Building docs, fast builds, doctest details, writing examples |
| `.agents/validation.md` | Reproducing paper results step-by-step |

### Auto-loading Rules

Rules in `.claude/rules/` load automatically when you touch matching files:
- `kernel-rules.md` — GPU kernel requirements (src/)
- `docstring-rules.md` — docstring and jldoctest conventions (src/)
- `testing-rules.md` — test writing and running (test/)
- `docs-rules.md` — documentation building and style (docs/)
- `examples-rules.md` — Literate.jl example conventions (examples/)

### Skills (slash commands)

- `/run-tests` — run targeted tests, prioritized by what's likely to break
- `/build-docs` — build documentation locally
- `/add-feature` — checklist for adding new physics/features
- `/new-simulation` — set up, run, and visualize a new simulation (with or without a reference paper)
- `/babysit-ci` — monitor CI, auto-fix small issues, pause on bigger problems, retrigger flaky runs
