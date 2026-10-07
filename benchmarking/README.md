# Full benchmark suite

Use **`benchmark_suite.py`** for new server studies. It runs the seven series
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
| `gpu_partition_super_fine` | 1440×720×200 | Two GPUs: 2×1×1, 1×2×1; four GPUs: 4×1×1, 2×2×1, 1×4×1 |

Scaling counts continue to the configured server capacity or the first geometry
limit. The next doubling is recorded as a resource/geometry boundary. A
configured capacity is a planning bound, not proof that those resources are
available now: submission, queue and execution outcomes are recorded separately.
A failed one-GPU allocation does not prevent trying larger GPU counts.

All cases use LatitudeLongitudeGrid without bathymetry, Float64,
WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3, Δt=60 s and
30 requested free-surface substeps. CPU cases use `extend_halos=false`; GPU
cases use `extend_halos=true`. Every rank has one Julia computation thread.
There are two untimed steps (one warmup and one helper preflight step), then
five ten-step timing windows. Windows synchronize ranks and GPUs at both
boundaries. This explicit synchronization differs from the historical helpers;
the worker records individual windows and actual retained free-surface substeps.

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
bash benchmarking/results/nibi/setup.sh
```

The loaded MPI library, NetCDF/HDF5 MPI dependencies and launcher must match.
For DRAC-style environments, set `mpi_init` to the provided `drac_mpi.jl`
hook. Other installations can leave it empty. The worker checks a ring exchange
before stepping, using GPU buffers for GPU cases. Local execution assumes
Open MPI's `--map-by core --bind-to core` flags; Slurm uses `srun`, requests
physical cores without SMT, and verifies actual physical-core/GPU placement.
Linux CPU affinity/topology interfaces are required by the CPU worker.

## Run the full table

First generate a plan without launching computation:

```bash
python3 benchmarking/benchmark_suite.py --config benchmarking/configs/nibi.json \
  --output benchmarking/results/new_server/2026-10-07_full_suite --plan
```

Review the resulting configurations, then execute that plan:

```bash
python3 benchmarking/benchmark_suite.py \
  --output benchmarking/results/new_server/2026-10-07_full_suite --resume --watch --commit
```

Or submit the full table to Slurm in one command with a fresh directory:

```bash
python3 benchmarking/benchmark_suite.py --config benchmarking/configs/nibi.json \
  --output benchmarking/results/new_server/2026-10-07_full_suite --submit --watch --commit
```

For a standalone server or an existing local allocation, use a local profile:

```bash
python3 benchmarking/benchmark_suite.py --config benchmarking/configs/server.example.json \
  --output benchmarking/results/new_server/2026-10-07_full_suite --run --commit
```

Without a profile, local planning detects available CPU affinity and NVIDIA
GPU count. With no mode flag, it executes using the profile's backend. Set
capacities to resources assigned to you. `--series` selects a comma-separated
subset of the seven names. `--resume` executes only `PLANNED` cases and never
resubmits pending/running/completed jobs. Use a fresh directory for failed-case
retries. Each CPU partition sweep and each GPU-count partition comparison runs
sequentially in one allocation, with fresh Julia/MPI processes per case.
Other Slurm allocation groups are independent and may start in any order.

Refresh saved outcomes and plots at any time:

```bash
python3 benchmarking/benchmark_suite.py \
  --output benchmarking/results/new_server/2026-10-07_full_suite --refresh --watch --commit
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
- Scaling plots use the measured one-rank baseline. A failed baseline leaves
  efficiency blank. Only validated completed cases enter plots. Profile timing
  and kernel breakdowns are kept in their own series.
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
compatibility launchers; they are not additional series in this seven-series table.

Older independent controllers live under `legacy/`. Thin wrappers at their
original `results/nibi/` and `results/rondeau/` paths preserve existing queued
jobs, finalizers and historical commands. Their dependent Julia/Slurm workers
and environment setup remain in place. Historical measurements and snapshots
have not been deleted or rewritten.

Run validation without production benchmarks:

```bash
module load python/3.11 scipy-stack/2025a  # Nibi; use your server's Python elsewhere
python3 -m unittest discover -s benchmarking/tests -v
python3 -m unittest discover -s benchmarking/results/nibi -p 'test_*series.py'
python3 -m unittest discover -s benchmarking/results/nibi -p test_cpu_core_scaling.py
```
