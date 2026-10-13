# Benchmark suite

NonhydrostaticModel; rigid lid; LatitudeLongitudeGrid without bathymetry; Float64, WENO7 momentum/tracers, ScalarDiffusivity (ν=1e-3, κ=1e-5 m²/s), T/S, RungeKutta3. Pressure: ConjugateGradientPoissonSolver; traditional spherical Coriolis and TEOS10 buoyancy.
Δt=60 s on the standard grids; larger horizontal grids reduce Δt in proportion to grid spacing (see each configuration).
No free-surface substeps or extended free-surface halos.
Actual timing protocols: 2 untimed steps, 1 windows of 1 steps.
One MPI rank per CPU core or GPU, one Julia computation thread per rank. Hydrostatic geometry bounds are retained to match partitions between models.
Window boundaries synchronize MPI ranks and GPUs. Fastest/median statistics use the maximum across ranks.
Strong efficiency = baseline time × baseline ranks / (time × ranks); weak efficiency = baseline time / time.
Standard baselines use one rank; the larger GPU grids use 4 and 16 ranks. Missing baselines have no efficiency estimate.
Reference lines show ideal inverse-rank strong timing, constant weak timing, and 100% efficiency.
Resolution plots show previous-grid / next-grid time; doubling each grid dimension ideally gives 1/8.
Profiled timings are separate; Nsight captures CUDA/NVTX/MPI after warmup. Kernel shares sum durations across ranks, not elapsed wall time.

## cpu_mpi_scaling_super_fine

Highest completed count: **192 ranks**.

![cpu_mpi_scaling_super_fine](cpu_mpi_scaling_super_fine.svg)

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |
|---|---:|---|---|---|---|---:|---:|---|---|
| balanced_192 | 192 | 16x12x1 | 1440x720x200 | LatitudeLongitudeGrid | COMPLETED | 121.662908 | 121.662908 | — | Rank results, finite fields and resource placement verified |

[balanced_192 configuration](cpu_mpi_scaling_super_fine/balanced_192/configuration.md): local resolution **90–90 × 60–60 × 200**, rigid lid; free-surface substeps not applicable.
## cpu_partition_cores_super_fine

Highest completed count: **0 ranks**.

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |
|---|---:|---|---|---|---|---:|---:|---|---|
| extreme_192x1x1 | 192 | 192x1x1 | 1440x720x200 | LatitudeLongitudeGrid | RUNNING | — | — | — | Exit 0:0; None |
## gpu_scaling_super_fine

Highest completed count: **0 ranks**.

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |
|---|---:|---|---|---|---|---:|---:|---|---|
| smoke_1 | 1 | 1x1x1 | 72x36x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| smoke_2 | 2 | 2x1x1 | 72x36x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |
| super_fine_4 | 4 | 2x2x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start N/A (scheduler timezone) |

## Pressure convergence checks

Validation pilots are separate from production comparisons. Each new accepted result checks every pressure stage and the independently recomputed final residual.

| Case | Preconditioner | Recorded solves | Maximum iterations | Last residual / tolerance | Recomputed final residual | Outcome |
|---|---|---:|---:|---|---|---|
| cpu_mpi_scaling_super_fine/balanced_192 | LocalFFTPreconditioner | 10 | 317 | 1.363e-08 / 1.490e-08 | 1.374e-08 | COMPLETED |
| cpu_partition_cores_super_fine/extreme_192x1x1 | LocalFFTPreconditioner | — | — | — | — | RUNNING |
| gpu_scaling_super_fine/smoke_1 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_fine/smoke_2 | LocalFFTPreconditioner | — | — | — | — | PENDING |
| gpu_scaling_super_fine/super_fine_4 | LocalFFTPreconditioner | — | — | — | — | PENDING |

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
| validation_72x36x200 | 72 × 36 × 200 (518,400) | 1 | — | 1 × 1 × 1 | 60 | — | — | — | — | PENDING |
| validation_72x36x200 | 72 × 36 × 200 (518,400) | 2 | — | 2 × 1 × 1 | 60 | — | — | — | — | PENDING |
| super_fine | 1440 × 720 × 200 (207,360,000) | 4 | — | 2 × 2 × 1 | 60 | — | — | — | — | PENDING |

