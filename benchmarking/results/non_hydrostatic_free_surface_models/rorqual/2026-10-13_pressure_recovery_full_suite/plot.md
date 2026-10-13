# Benchmark suite

NonhydrostaticModel; rigid lid; LatitudeLongitudeGrid without bathymetry; Float64, WENO7 momentum/tracers, ScalarDiffusivity (ν=1e-3, κ=1e-5 m²/s), T/S, RungeKutta3. Pressure: ConjugateGradientPoissonSolver; traditional spherical Coriolis and TEOS10 buoyancy.
Δt=60 s on the standard grids; larger horizontal grids reduce Δt in proportion to grid spacing (see each configuration).
No free-surface substeps or extended free-surface halos.
Actual timing protocols: 2 untimed steps, 5 windows of 10 steps.
One MPI rank per CPU core or GPU, one Julia computation thread per rank. Hydrostatic geometry bounds are retained to match partitions between models.
Window boundaries synchronize MPI ranks and GPUs. Fastest/median statistics use the maximum across ranks.
Strong efficiency = baseline time × baseline ranks / (time × ranks); weak efficiency = baseline time / time.
Standard baselines use one rank; the larger GPU grids use 4 and 16 ranks. Missing baselines have no efficiency estimate.
Reference lines show ideal inverse-rank strong timing, constant weak timing, and 100% efficiency.
Resolution plots show previous-grid / next-grid time; doubling each grid dimension ideally gives 1/8.
Profiled timings are separate; Nsight captures CUDA/NVTX/MPI after warmup. Kernel shares sum durations across ranks, not elapsed wall time.

## cpu_mpi_scaling_super_fine

Highest completed count: **0 ranks**.

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |
|---|---:|---|---|---|---|---:|---:|---|---|
| 1_ranks | 1 | 1x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| 3_ranks | 3 | 3x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| 6_ranks | 6 | 3x2x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| 12_ranks | 12 | 4x3x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| 24_ranks | 24 | 6x4x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| 48_ranks | 48 | 8x6x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| 96_ranks | 96 | 12x8x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| 192_ranks | 192 | 16x12x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start 2026-10-13T16:34:48 (scheduler timezone) |
| 384_ranks | 384 | 24x16x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start 2026-10-13T17:47:21 (scheduler timezone) |
| 768_ranks | 768 | 32x24x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start 2026-10-13T16:55:15 (scheduler timezone) |
| 1536_ranks | 1536 | 32x48x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start 2026-10-13T17:02:33 (scheduler timezone) |
| 3072_ranks | 3072 | 64x48x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start 2026-10-13T18:04:00 (scheduler timezone) |
| 6144_ranks | 6144 | 96x64x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start 2026-10-13T18:00:41 (scheduler timezone) |
| 12288_ranks | 12288 | 128x96x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start 2026-10-13T16:29:01 (scheduler timezone) |
| 24576_ranks | 24576 |  | 1440x720x200 | LatitudeLongitudeGrid | GEOMETRY_LIMIT | — | — | — | 24576 ranks have no horizontal partition with at least 7 local cells per direction |
## gpu_scaling_super_fine

Highest completed count: **0 ranks**.

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |
|---|---:|---|---|---|---|---:|---:|---|---|
| 1_ranks | 1 | 1x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 2_ranks | 2 | 2x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 4_ranks | 4 | 2x2x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 8_ranks | 8 | 4x2x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 16_ranks | 16 | 4x4x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 32_ranks | 32 | 8x4x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 64_ranks | 64 | 8x8x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 128_ranks | 128 | 16x8x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 256_ranks | 256 | 16x16x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 512_ranks | 512 | 32x16x1 | 1440x720x200 | LatitudeLongitudeGrid | RESOURCE_LIMIT | — | — | — | Requires 512; configured capacity is 264 |
## cpu_resolution

Highest completed count: **0 ranks**.

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |
|---|---:|---|---|---|---|---:|---:|---|---|
| default | 1 | 1x1x1 | 360x180x50 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| fine | 1 | 1x1x1 | 720x360x100 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| super_fine | 1 | 1x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
## gpu_resolution

