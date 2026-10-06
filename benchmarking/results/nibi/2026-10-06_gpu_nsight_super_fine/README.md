# Nsight Systems GPU partition series

New series on Nibi, independent of the existing GPU scaling/partition runs.
Global resolution: **1440 × 720 × 200**, grid name **super_fine**, grid type
**LatitudeLongitudeGrid**, Float64. One MPI rank and one Julia thread per H100.

| GPUs | MPI partition | Local resolution per rank |
|---:|---|---|
| 1 | 1×1×1 | 1440×720×200 |
| 2 | 2×1×1 | 720×720×200 |
| 2 | 1×2×1 | 1440×360×200 |
| 4 | 4×1×1 | 360×720×200 |
| 4 | 2×2×1 | 720×360×200 |
| 4 | 1×4×1 | 1440×180×200 |

Three single-node allocations request 1, 2 and 4 H100s respectively,
8 host cores per GPU and 128 GiB host memory per allocation. Time limits:
30, 45 and 60 minutes. Cases within each allocation run sequentially on
its GPU set, with fresh Julia/MPI processes. Slurm schedules these allocations
independently. Exact submission commands and scheduler job settings are saved.

The model uses WENOVectorInvariantDefault momentum advection, WENO7 tracer
advection, CATKE, T/S tracers, SplitRungeKutta3, Δt=60 s and 30 requested
free-surface substeps with extended halos. It matches the prior GPU study.

Nsight Systems captures CUDA, NVTX and OpenMPI activity on every rank, giving
17 separate traces across six cases. Initialization, GPU/MPI checks, and two
untimed steps occur before CUDA profiler start markers. Collection covers five
ten-step timing windows and timing-helper finalization; finite-state checks and
JSON output occur after stop markers. A window is a timed block of ten model
steps. Fastest/median timings select the fastest/median of five windows, divided
by ten; the series reports the slowest rank's statistic for each case.
Profiled timings include instrumentation overhead.

Raw `.nsys-rep` and SQLite files stay under
`/scratch/anditse/nsight_traces/2026-10-06_gpu_nsight_super_fine/`.
Each completed case records paths, sizes and SHA-256 checksums in `raw_traces.csv`.
Rank folders retain profiler logs and CSV summaries for kernels, CUDA API,
memory transfers, MPI and NVTX (when available). Optional missing reports have
export logs and exit codes. A valid case requires complete rank timings,
finite model fields, distinct GPUs, raw traces and nonempty CUDA kernel summaries.

[Live report](plot.md) records all configurations, job outcomes, timings and a
kernel-duration breakdown plot once traces finish. Fractions sum kernel durations
across ranks; they are not wall-time percentages. An after-any CPU finalizer and
login-host monitor regenerate reports and commit completed outcomes.

```bash
python3 benchmarking/results/nibi/nsight_series.py benchmarking/results/nibi/2026-10-06_gpu_nsight_super_fine --submit
module load python/3.11 scipy-stack/2025a
python3 benchmarking/results/nibi/nsight_series.py benchmarking/results/nibi/2026-10-06_gpu_nsight_super_fine --watch --commit
```

[Official Nsight Systems capture and MPI documentation](https://docs.nvidia.com/nsight-systems/UserGuide/index.html).
