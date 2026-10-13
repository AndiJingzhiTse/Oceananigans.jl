# Ocean model benchmarks

Use **`benchmark_suite.py`** for new server studies. It runs the ten series
below through one planner, one Julia worker and one report generator. Python
3.11+, Julia with the benchmark project installed, Open MPI, and matplotlib
(for plots) are required. NVIDIA GPUs, CUDA-aware MPI and Nsight Systems are
required for GPU/profile cases. Use assigned compute resources; on clusters,
submit through Slurm rather than running computation on a login node.

| Series | Resolution | Resource sequence / partition |
|---|---|---|
| `cpu_mpi_scaling_super_fine` | 1440×720×200 | 1, 3, 6, 12, 24, … physical cores; one MPI rank/core |
| `gpu_scaling_super_fine` | 1440×720×200 | 1, 2, 4, 8, … GPUs; one MPI rank/GPU |
| `cpu_resolution` | 360×180×50 → 720×360×100 → 1440×720×200 | One physical core, one rank/thread |
| `gpu_resolution` | 360×180×50 → 720×360×100 → 1440×720×200 | One GPU, one rank/thread |
| `cpu_partition_cores_super_fine` | 1440×720×200 | Exactly 192 cores/ranks; all 14 horizontal factor pairs, 192×1×1 → 96×2×1 → 64×3×1 → … → 1×192×1 |
| `gpu_nsight_scaling_super_fine` | 1440×720×200 | Nsight on 1, 2, 4, 8, … GPUs, with separate traces per rank |
| `gpu_partition_super_fine` | 1440×720×200 | 1×1×1 baseline and all horizontal factor pairs for 2, 4, 8, 16, 32 and 64 GPUs; MPI efficiency normalized to the measured 1×1×1 case |
| `gpu_scaling_super_super_fine` | 2880×1440×200 | 4, 8, 16, … GPUs; measured 4-GPU efficiency baseline; Δt=30 s |
| `gpu_scaling_super_super_super_fine` | 5760×2880×200 | 16, 32, 64, … GPUs; measured 16-GPU efficiency baseline; Δt=15 s |
| `gpu_weak_scaling_super_fine` | 1440√n × 720√n × 200 | 1, 4, 16, … GPUs; fixed 207,360,000 cells/GPU; Δt=60/√n s |

## Saved series inventory

This is a **2026-10-13 UTC snapshot of saved records**. Completed counts
refer to validated measurements, not completion of every planned case. Follow
each run's `plot.md` and `suite.json` for updated outcomes; records on other
clusters may reflect an earlier refresh. The identifiers below are the exact
names accepted by the current controller's `--series` option.

| Series identifier | Study | Completed Rorqual measurements |
|---|---|---|
| `cpu_mpi_scaling_super_fine` | CPU strong scaling | Through 12,288 cores after CPU rerun |
| `gpu_scaling_super_fine` | GPU strong scaling | Through 64 GPUs |
| `cpu_resolution` | CPU resolution comparison | All three grids |
| `gpu_resolution` | GPU resolution comparison | All three grids |
| `cpu_partition_cores_super_fine` | CPU partition comparison at 192 cores | 13 valid partitions; remaining layout is a geometry limit |
| `gpu_nsight_scaling_super_fine` | GPU scaling under Nsight profiling | Through 64 GPUs |
| `gpu_partition_super_fine` | GPU partition comparison | Original sweep through 16 GPUs; expanded rerun in progress |
| `gpu_scaling_super_super_fine` | Strong scaling, 2880×1440×200 | Through 64 GPUs |
| `gpu_scaling_super_super_super_fine` | Strong scaling, 5760×2880×200 | Earlier results through 64 GPUs; fresh rerun pending |
| `gpu_weak_scaling_super_fine` | Fixed cells/GPU, starting at super_fine | Through 64 GPUs |

