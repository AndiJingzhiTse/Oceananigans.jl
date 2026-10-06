# Nibi GPU strong scaling

This sweep runs the global **1440 × 720 × 200** earth-ocean model on
1, 2, 4, 8, 16, 32, … NVIDIA H100 GPUs, with one MPI rank per GPU.
It matches `../rondeau/2026-09-27_all/gpu_scaling_super_fine` except for
the requested vertical resolution and Nibi's hardware/software environment.

The [2026-10-05 run report](2026-10-05_gpu_scaling/README.md) records the
measurements, missing queued counts, and the limits encountered.
The [follow-up status](2026-10-05_gpu_scaling/retry_status.md) tracks
the subsequent 8-, 16-, 64-, and 128-GPU attempts.

Settings: latitude–longitude without bathymetry, Float64,
WENOVectorInvariantDefault momentum, WENO7 tracers, CATKE, T/S,
SplitRungeKutta3, Δt = 60 s, two warmup steps, five windows of ten steps.
All counts, including one GPU, use `Distributed(GPU())`.

## Run

From the Oceananigans checkout, on a Nibi login node:

```bash
bash benchmarking/results/nibi/setup.sh
python3 benchmarking/results/nibi/scaling.py \
    benchmarking/results/nibi/2026-10-05_gpu_scaling --account=def-fpoulin_gpu
module load python/3.11 scipy-stack/2025a
python3 benchmarking/results/nibi/plot_scaling.py \
    benchmarking/results/nibi/2026-10-05_gpu_scaling
```

`DRAC_ROOT` defaults to `$HOME/Oceananigans-DRAC`. Its `env/nibi.sh` loads
the modules and selects the scratch depot. Setup creates an ignored
`environment/`, develops this checkout and its benchmark package, restricts
OpenMPI_jll to 4.1, and redirects both MPI.jl and OpenMPI_jll to the module's
system MPI. `run_benchmark.jl` loads NetCDF first, then calls the documented
`drac_mpi_init()` to repair `OPAL_PREFIX` before MPI initialization.
See [the Nibi guide](../../../../Oceananigans-DRAC/docs/nibi.md) in the
adjacent Oceananigans-DRAC checkout.

The controller normally submits one job at a time. `--submit-only` queues all
requested counts first; rerun without that flag to monitor and validate them.
Jobs use up to eight GPUs per node,
eight CPUs per rank, and 45 minutes per job. Full GPU nodes request `--mem=0`;
partial nodes request 64 GiB host memory. Horizontal partitions are balanced
and divide both global dimensions exactly; the 1/2/4-GPU partitions match
the reference. At each count, a GPU UUID check and a CUDA-aware MPI ring
exchange must pass before benchmarking.

`attempts.csv` records submission failures and Slurm state/exit code/reason.
Each count retains submission output, job log, accounting record, hardware,
modules, revision, raw per-rank JSON, and the suite's Markdown report.
The sweep stops at the first failure. Repeating the command resumes live jobs,
skips completed counts after validating every rank, and retries failed counts.
Use `--counts=...` to restrict a retry. Scheduler wait is kept distinct from
benchmark failure; the controller does not call a queued job a failed run.
Previous attempt files are archived under `previous_attempts/<job_id>/`
before a retry. `--time-limit=00:20:00` overrides the default wall time.

To queue and monitor independent counts concurrently:

```bash
python3 benchmarking/results/nibi/scaling.py \
    benchmarking/results/nibi/2026-10-05_gpu_scaling \
    --counts=8,16,64,128 --time-limit=00:20:00 --submit-only
module load python/3.11 scipy-stack/2025a
python3 benchmarking/results/nibi/refresh_scaling.py \
    benchmarking/results/nibi/2026-10-05_gpu_scaling --watch --commit
```

The refresher updates `retry_status.md`, validates completed jobs, and
regenerates the plot. `--commit` creates a local commit when all selected
jobs have terminated, provided the branch is unchanged and the index is
clear. It does not push. `finalize.sbatch` can run the same refresher with
an `afterany` dependency on all GPU jobs so finalization survives logout.

The plot uses `T₁ / (N × Tₙ) × 100%`, with the slowest rank's fastest window
as in the reference. It also shows median-based efficiency and timing spread.
Only completed jobs with valid results from every rank enter the plot.
The benchmark suite retains window aggregates rather than individual windows.