Highest completed count: **0 ranks**.

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |
|---|---:|---|---|---|---|---:|---:|---|---|
| default | 1 | 1x1x1 | 360x180x50 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| fine | 1 | 1x1x1 | 720x360x100 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| super_fine | 1 | 1x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
## cpu_partition_cores_super_fine

Highest completed count: **0 ranks**.

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |
|---|---:|---|---|---|---|---:|---:|---|---|
| 192x1x1 | 192 | 192x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start 2026-10-13T17:27:46 (scheduler timezone) |
| 96x2x1 | 192 | 96x2x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start 2026-10-13T17:49:23 (scheduler timezone) |
| 64x3x1 | 192 | 64x3x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start 2026-10-13T17:49:23 (scheduler timezone) |
| 48x4x1 | 192 | 48x4x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| 32x6x1 | 192 | 32x6x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| 24x8x1 | 192 | 24x8x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| 16x12x1 | 192 | 16x12x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| 12x16x1 | 192 | 12x16x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| 8x24x1 | 192 | 8x24x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| 6x32x1 | 192 | 6x32x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| 4x48x1 | 192 | 4x48x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| 3x64x1 | 192 | 3x64x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| 2x96x1 | 192 | 2x96x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| 1x192x1 | 192 | 1x192x1 | 1440x720x200 | LatitudeLongitudeGrid | GEOMETRY_LIMIT | — | — | — | Partition [1, 192, 1] has fewer than 7 local cells per horizontal direction |
## gpu_nsight_scaling_super_fine

Highest completed count: **0 ranks**.

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |
|---|---:|---|---|---|---|---:|---:|---|---|
| 1_ranks | 1 | 1x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 2_ranks | 2 | 2x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 4_ranks | 4 | 2x2x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 8_ranks | 8 | 4x2x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 16_ranks | 16 | 4x4x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 32_ranks | 32 | 8x4x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 64_ranks | 64 | 8x8x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 128_ranks | 128 | 16x8x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 256_ranks | 256 | 16x16x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 512_ranks | 512 | 32x16x1 | 1440x720x200 | LatitudeLongitudeGrid | RESOURCE_LIMIT | — | — | — | Requires 512; configured capacity is 264 |
## gpu_partition_super_fine

Highest completed count: **0 ranks**.

MPI efficiency awaits the measured 1 × 1 × 1 baseline.

![gpu_partition_super_fine](gpu_partition_super_fine.svg)

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |
|---|---:|---|---|---|---|---:|---:|---|---|
| 1x1x1 | 1 | 1x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 2x1x1 | 2 | 2x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 1x2x1 | 2 | 1x2x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 4x1x1 | 4 | 4x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 2x2x1 | 4 | 2x2x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 1x4x1 | 4 | 1x4x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 8x1x1 | 8 | 8x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 4x2x1 | 8 | 4x2x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 2x4x1 | 8 | 2x4x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 1x8x1 | 8 | 1x8x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 16x1x1 | 16 | 16x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 8x2x1 | 16 | 8x2x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 4x4x1 | 16 | 4x4x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 2x8x1 | 16 | 2x8x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 1x16x1 | 16 | 1x16x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 32x1x1 | 32 | 32x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 16x2x1 | 32 | 16x2x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 8x4x1 | 32 | 8x4x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 4x8x1 | 32 | 4x8x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 2x16x1 | 32 | 2x16x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 1x32x1 | 32 | 1x32x1 | 1440x720x200 | LatitudeLongitudeGrid | GEOMETRY_LIMIT | — | — | — | Partition [1, 32, 1] has fewer than 23 local cells per horizontal direction |
| 64x1x1 | 64 | 64x1x1 | 1440x720x200 | LatitudeLongitudeGrid | GEOMETRY_LIMIT | — | — | — | Partition [64, 1, 1] has fewer than 23 local cells per horizontal direction |
| 32x2x1 | 64 | 32x2x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 16x4x1 | 64 | 16x4x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 8x8x1 | 64 | 8x8x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 4x16x1 | 64 | 4x16x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 2x32x1 | 64 | 2x32x1 | 1440x720x200 | LatitudeLongitudeGrid | GEOMETRY_LIMIT | — | — | — | Partition [2, 32, 1] has fewer than 23 local cells per horizontal direction |
| 1x64x1 | 64 | 1x64x1 | 1440x720x200 | LatitudeLongitudeGrid | GEOMETRY_LIMIT | — | — | — | Partition [1, 64, 1] has fewer than 23 local cells per horizontal direction |
## gpu_scaling_super_super_fine