All saved hydrostatic studies, including historical protocols and retries,
live under [results/hydrostatic_free_surface_models/](results/hydrostatic_free_surface_models/):

| Location | Saved studies |
|---|---|
| [Rorqual](results/hydrostatic_free_surface_models/rorqual/) | All ten standard series; original full suite, CPU retry, extended GPU suite, and latest partition/largest-grid rerun |
| [Nibi](results/hydrostatic_free_surface_models/nibi/) | GPU strong scaling; CPU hybrid scaling with 192 threads/rank; CPU scaling with one rank/core; four-node CPU partition comparison; four-GPU partition comparison; GPU Nsight partition study; extended GPU strong/weak scaling and partition suite |
| [Fir](results/hydrostatic_free_surface_models/fir/) | Initial seven-series suite: CPU/GPU strong scaling, CPU/GPU resolution, CPU/GPU partitions, and GPU Nsight scaling. GPU scaling measurements are saved; other cases include failed and pending attempts |
| [Rondeau](results/hydrostatic_free_surface_models/rondeau/) | CPU/GPU resolution comparisons; CPU strong scaling on default and fine grids; GPU strong scaling on fine and super_fine grids; CPU/GPU profiling; targeted super_fine rerun; six-case component ablation |
| [Andi-5070ti](results/hydrostatic_free_surface_models/Andi-5070ti/) | Local CPU/GPU benchmark sweeps; distributed CPU benchmarks; GPU profiling at 720×360×50 and 360×180×50; CPU profiling at 720×360×50 |
| [Suite validation](results/hydrostatic_free_surface_models/suite_validation/) | Completed two-rank CPU MPI smoke test on a 72×36×8 grid; validation rather than production scaling |

The Rondeau component ablation cases are baseline, no tracer advection,
no Coriolis, no buoyancy, no closure, and no user tracers. The last case also
disables buoyancy because the default seawater formulation requires T/S.
Historical protocols differ: some Rondeau grids retain 50 vertical levels,
the initial Nibi CPU study uses 192 threads/rank, and the extended Nibi GPU
scaling study uses five 100-step windows. Consult each run's configuration;
matching grid or series names do not establish identical settings.

## Terminology

| Term | Meaning |
|---|---|
| Case / series / suite | A case is one configuration. A series varies resources, resolution, partition, or model components. A suite groups series in one run directory. |
| Node / allocation | A node is a compute machine. A Slurm allocation grants specified nodes, CPUs, GPUs, memory, and wall time; it can execute several cases sequentially. |
| MPI rank / Julia thread / physical core | A rank is a process communicating through MPI. Threads share a process. Physical cores exclude SMT hardware threads. Standard CPU cases use one rank and one computation thread/core; GPU cases use one rank/GPU. Requested GPU host CPUs are separate from Julia computation threads. |
| Global / local resolution | Global `Nx × Ny × Nz` describes the entire grid. Local resolution describes one rank's interior cells; remainder cells can make local sizes differ between ranks. |
| MPI partition | `Px × Py × Pz` splits the grid across ranks, with `Px × Py × Pz = rank count`. Standard cases use horizontal decomposition (`Pz=1`); a single rank is `1 × 1 × 1`. |
| Grid type | The geometry implementation, such as `LatitudeLongitudeGrid`, `RectilinearGrid`, or a tripolar grid. Record it separately from resolution. |
| Halo / extended halos | Extra boundary cells exchanged between ranks. `extend_halos` enlarges the free-surface halo region; record it because it changes communication and the minimum feasible local domain. |
| Δt / free-surface substeps | Δt is simulated time advanced per model step. The free-surface solver takes smaller internal steps; record both requested and actually retained substep counts. |
| Warmup / timing window | Warmup is untimed preparation. A timing window measures a block of model steps. Standard cases use two untimed steps and five windows of ten steps. |
| Fastest / median seconds per step | For each rank, divide its minimum/median window duration by steps/window. Report the maximum of those per-rank values, so the slowest rank determines the statistic. |
| Strong / weak scaling | Strong scaling fixes the global grid while increasing resources. Weak scaling fixes work per resource while increasing the global grid and resources together. |
| Baseline / speedup / MPI efficiency | A baseline is a measured reference case. Speedup is baseline time divided by measured time. Strong efficiency accounts for the resource-count increase; weak efficiency compares times at fixed work/resource. See formulas below. |
| Resolution / partition comparison | Resolution studies change grid size at fixed resources. Partition studies change decomposition; compare layouts at the same resource count and model settings. |
| Component ablation | Disable a selected model component to measure its contribution; record dependent changes such as disabling buoyancy when removing T/S. |
| Nsight profiling | Instrumented CUDA/MPI/NVTX capture. Profiled timings remain separate from unprofiled timings because capture can affect performance. |
| Throughput / GiB per GPU | Throughput is global interior cells divided by seconds/step. GiB is bytes/2³⁰. Device memory is measured after timing and reported as the maximum across ranks; it includes context/buffers and is not peak memory. |
| Outcome / limit | `PENDING` or `RUNNING` is unfinished. `COMPLETED` requires validated artifacts. Geometry, configured resource bounds, scheduler restrictions, timeouts, application failures, and invalid results are different outcomes. |

