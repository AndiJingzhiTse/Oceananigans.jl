# Full benchmark suite

LatitudeLongitudeGrid without bathymetry; Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
30 requested free-surface substeps; two untimed steps, five windows. Window lengths and Δt are recorded per case: scaling studies following DRAC use 100 steps; other cases use ten.
One MPI rank per CPU core or GPU, one Julia computation thread per rank. CPU extended halos=false; GPU=true.
Window boundaries synchronize MPI ranks and GPUs. Fastest/median statistics use the maximum across ranks.
Strong efficiency uses the smallest validated GPU/rank count in each series, identified below. Weak efficiency uses one GPU: T₁/Tₙ, with constant interior cells/GPU; missing weak baselines have no efficiency estimate.
Profiled timings are separate; Nsight captures CUDA/NVTX/MPI after warmup. Kernel shares sum durations across ranks, not elapsed wall time.

## gpu_partition_super_fine

Highest completed count: **0 ranks**.

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Δt (s) / steps per window | Details |
|---|---:|---|---|---|---|---:|---:|---|---|---|
| 2x1x1 | 2 | 2x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 10 | (Priority); estimated start N/A (scheduler timezone) |
| 1x2x1 | 2 | 1x2x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 10 | (Priority); estimated start N/A (scheduler timezone) |
| 4x1x1 | 4 | 4x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 10 | (Priority); estimated start N/A (scheduler timezone) |
| 2x2x1 | 4 | 2x2x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 10 | (Priority); estimated start N/A (scheduler timezone) |
| 1x4x1 | 4 | 1x4x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 10 | (Priority); estimated start N/A (scheduler timezone) |
| 8x1x1 | 8 | 8x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 10 | (Priority); estimated start N/A (scheduler timezone) |
| 4x2x1 | 8 | 4x2x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 10 | (Priority); estimated start N/A (scheduler timezone) |
| 2x4x1 | 8 | 2x4x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 10 | (Priority); estimated start N/A (scheduler timezone) |
| 1x8x1 | 8 | 1x8x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 10 | (Priority); estimated start N/A (scheduler timezone) |
| 16x1x1 | 16 | 16x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 10 | (Priority); estimated start N/A (scheduler timezone) |
| 8x2x1 | 16 | 8x2x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 10 | (Priority); estimated start N/A (scheduler timezone) |
| 4x4x1 | 16 | 4x4x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 10 | (Priority); estimated start N/A (scheduler timezone) |
| 2x8x1 | 16 | 2x8x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 10 | (Priority); estimated start N/A (scheduler timezone) |
| 1x16x1 | 16 | 1x16x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 10 | (Priority); estimated start N/A (scheduler timezone) |
## gpu_scaling_super_fine

Highest completed count: **0 ranks**.

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Δt (s) / steps per window | Details |
|---|---:|---|---|---|---|---:|---:|---|---|---|
| 1_ranks | 1 | 1x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 2_ranks | 2 | 2x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 4_ranks | 4 | 4x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 8_ranks | 8 | 8x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 16_ranks | 16 | 16x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 32_ranks | 32 | 32x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 64_ranks | 64 |  | 1440x720x200 | LatitudeLongitudeGrid | GEOMETRY_LIMIT | — | — | — | None / None | Partition [64, 1, 1] has fewer than 23 local cells per horizontal direction |
## gpu_scaling_super_super_fine