Highest completed count: **0 ranks**.

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |
|---|---:|---|---|---|---|---:|---:|---|---|
| 4_ranks | 4 | 2x2x1 | 2880x1440x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 8_ranks | 8 | 4x2x1 | 2880x1440x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 16_ranks | 16 | 4x4x1 | 2880x1440x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 32_ranks | 32 | 8x4x1 | 2880x1440x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 64_ranks | 64 | 8x8x1 | 2880x1440x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 128_ranks | 128 | 16x8x1 | 2880x1440x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 256_ranks | 256 | 16x16x1 | 2880x1440x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 512_ranks | 512 | 32x16x1 | 2880x1440x200 | LatitudeLongitudeGrid | RESOURCE_LIMIT | — | — | — | Requires 512; configured capacity is 264 |
## gpu_scaling_super_super_super_fine

Highest completed count: **0 ranks**.

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |
|---|---:|---|---|---|---|---:|---:|---|---|
| 16_ranks | 16 | 4x4x1 | 5760x2880x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 32_ranks | 32 | 8x4x1 | 5760x2880x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 64_ranks | 64 | 8x8x1 | 5760x2880x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 128_ranks | 128 | 16x8x1 | 5760x2880x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 256_ranks | 256 | 16x16x1 | 5760x2880x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 512_ranks | 512 | 32x16x1 | 5760x2880x200 | LatitudeLongitudeGrid | RESOURCE_LIMIT | — | — | — | Requires 512; configured capacity is 264 |
## gpu_weak_scaling_super_fine

Highest completed count: **0 ranks**.

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |
|---|---:|---|---|---|---|---:|---:|---|---|
| 1_ranks | 1 | 1x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 4_ranks | 4 | 2x2x1 | 2880x1440x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 16_ranks | 16 | 4x4x1 | 5760x2880x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 64_ranks | 64 | 8x8x1 | 11520x5760x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 256_ranks | 256 | 16x16x1 | 23040x11520x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 1024_ranks | 1024 | 32x32x1 | 46080x23040x200 | LatitudeLongitudeGrid | RESOURCE_LIMIT | — | — | — | Requires 1024; configured capacity is 264 |

## Pressure convergence checks

Validation pilots are separate from production comparisons. Each new accepted result checks every pressure stage and the independently recomputed final residual.

