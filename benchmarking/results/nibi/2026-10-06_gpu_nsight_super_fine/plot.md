# Nsight Systems — super-fine GPU series

Global resolution: **1440 × 720 × 200**. Grid type: **LatitudeLongitudeGrid**. Float64, one MPI rank per GPU.
CUDA, NVTX and OpenMPI traces; capture starts after two untimed steps and covers five ten-step timing windows.
Model: WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3, Δt=60 s, requested free-surface substeps=30, extend_halos=true.
The layouts for each GPU count run sequentially on the same allocated GPU set, with fresh Julia/MPI processes.
Profiled timings include instrumentation overhead and are separate from the existing unprofiled scaling series.

| GPUs | Partition | Resolution | Grid type | Job | State | Profiled fastest s/step | Median s/step | Details |
|---:|---|---|---|---|---|---:|---:|---|
| 1 | 1x1x1 | 1440x720x200 | LatitudeLongitudeGrid | 23324756 | PENDING | — | — | (Priority); estimated start N/A America/Toronto |
| 2 | 2x1x1 | 1440x720x200 | LatitudeLongitudeGrid | 23324758 | PENDING | — | — | (Priority); estimated start N/A America/Toronto |
| 2 | 1x2x1 | 1440x720x200 | LatitudeLongitudeGrid | 23324758 | PENDING | — | — | (Priority); estimated start N/A America/Toronto |
| 4 | 4x1x1 | 1440x720x200 | LatitudeLongitudeGrid | 23324759 | PENDING | — | — | (Priority); estimated start N/A America/Toronto |
| 4 | 2x2x1 | 1440x720x200 | LatitudeLongitudeGrid | 23324759 | PENDING | — | — | (Priority); estimated start N/A America/Toronto |
| 4 | 1x4x1 | 1440x720x200 | LatitudeLongitudeGrid | 23324759 | PENDING | — | — | (Priority); estimated start N/A America/Toronto |

Kernel categories follow the existing Rondeau Nsight grouping: hydrostatic Gc (tracers), Gu, Gv, and all other kernels.
Fractions use summed GPU kernel duration across ranks, not elapsed wall time. Concurrent activities may overlap; MPI CPU durations cannot be added to GPU durations to form a wall-time percentage.
Every rank retains CUDA kernel/API/memory, MPI and NVTX summaries when those events are available. Missing optional MPI/NVTX reports are recorded in their export logs.
Raw .nsys-rep traces and exported SQLite databases live in scratch; completed cases have raw_traces.csv with paths, sizes and SHA-256 checksums. Text summaries and timing/configuration metadata are committed here.

[Nsight capture and MPI profiling documentation](https://docs.nvidia.com/nsight-systems/UserGuide/index.html)