The run report records the highest measured GPU count and the observed reason
the next count could not complete. Resource feasibility, queue state, and
application errors are reported separately.

## Four-GPU partition comparison

The [super-fine partition series](2026-10-06_gpu_partition_super_fine/README.md)
compares `4x1x1`, `2x2x1`, and `1x4x1` at fixed **1440×720×200** resolution.
All three run sequentially on the same four H100 GPUs on one node, using
fresh Julia/MPI processes and the same model and timing settings as above.
The whole allocation requests 32 CPUs, 64 GiB host RAM, and 30 minutes.

```bash
python3 benchmarking/results/nibi/partition_series.py \
    benchmarking/results/nibi/2026-10-06_gpu_partition_super_fine --submit
module load python/3.11 scipy-stack/2025a
python3 benchmarking/results/nibi/partition_series.py \
    benchmarking/results/nibi/2026-10-06_gpu_partition_super_fine --watch --commit
```

Each partition retains separate raw results and logs. The report compares
fastest and median times and speedup relative to the fresh `2x2x1` case.
`finalize_partitions.sbatch` can regenerate the report and commit validated
results with an `afterany` dependency on the allocation. A failed case is
recorded and the series proceeds to the remaining cases when possible.

Validate the reporting code with:

```bash
module load python/3.11 scipy-stack/2025a
python3 -m unittest discover -s benchmarking/results/nibi -p test_partition_series.py
```

## Historical CPU super-fine scaling and partition comparison

A CPU means a full Nibi compute node: 192 physical cores, one MPI rank,
and 192 Julia threads. The grid is fixed at 1440×720×200. CPU settings
match the GPU model, warmup, and five ten-step timing windows.

```bash
python3 benchmarking/results/nibi/cpu_series.py benchmarking/results/nibi/2026-10-06_cpu_scaling_super_fine --submit scaling
python3 benchmarking/results/nibi/cpu_series.py benchmarking/results/nibi/2026-10-06_cpu_partition_super_fine --submit partition
module load python/3.11 scipy-stack/2025a
python3 benchmarking/results/nibi/cpu_series.py benchmarking/results/nibi/2026-10-06_cpu_scaling_super_fine --watch --commit
python3 benchmarking/results/nibi/cpu_series.py benchmarking/results/nibi/2026-10-06_cpu_partition_super_fine --watch --commit
python3 -m unittest discover -s benchmarking/results/nibi -p 'test_cpu_series.py'
```

Submission creates dependent finalizer jobs automatically. A scaling run
requests 1, 2, 4, …, 512 nodes, then the largest exact horizontal decomposition
within the CPU partition (currently 675 nodes), stopping at a submission failure. A test-only
1024-node request records the next Slurm limit; it does not create a job.
The partition comparison requests four nodes and runs 4×1×1, 2×2×1, and
1×4×1 sequentially on them. Both controllers validate MPI rank completeness,
192 threads/cores per rank, distinct nodes, grid shapes and timing statistics.
See [CPU scaling](2026-10-06_cpu_scaling_super_fine/README.md) and
[CPU partitions](2026-10-06_cpu_partition_super_fine/README.md).

## Active replacement: CPU scaling from three cores

Use [the replacement CPU core series](2026-10-06_cpu_scaling_cores_super_fine/README.md)
for new CPU scaling comparisons. It runs 3, 6, 12, 24, 48, 96, 192 cores,
then 2, 4, 8, 16, 32 and 64 full 192-core nodes, with one single-threaded
MPI rank per core and explicit pinning. Every run records MPI partition,
global/local resolution and grid type. Balanced partitions preserve the
1440×720×200 LatitudeLongitudeGrid even when dimensions divide unevenly.
The next doubling is blocked by the seven-cell local halo requirement.

```bash
python3 benchmarking/results/nibi/cpu_core_scaling.py benchmarking/results/nibi/2026-10-06_cpu_scaling_cores_super_fine --submit
module load python/3.11 scipy-stack/2025a
python3 benchmarking/results/nibi/cpu_core_scaling.py benchmarking/results/nibi/2026-10-06_cpu_scaling_cores_super_fine --watch --commit
```

The earlier whole-node, 192-thread-per-rank CPU scaling series is historical;
its unfinished jobs were cancelled when the replacement was requested.
The CPU partition comparison and GPU jobs are separate studies.