Canonical names for new standard series are:

| Grid name | Global resolution |
|---|---|
| `default` | 360 × 180 × 50 |
| `fine` | 720 × 360 × 100 |
| `super_fine` | 1440 × 720 × 200 |
| `super_super_fine` | 2880 × 1440 × 200 |
| `super_super_super_fine` | 5760 × 2880 × 200 |

## Instructions for every series

These requirements apply to new series and reruns. Explicit user settings
override defaults; document intentional exceptions. Follow the repository's
[benchmark and Git rules](../AGENTS.md#benchmark-records) as well.

1. **Plan and preserve provenance.** Use `benchmark_suite.py` and a profile under
   `configs/` for standard series. Create a fresh dated directory under
   `results/<model_family>/<server>/` (hydrostatic or nonhydrostatic). Record the purpose,
   configurations, source revision, exact launch/submission commands, executable
   snapshot, and resolved Julia environment. Preserve previous results and failures.
2. **Keep comparisons consistent.** Use the model settings below unless explicitly
   changed. Record actual global/local resolution, grid type, partition, rank/thread
   counts, Δt, warmup, samples, steps/window, requested/retained substeps, and halo
   settings for every case. Keep physics, precision, solver, and timing protocol
   consistent within a comparison. Explain historical differences before comparing.
3. **Use assigned resources.** Submit cluster computation through Slurm. Record
   requested resources and actual nodes, physical cores, affinity, GPUs, hardware,
   and Julia/package/MPI/CUDA/profiler versions. Query current scheduler availability;
   configured capacity does not guarantee allocation. Prepare the environment before
   submitting, and keep developed source paths stable until jobs finish.
4. **Validate before accepting timing.** Verify every rank result, expected local
   sizes, unique CPU/GPU placement, MPI communication, and finite model fields.
   GPU runs must use distinct GPUs and pass CUDA-aware MPI checks. Synchronize ranks
   and GPUs around timing windows. Use the slowest-rank statistics defined above.
5. **Use measured baselines.** Use one core/GPU where feasible, or the explicitly
   planned 4-/16-GPU baseline for larger grids. Leave efficiency unavailable until
   the baseline completes successfully. Never invent timings or combine an old
   baseline with a fresh rerun. Investigate efficiency above 100% using raw windows,
   configuration, and placement; retain observed values without clipping them.
6. **Report timings and references.** Plot strong-scaling timings and efficiencies,
   weak-scaling timings and efficiencies, resolution timings and raw ratios, and
   partition comparisons. GPU partition plots use MPI efficiency relative to
   measured `1 × 1 × 1`, start the y-axis at zero, and show ideal 100%. Draw the
   applicable expected ratio/efficiency and ideal timing from the formulas below.
   Label numerator, denominator, baseline, resource count, and units. Order the
   strong-grid comparison legend by 1-, 4-, then 16-GPU baseline. Use plain ticks
   when scientific notation adds no information.
7. **Separate measurements from outcomes.** Plot only completed, validated cases.
   Record the largest completed count and the observed reason larger cases did
   not complete. Preserve raw windows, logs, failure evidence, trace locations,
   checksums, and profile summaries. Keep profiled and unprofiled results separate.
   GPU comparison tables include resolution, ranks, actual nodes, partition, Δt,
   median seconds/step, efficiency, throughput, measured GiB/GPU, and outcome;
   unavailable measurements stay blank.
8. **Finish with reviewable records.** Refresh reports, run checks appropriate to
   the change, and commit the task's source/documentation and benchmark records.
   Identify in-progress logs separately from validated measurements. Verify
   `git status --short` is empty before reporting completion. Preserve unrelated
   edits; if active writers prevent a clean tree, report the remaining paths and
   their cause. Never remove evidence just to clean the tree.

### Efficiency and expected references

Let `T(n)` be fastest or median seconds/step at `n` resources, and let `nb`
be the measured baseline resource count. Use the same timing statistic in
both numerator and denominator.

| Quantity | Formula | Expected reference |
|---|---|---|
| Speedup | `T(nb) / T(n)` | Strong scaling: `n / nb` |
| Strong MPI efficiency (%) | `100 × T(nb) × nb / (T(n) × n)` | 100% |
| GPU partition MPI efficiency (%) | `100 × T(1×1×1) / (T(partition) × ranks)` | 100% |
| Weak efficiency (%) | `100 × T(nb) / T(n)` at fixed cells/resource | 100% |
| Strong timing | `T(n)` | `T(nb) × nb / n` |
| Weak timing | `T(n)` | Constant `T(nb)` |
| Strong adjacent time ratio | `T(next count) / T(previous count)` | 1/2 when doubling resources |
| Resolution time ratio | `T(previous grid) / T(next grid)` | 1/8 when doubling Nx, Ny, and Nz |

Plot the raw resolution ratio without a cube root. For historical grids with
fixed Nz or other size changes, derive the expected ratio from actual interior
cell counts; doubling only Nx and Ny gives 1/4 under linear cell-count scaling.
For GPU weak scaling starting at `super_fine`, use 1, 4, 16, 64, … GPUs,
207,360,000 interior cells/GPU, 200 vertical levels, and
`Δt = 60 × 1440 / Nx` seconds. Doubling both horizontal dimensions at each
stage quadruples the GPU count.

### Default model and timing settings

Scaling counts continue to the configured server capacity or the first geometry
limit. The next doubling is recorded as a resource/geometry boundary. A
configured capacity is a planning bound, not proof that those resources are
available now: submission, queue and execution outcomes are recorded separately.
A failed one-GPU allocation does not prevent trying larger GPU counts.

All cases use LatitudeLongitudeGrid without bathymetry, Float64,
WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3, Δt=60 s and
30 requested free-surface substeps. The larger horizontal grids reduce Δt as
shown above; the original three-grid resolution studies retain Δt=60 s and
their original grid list. CPU cases use `extend_halos=false`; GPU
cases use `extend_halos=true`. Every rank has one Julia computation thread.
There are two untimed steps (one warmup and one helper preflight step), then
five ten-step timing windows. Windows synchronize ranks and GPUs at both
boundaries. This explicit synchronization differs from the historical helpers;
the worker records individual windows and actual retained free-surface substeps.

## Nonhydrostatic suite and model comparison

The suite defaults to `HydrostaticFreeSurfaceModel`. Use `--model NonhydrostaticModel`
to repeat all ten series with the standard **rigid-lid** nonhydrostatic model.
Its results live under `results/non_hydrostatic_free_surface_models/<server>/`;
the directory name is an organizational label and does not imply an evolving
free surface. The controller keeps the same grid sizes, resource sequences,
partitions, Float64 precision, T/S, TEOS10 buoyancy, traditional spherical
Coriolis, Δt, and five ten-step timing windows.

Nonhydrostatic cases use WENO7 momentum/tracer advection, `ScalarDiffusivity`
with ν=1e-3 and κ=1e-5 m²/s, `RungeKutta3`, and a three-dimensional
`ConjugateGradientPoissonSolver`. CATKE, `SplitRungeKutta3`, and the
split-explicit free surface are hydrostatic settings. Nonhydrostatic runs have
no free-surface substeps or extended free-surface halos. The hydrostatic
partition geometry bounds are retained to compare the same layouts. The
worker validates finite velocities, tracers and pressure, and checks the residual
against the configured tolerance after every RK3 pressure solve, including warmup.
The pressure iteration cap defaults to 5000 and must be identical on every rank;
different local bounds could desynchronize uneven MPI partitions. Record the
preconditioner, relative/absolute tolerances, iteration cap, and every solve's
iterations, residual, tolerance and convergence outcome. Nonhydrostatic initial
conditions use a recorded seed of 1234 plus MPI rank for reproducible solver pilots.

Server specs can select `pressure_preconditioner` as
`DiagonallyDominantPreconditioner`, `ColumnwiseTridiagonalPreconditioner`,
`VerticalLinePreconditioner`, or `LocalFFTPreconditioner`.
Use `pressure_diagnostics: true` for pilots to log residual progress every 200
iterations; these records reuse the solver's existing norm evaluations. Keep
diagnostics disabled for production timings. The columnwise preconditioner
targets thin, vertically stretched ocean grids; validate its CPU/GPU MPI behavior
and convergence on a representative production grid before choosing it for a suite.
Keep convergence tolerances unchanged when comparing preconditioners.

The worker's vertical-line variant retains the full Poisson matrix diagonal
when solving each vertical block. The local FFT variant applies the existing
Fourier/tridiagonal solver to a Cartesian approximation of each rank's block,
with the same stretched vertical coordinates. Its screening term is the sum
of `1/local_L²` over the horizontally partitioned directions; an unsplit
longitude direction retains its physical periodic topology. The auxiliary Cartesian
grid changes only the approximate inverse: the model and pressure operator
remain on the recorded latitude–longitude grid. This avoids distributed FFT
transpose divisibility restrictions on partition comparisons. Record each
rank's auxiliary extent and screening term; FFTW uses one thread and ESTIMATE
planning. Validate actual convergence rather than assuming an FFT approximation
is adequate. Local FFT runs also check symmetry and the sign of the quadratic
form before model initialization. These benchmark preconditioners do not modify
package solver defaults.

New nonhydrostatic suites default to the local FFT preconditioner, independent
partition allocations, full GPU-node reservations on Slurm, eight-hour CPU
allocations and six-hour GPU allocations. Low-rank CPU limits are 72/48/24/12
hours at 1/3/6/12 ranks. Explicit server specs override these defaults.
These limits accommodate the measured global-pressure cost while retaining
the same two warmup steps and five ten-step windows as the hydrostatic runs.

`pressure_check_true_residual: true` independently recomputes the final
pressure residual outside the timing windows and rejects a result above its
configured tolerance. Account for the last RK stage duration: the model stores
physical pressure after applying the pressure impulse, while the solver's
right-hand side belongs to the impulse equation. All accepted new nonhydrostatic
runs use this check.
The optional `pressure_preserve_residual` measures norms on a scratch copy;
it diagnoses roundoff from the native norm's in-place scaling and restoration.

Use `separate_partitions: true` when a slow layout could exhaust a shared
allocation. Each layout then receives its own allocation and time limit;
record placement because the layouts may run on different nodes. An allocation
timeout does not mean every bundled case ran: cases without a start marker are
reported as `NOT_RUN`, with the allocation outcome preserved.

Server specs can set `cpu_time_overrides` to a mapping such as
`{"1": "72:00:00", "3": "48:00:00"}` when measured nonhydrostatic costs
require longer low-rank allocations. `full_gpu_nodes: true` reserves all GPUs
on each node while the execution step assigns one GPU per MPI rank. Use it when
fractional-GPU partitions are unavailable; record allocated resources separately
from the GPUs actually used. One- and two-GPU timings still use one and two
GPUs, although their allocations reserve four on Rorqual.

Use a small CPU/GPU MPI validation run before submitting a new model's full
suite. Keep validation timings separate from production results. Package
loading/precompilation and model initialization must finish before timing;
record timeouts and memory failures rather than treating partial windows as
measurements.

```bash
python3 benchmarking/benchmark_suite.py --config benchmarking/configs/rorqual.json \
  --model NonhydrostaticModel \
  --output benchmarking/results/non_hydrostatic_free_surface_models/rorqual/2026-10-13_full_suite \
  --compare-with benchmarking/results/hydrostatic_free_surface_models/rorqual/2026-10-12_gpu_partition_and_largest_grid_rerun \
  --compare-with benchmarking/results/hydrostatic_free_surface_models/rorqual/2026-10-07_cpu_retry \
  --compare-with benchmarking/results/hydrostatic_free_surface_models/rorqual/2026-10-07_gpu_extended_suite \
  --compare-with benchmarking/results/hydrostatic_free_surface_models/rorqual/2026-10-07_full_suite \
  --comparison-report benchmarking/results/model_comparison.md --submit --watch --commit
```

`--compare-with` paths select the other model's records, with earlier paths
taking precedence for an entire series. They do not provide baselines for the
new model. `--comparison-report` saves a Markdown comparison across all ten
series and updates it on every refresh. Ratios use nonhydrostatic/hydrostatic
seconds per step: 1 means equal time, above 1 means nonhydrostatic takes longer.
Only pairs with validated timings and matching workload, partition, precision,
rank/thread counts, Δt, and timing/profiling protocol receive a ratio.
Missing or unfinished measurements remain blank. Efficiencies use each model's
own measured baseline; profile timings remain separate from unprofiled timings.

The ratio compares the full configurations, including different advection,
closure, pressure treatment, tracer sets (CATKE can add TKE), and time stepper.
It does not isolate the cost of changing only the hydrostatic approximation.
Per-case configuration links and selected-run links retain that provenance.

## Configure a server

Run commands from the repository root. Copy `configs/server.example.json` and
adjust capacities, per-node core/GPU counts, project, environment and trace
paths. For Slurm, set `backend=slurm`, CPU/GPU accounts, optional partitions,
GPU type, CPU constraint and any extra `sbatch` arguments. Capacity fields must
be explicit for Slurm. `cpu_cores_per_node` counts physical cores, not SMT
threads. Defaults request exclusive CPU nodes for controlled comparisons.

The checked-in `configs/nibi.json` uses the current repo instructions' account
`def-fpoulin`, the Nibi environment and CUDA-aware MPI initialization hook.
Its 699-node/29-GPU-node capacity bounds come from the earlier study; check
current Slurm limits and allocation policy before reuse. It leaves partition
selection to Nibi's submission policy. `--max-cpu-cores` and `--max-gpus` can
lower or update the bounds. CPU/GPU memories, time limits, cores/GPU and
submission flags are configurable in the JSON profile. Small CPU scaling
counts receive 24-hour (1/3), 12-hour (6) and 6-hour (12) limits automatically;
remaining CPU cases use `cpu_time`, GPU cases `gpu_time`, grouped partition
comparisons `partition_time`.

Instantiate/precompile the selected Julia project before MPI launches:

```bash
julia --project=benchmarking -e 'using Pkg; Pkg.instantiate(); Pkg.precompile()'
```

On Nibi, the retained compatibility setup command prepares its isolated project:

```bash
bash benchmarking/results/hydrostatic_free_surface_models/nibi/setup.sh
```

The loaded MPI library, NetCDF/HDF5 MPI dependencies and launcher must match.
For DRAC-style environments, set `mpi_init` to the provided `drac_mpi.jl`
hook. Other installations can leave it empty. The worker checks a ring exchange
before stepping, using GPU buffers for GPU cases. Local execution assumes
Open MPI's `--map-by core --bind-to core` flags; Slurm uses `srun`, requests
physical cores without SMT, and verifies actual physical-core/GPU placement.
Linux CPU affinity/topology interfaces are required by the CPU worker.

GPU allocations occupying every GPU on each node request `--mem=0`, following
Oceananigans-DRAC/docs/drac.md. Smaller allocations use the configured GPU memory.
`reference_suites` can list existing suite directories; their saved outcomes feed
the DRAC-style strong/weak comparison tables without resubmitting their jobs.
Current-series results take precedence over references, including while a new
baseline is pending: old and new runs are never mixed to compute a rerun's
efficiency. `replacement_suites` can point a report at a fresh rerun directory;
replaced series are displayed from that directory while historical raw records
and job outcomes stay in the original suite.
GPU partition plots use fastest/median MPI efficiencies relative to the measured
1×1×1 baseline, with a zero y-axis origin and a 100% ideal reference. Extreme
32-/64-GPU partitions below 23 local horizontal cells are geometry limits.
Each larger-grid strong study uses its planned 4- or 16-GPU measured baseline;
if that baseline fails, efficiency stays unavailable. Weak efficiency divides
baseline time by measured time, without dividing by the GPU count. Plots include
ideal timing and 100% efficiency references. Tables report median timings,
global throughput and measured maximum device-used GiB per GPU after timing,
including context/buffers (not peak memory); old records without this measurement
show a blank entry. Timing still uses five ten-step windows, compared with the
reference document's five 100-step windows.

## Run the full table

First generate a plan without launching computation:

```bash
python3 benchmarking/benchmark_suite.py --config benchmarking/configs/nibi.json \
  --output benchmarking/results/hydrostatic_free_surface_models/new_server/2026-10-07_full_suite --plan
```

Review the resulting configurations, then execute that plan:

```bash
python3 benchmarking/benchmark_suite.py \
  --output benchmarking/results/hydrostatic_free_surface_models/new_server/2026-10-07_full_suite --resume --watch --commit
```

Or submit the full table to Slurm in one command with a fresh directory:

```bash
python3 benchmarking/benchmark_suite.py --config benchmarking/configs/nibi.json \
  --output benchmarking/results/hydrostatic_free_surface_models/new_server/2026-10-07_full_suite --submit --watch --commit
```

For a standalone server or an existing local allocation, use a local profile:

```bash
python3 benchmarking/benchmark_suite.py --config benchmarking/configs/server.example.json \
  --output benchmarking/results/hydrostatic_free_surface_models/new_server/2026-10-07_full_suite --run --commit
```

Without a profile, local planning detects available CPU affinity and NVIDIA
GPU count. With no mode flag, it executes using the profile's backend. Set
capacities to resources assigned to you. `--series` selects a comma-separated
subset of the ten names. `--resume` executes only `PLANNED` cases and never
resubmits pending/running/completed jobs. Use a fresh directory for failed-case
retries. Each CPU partition sweep and each GPU-count partition comparison runs
sequentially in one allocation, with fresh Julia/MPI processes per case.
Other Slurm allocation groups are independent and may start in any order.

Refresh saved outcomes and plots at any time:

```bash
python3 benchmarking/benchmark_suite.py \
  --output benchmarking/results/hydrostatic_free_surface_models/new_server/2026-10-07_full_suite --refresh --watch --commit
```

Slurm submission also schedules an after-any CPU finalizer using the executable
script snapshot. `report_modules` loads Python/matplotlib modules for it.
The login monitor and finalizer share a lock; if a monitor owns the lock when
the finalizer runs, the monitor handles finalization. Commit mode requires a
configured Git identity and an output directory inside a repository. It stages
only that directory and refuses an index containing unrelated changes; it does
not push. Benchmark suite source changes and records are committed separately.

## Records and limits

- `suite.json` holds server settings, planned cases, job IDs, outcomes and
  validated statistics. `results.csv` and `plot.md` summarize all cases.
- Each case retains configuration JSON/Markdown, command, rank placement,
  actual windows and metadata, finite-state validation, and execution logs.
- `run_metadata/` snapshots executable suite code, the benchmark source,
  environment files and source revision. Queued jobs use the captured worker.
  The selected Julia project still loads its developed package paths; keep
  that checkout/revision stable until the run completes, or use an isolated
  checkout/environment per study.
- Profile captures/SQLite files stay under configured `trace_root`. Each rank
  retains CUDA kernel/API/memory, MPI and NVTX exports when available. Required
  kernel summaries and raw trace SHA-256 checksums are validated; manifests
  are saved in `raw_traces.csv`. Missing optional reports have export logs.
- Scaling plots use the measured one-rank baseline, or the planned 4-/16-GPU
  baseline for larger grids. A failed baseline leaves efficiency blank. Only
  validated completed cases enter plots. Profile timing and kernel breakdowns
  are kept in their own series.
- CPU local domains need at least seven horizontal cells; GPU extended halos
  require at least 23 for distributed cases with the current 30-substep model.
  Balanced partitions preserve all remainder cells. The 1×192×1 CPU layout
  has only 3–4 local y cells and is recorded as `GEOMETRY_LIMIT`.
- State reports distinguish configured resource bounds, geometry limits,
  submission rejection, pending queues, timeouts, failures and invalid results.
  The highest validated completed count appears per series.
- Refresh caches validated statistics. Use `--refresh --revalidate` to check
  completed files again after moving or editing artifacts.

## Script layout and historical compatibility

`benchmark_suite.py` is the main entry point. `suite/plan.py`, `suite/worker.jl`,
`suite/rank.sh` and `suite/report.py` share planning, execution and reporting.
`run_benchmarks.jl` remains the general timing/simulation/I/O command;
`generate_bathymetry.jl` and the model implementation under `src/` remain shared
utilities. Component ablation and historical Rondeau profiling retain their
compatibility launchers; they are not additional series in this ten-series table.

Older independent controllers live under `legacy/`. Thin wrappers at their
relocated `results/hydrostatic_free_surface_models/nibi/` and
`results/hydrostatic_free_surface_models/rondeau/` paths support the historical
controllers and commands. Their dependent Julia/Slurm workers
and environment setup remain in place. Historical measurements and logs are
retained; executable snapshots use the relocated paths.

Run validation without production benchmarks:

```bash
module load python/3.11 scipy-stack/2025a  # Nibi; use your server's Python elsewhere
python3 -m unittest discover -s benchmarking/tests -v
python3 -m unittest discover -s benchmarking/results/hydrostatic_free_surface_models/nibi -p 'test_*series.py'
python3 -m unittest discover -s benchmarking/results/hydrostatic_free_surface_models/nibi -p test_cpu_core_scaling.py
```

Hydrostatic benchmark runs live under `results/hydrostatic_free_surface_models/<server>/`.
Use these paths directly; the former `results/nibi` and `results/rorqual` aliases
have been removed. Queued jobs that embedded the old paths were resubmitted,
with their original scripts and job IDs preserved in `run_metadata/path_relocation.json`.
Raw historical logs retain the addresses used when those jobs ran.
