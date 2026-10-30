# Benchmark suite

HydrostaticFreeSurfaceModel; LatitudeLongitudeGrid without bathymetry; Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=60 s on the standard grids; larger horizontal grids reduce Δt in proportion to grid spacing (see each configuration).
30 requested free-surface substeps.
Actual timing protocols: 2 untimed steps, 5 windows of 10 steps.
One MPI rank per CPU core or GPU, one Julia computation thread per rank. CPU extended halos=false; GPU=true.
Window boundaries synchronize MPI ranks and GPUs. Fastest/median statistics use the maximum across ranks.
Strong efficiency = baseline time × baseline ranks / (time × ranks); weak efficiency = baseline time / time.
For gpu_weak_scaling on Rondeau, cells/GPU increase 1:4:16; efficiency = (baseline time / time) × (cells/GPU / baseline cells/GPU). This is a linear cell-count reference, not constant-work weak scaling.
Standard baselines use one rank; the larger GPU grids use 4 and 16 ranks. Missing baselines have no efficiency estimate.
Reference lines show ideal inverse-rank strong timing, constant weak timing, and 100% efficiency.
Resolution plots show previous-grid / next-grid time; doubling each grid dimension ideally gives 1/8.
Profiled timings are separate; Nsight captures CUDA/NVTX/MPI after warmup. Kernel shares sum durations across ranks, not elapsed wall time.

## gpu_scaling_fine

Highest completed count: **0 ranks**.

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |
|---|---:|---|---|---|---|---:|---:|---|---|
| 1_ranks | 1 | 1x1x1 | 720x360x100 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 2_ranks | 2 | 2x1x1 | 720x360x100 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 4_ranks | 4 | 2x2x1 | 720x360x100 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 8_ranks | 8 | 4x2x1 | 720x360x100 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |
| 16_ranks | 16 | 4x4x1 | 720x360x100 | LatitudeLongitudeGrid | PENDING | — | — | — | (Dependency); estimated start N/A (scheduler timezone) |

## GPU scaling comparison (DRAC table format)

Timing protocols are recorded per case. Tables use median seconds per step.
LatitudeLongitudeGrid; partitions are Px × Py × Pz. Nodes are measured from rank placement.
Throughput = global interior cells / median step time. Memory is maximum device-used GiB across ranks after timing, including CUDA context and buffers; it is not peak memory.
Missing memory measurements and unfinished timings are shown as —.

### Strong scaling

Strong efficiency = baseline time × baseline GPUs / (measured time × GPUs); ideal = 100%. Baselines: fine 1 GPUs.

| Grid | Global resolution (cells) | GPUs | Nodes | Partition | Δt (s) | Median s/step | Efficiency | Throughput (cells/s) | Memory/GPU (GiB) | State |
|---|---|---:|---:|---|---:|---:|---:|---:|---:|---|
| fine | 720 × 360 × 100 (25,920,000) | 1 | — | 1 × 1 × 1 | 60 | — | — | — | — | PENDING |
| fine | 720 × 360 × 100 (25,920,000) | 2 | — | 2 × 1 × 1 | 60 | — | — | — | — | PENDING |
| fine | 720 × 360 × 100 (25,920,000) | 4 | — | 2 × 2 × 1 | 60 | — | — | — | — | PENDING |
| fine | 720 × 360 × 100 (25,920,000) | 8 | — | 4 × 2 × 1 | 60 | — | — | — | — | PENDING |
| fine | 720 × 360 × 100 (25,920,000) | 16 | — | 4 × 4 × 1 | 60 | — | — | — | — | PENDING |