| Case | Preconditioner | Recorded solves | Maximum iterations | Last residual / tolerance | Recomputed final residual | Outcome |
|---|---|---:|---:|---|---|---|
| cpu_mpi_scaling_super_fine/1_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_mpi_scaling_super_fine/3_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_mpi_scaling_super_fine/6_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_mpi_scaling_super_fine/12_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_mpi_scaling_super_fine/24_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_mpi_scaling_super_fine/48_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_mpi_scaling_super_fine/96_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_mpi_scaling_super_fine/192_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_mpi_scaling_super_fine/384_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_mpi_scaling_super_fine/768_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_mpi_scaling_super_fine/1536_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_mpi_scaling_super_fine/3072_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_mpi_scaling_super_fine/6144_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_mpi_scaling_super_fine/12288_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_fine/1_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_fine/2_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_fine/4_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_fine/8_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_fine/16_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_fine/32_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_fine/64_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_fine/128_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_fine/256_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_fine/512_ranks | LocalFFTPreconditioner | — | — | — | — | RESOURCE_LIMIT |
| cpu_resolution/default | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_resolution/fine | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_resolution/super_fine | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_resolution/default | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_resolution/fine | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_resolution/super_fine | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_partition_cores_super_fine/192x1x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_partition_cores_super_fine/96x2x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_partition_cores_super_fine/64x3x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_partition_cores_super_fine/48x4x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_partition_cores_super_fine/32x6x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_partition_cores_super_fine/24x8x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_partition_cores_super_fine/16x12x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_partition_cores_super_fine/12x16x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_partition_cores_super_fine/8x24x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_partition_cores_super_fine/6x32x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_partition_cores_super_fine/4x48x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_partition_cores_super_fine/3x64x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| cpu_partition_cores_super_fine/2x96x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_nsight_scaling_super_fine/1_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_nsight_scaling_super_fine/2_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_nsight_scaling_super_fine/4_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_nsight_scaling_super_fine/8_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_nsight_scaling_super_fine/16_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_nsight_scaling_super_fine/32_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_nsight_scaling_super_fine/64_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_nsight_scaling_super_fine/128_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_nsight_scaling_super_fine/256_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_nsight_scaling_super_fine/512_ranks | LocalFFTPreconditioner | — | — | — | — | RESOURCE_LIMIT |
| gpu_partition_super_fine/1x1x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/2x1x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/1x2x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/4x1x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/2x2x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/1x4x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/8x1x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/4x2x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/2x4x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/1x8x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/16x1x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/8x2x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/4x4x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/2x8x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/1x16x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/32x1x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/16x2x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/8x4x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/4x8x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/2x16x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/32x2x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/16x4x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/8x8x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_partition_super_fine/4x16x1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_super_fine/4_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_super_fine/8_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_super_fine/16_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_super_fine/32_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_super_fine/64_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_super_fine/128_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_super_fine/256_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_super_fine/512_ranks | LocalFFTPreconditioner | — | — | — | — | RESOURCE_LIMIT |
| gpu_scaling_super_super_super_fine/16_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_super_super_fine/32_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_super_super_fine/64_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_super_super_fine/128_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_super_super_fine/256_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_super_super_fine/512_ranks | LocalFFTPreconditioner | — | — | — | — | RESOURCE_LIMIT |
| gpu_weak_scaling_super_fine/1_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_weak_scaling_super_fine/4_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_weak_scaling_super_fine/16_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_weak_scaling_super_fine/64_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_weak_scaling_super_fine/256_ranks | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_weak_scaling_super_fine/1024_ranks | LocalFFTPreconditioner | — | — | — | — | RESOURCE_LIMIT |

## GPU scaling comparison (DRAC table format)

Reference: Oceananigans-DRAC/docs/drac.md, section 8. These are Rorqual measurements, not the reference’s Nibi timings.
Timing protocols are recorded per case; the reference uses five 100-step windows. Tables use median seconds per step.
LatitudeLongitudeGrid; partitions are Px × Py × Pz. Nodes are measured from rank placement.
Throughput = global interior cells / median step time. Memory is maximum device-used GiB across ranks after timing, including CUDA context and buffers; it is not peak memory.
Missing memory measurements and unfinished timings are shown as —.

### Strong scaling

Strong efficiency = baseline time × baseline GPUs / (measured time × GPUs); ideal = 100%. Baselines: super_fine 1 GPU, super_super_fine 4 GPUs, super_super_super_fine 16 GPUs.