Highest completed count: **0 ranks**.

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Δt (s) / steps per window | Details |
|---|---:|---|---|---|---|---:|---:|---|---|---|
| 1_ranks | 1 | 1x1x1 | 2880x1440x200 | LatitudeLongitudeGrid | MEMORY_ESTIMATE_LIMIT | — | — | — | 30.0 / 100 | Not submitted: DRAC reference starts this grid at 4 H100 80 GiB GPUs; estimated device capacity insufficient below that count |
| 2_ranks | 2 | 2x1x1 | 2880x1440x200 | LatitudeLongitudeGrid | MEMORY_ESTIMATE_LIMIT | — | — | — | 30.0 / 100 | Not submitted: DRAC reference starts this grid at 4 H100 80 GiB GPUs; estimated device capacity insufficient below that count |
| 4_ranks | 4 | 4x1x1 | 2880x1440x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 30.0 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 8_ranks | 8 | 8x1x1 | 2880x1440x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 30.0 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 16_ranks | 16 | 16x1x1 | 2880x1440x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 30.0 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 32_ranks | 32 | 32x1x1 | 2880x1440x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 30.0 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 64_ranks | 64 | 64x1x1 | 2880x1440x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 30.0 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 128_ranks | 128 |  | 2880x1440x200 | LatitudeLongitudeGrid | GEOMETRY_LIMIT | — | — | — | None / None | Partition [128, 1, 1] has fewer than 23 local cells per horizontal direction |
## gpu_scaling_super_super_super_fine

Highest completed count: **0 ranks**.

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Δt (s) / steps per window | Details |
|---|---:|---|---|---|---|---:|---:|---|---|---|
| 1_ranks | 1 | 1x1x1 | 5760x2880x200 | LatitudeLongitudeGrid | MEMORY_ESTIMATE_LIMIT | — | — | — | 15.0 / 100 | Not submitted: DRAC reference starts this grid at 16 H100 80 GiB GPUs; estimated device capacity insufficient below that count |
| 2_ranks | 2 | 2x1x1 | 5760x2880x200 | LatitudeLongitudeGrid | MEMORY_ESTIMATE_LIMIT | — | — | — | 15.0 / 100 | Not submitted: DRAC reference starts this grid at 16 H100 80 GiB GPUs; estimated device capacity insufficient below that count |
| 4_ranks | 4 | 4x1x1 | 5760x2880x200 | LatitudeLongitudeGrid | MEMORY_ESTIMATE_LIMIT | — | — | — | 15.0 / 100 | Not submitted: DRAC reference starts this grid at 16 H100 80 GiB GPUs; estimated device capacity insufficient below that count |
| 8_ranks | 8 | 8x1x1 | 5760x2880x200 | LatitudeLongitudeGrid | MEMORY_ESTIMATE_LIMIT | — | — | — | 15.0 / 100 | Not submitted: DRAC reference starts this grid at 16 H100 80 GiB GPUs; estimated device capacity insufficient below that count |
| 16_ranks | 16 | 16x1x1 | 5760x2880x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 15.0 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 32_ranks | 32 | 32x1x1 | 5760x2880x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 15.0 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 64_ranks | 64 | 64x1x1 | 5760x2880x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 15.0 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 128_ranks | 128 | 128x1x1 | 5760x2880x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 15.0 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 256_ranks | 256 |  | 5760x2880x200 | LatitudeLongitudeGrid | GEOMETRY_LIMIT | — | — | — | None / None | Partition [256, 1, 1] has fewer than 23 local cells per horizontal direction |
## gpu_weak_scaling_super_fine

Highest completed count: **0 ranks**.

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Δt (s) / steps per window | Details |
|---|---:|---|---|---|---|---:|---:|---|---|---|
| 1_ranks | 1 | 1x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 60 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 2_ranks | 2 | 2x1x1 | 2880x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 30.0 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 4_ranks | 4 | 2x2x1 | 2880x1440x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 30.0 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 8_ranks | 8 | 4x2x1 | 5760x1440x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 15.0 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 16_ranks | 16 | 4x4x1 | 5760x2880x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 15.0 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 32_ranks | 32 | 8x4x1 | 11520x2880x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 7.5 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 64_ranks | 64 | 8x8x1 | 11520x5760x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 7.5 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 128_ranks | 128 | 16x8x1 | 23040x5760x200 | LatitudeLongitudeGrid | PENDING | — | — | — | 3.75 / 100 | (Priority); estimated start N/A (scheduler timezone) |
| 256_ranks | 256 | 16x16x1 | 23040x11520x200 | LatitudeLongitudeGrid | RESOURCE_LIMIT | — | — | — | 3.75 / 100 | Requires 256; configured capacity is 232 |