| Grid | Global resolution (cells) | GPUs | Nodes | Partition | Δt (s) | Median s/step | Efficiency | Throughput (cells/s) | Memory/GPU (GiB) | State |
|---|---|---:|---:|---|---:|---:|---:|---:|---:|---|
| super_fine | 1440 × 720 × 200 (207,360,000) | 1 | — | 1 × 1 × 1 | 60 | — | — | — | — | PENDING |
| super_fine | 1440 × 720 × 200 (207,360,000) | 2 | — | 2 × 1 × 1 | 60 | — | — | — | — | PENDING |
| super_fine | 1440 × 720 × 200 (207,360,000) | 4 | — | 2 × 2 × 1 | 60 | — | — | — | — | PENDING |
| super_fine | 1440 × 720 × 200 (207,360,000) | 8 | — | 4 × 2 × 1 | 60 | — | — | — | — | PENDING |
| super_fine | 1440 × 720 × 200 (207,360,000) | 16 | — | 4 × 4 × 1 | 60 | — | — | — | — | PENDING |
| super_fine | 1440 × 720 × 200 (207,360,000) | 32 | — | 8 × 4 × 1 | 60 | — | — | — | — | PENDING |
| super_fine | 1440 × 720 × 200 (207,360,000) | 64 | — | 8 × 8 × 1 | 60 | — | — | — | — | PENDING |
| super_fine | 1440 × 720 × 200 (207,360,000) | 128 | — | 16 × 8 × 1 | 60 | — | — | — | — | PENDING |
| super_fine | 1440 × 720 × 200 (207,360,000) | 256 | — | 16 × 16 × 1 | 60 | — | — | — | — | PENDING |
| super_super_fine | 2880 × 1440 × 200 (829,440,000) | 4 | — | 2 × 2 × 1 | 30 | — | — | — | — | PENDING |
| super_super_fine | 2880 × 1440 × 200 (829,440,000) | 8 | — | 4 × 2 × 1 | 30 | — | — | — | — | PENDING |
| super_super_fine | 2880 × 1440 × 200 (829,440,000) | 16 | — | 4 × 4 × 1 | 30 | — | — | — | — | PENDING |
| super_super_fine | 2880 × 1440 × 200 (829,440,000) | 32 | — | 8 × 4 × 1 | 30 | — | — | — | — | PENDING |
| super_super_fine | 2880 × 1440 × 200 (829,440,000) | 64 | — | 8 × 8 × 1 | 30 | — | — | — | — | PENDING |
| super_super_fine | 2880 × 1440 × 200 (829,440,000) | 128 | — | 16 × 8 × 1 | 30 | — | — | — | — | PENDING |
| super_super_fine | 2880 × 1440 × 200 (829,440,000) | 256 | — | 16 × 16 × 1 | 30 | — | — | — | — | PENDING |
| super_super_super_fine | 5760 × 2880 × 200 (3,317,760,000) | 16 | — | 4 × 4 × 1 | 15 | — | — | — | — | PENDING |
| super_super_super_fine | 5760 × 2880 × 200 (3,317,760,000) | 32 | — | 8 × 4 × 1 | 15 | — | — | — | — | PENDING |
| super_super_super_fine | 5760 × 2880 × 200 (3,317,760,000) | 64 | — | 8 × 8 × 1 | 15 | — | — | — | — | PENDING |
| super_super_super_fine | 5760 × 2880 × 200 (3,317,760,000) | 128 | — | 16 × 8 × 1 | 15 | — | — | — | — | PENDING |
| super_super_super_fine | 5760 × 2880 × 200 (3,317,760,000) | 256 | — | 16 × 16 × 1 | 15 | — | — | — | — | PENDING |

### Weak scaling

Weak efficiency = one-GPU baseline time / measured time; ideal = 100%. Interior cells/GPU = 207,360,000.

| Grid | Global resolution (cells) | GPUs | Nodes | Partition | Δt (s) | Median s/step | Efficiency | Throughput (cells/s) | Memory/GPU (GiB) | State |
|---|---|---:|---:|---|---:|---:|---:|---:|---:|---|
| super_fine | 1440 × 720 × 200 (207,360,000) | 1 | — | 1 × 1 × 1 | 60 | — | — | — | — | PENDING |
| weak_4_ranks | 2880 × 1440 × 200 (829,440,000) | 4 | — | 2 × 2 × 1 | 30 | — | — | — | — | PENDING |
| weak_16_ranks | 5760 × 2880 × 200 (3,317,760,000) | 16 | — | 4 × 4 × 1 | 15 | — | — | — | — | PENDING |
| weak_64_ranks | 11520 × 5760 × 200 (13,271,040,000) | 64 | — | 8 × 8 × 1 | 7.5 | — | — | — | — | PENDING |
| weak_256_ranks | 23040 × 11520 × 200 (53,084,160,000) | 256 | — | 16 × 16 × 1 | 3.75 | — | — | — | — | PENDING |

