# Full benchmark suite

LatitudeLongitudeGrid without bathymetry; Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=60 s on the standard grids; larger horizontal grids reduce Δt in proportion to grid spacing (see each configuration).
30 requested free-surface substeps; two untimed steps and five ten-step windows.
One MPI rank per CPU core or GPU, one Julia computation thread per rank. CPU extended halos=false; GPU=true.
Window boundaries synchronize MPI ranks and GPUs. Fastest/median statistics use the maximum across ranks.
Strong efficiency = baseline time × baseline ranks / (time × ranks); weak efficiency = baseline time / time.
Standard baselines use one rank; the larger GPU grids use 4 and 16 ranks. Missing baselines have no efficiency estimate.
Reference lines show ideal inverse-rank strong timing, constant weak timing, and 100% efficiency.
Resolution plots show previous-grid / next-grid time; doubling each grid dimension ideally gives 1/8.
Profiled timings are separate; Nsight captures CUDA/NVTX/MPI after warmup. Kernel shares sum durations across ranks, not elapsed wall time.

## gpu_partition_super_fine

Highest completed count: **16 ranks**.

![gpu_partition_super_fine](gpu_partition_super_fine.svg)

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |
|---|---:|---|---|---|---|---:|---:|---|---|
| 2x1x1 | 2 | 2x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (ReqNodeNotAvail, UnavailableNodes:rg[12602,12903,13403]); estimated start N/A (scheduler timezone) |
| 1x2x1 | 2 | 1x2x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (ReqNodeNotAvail, UnavailableNodes:rg[12602,12903,13403]); estimated start N/A (scheduler timezone) |
| 4x1x1 | 4 | 4x1x1 | 1440x720x200 | LatitudeLongitudeGrid | COMPLETED | 0.247071 | 0.249360 | — | Rank results, finite fields and resource placement verified |
| 2x2x1 | 4 | 2x2x1 | 1440x720x200 | LatitudeLongitudeGrid | COMPLETED | 0.252772 | 0.255086 | — | Rank results, finite fields and resource placement verified |
| 1x4x1 | 4 | 1x4x1 | 1440x720x200 | LatitudeLongitudeGrid | RUNNING | — | — | — | Exit 0:0; None |
| 8x1x1 | 8 | 8x1x1 | 1440x720x200 | LatitudeLongitudeGrid | COMPLETED | 0.142374 | 0.147195 | — | Rank results, finite fields and resource placement verified |
| 4x2x1 | 8 | 4x2x1 | 1440x720x200 | LatitudeLongitudeGrid | COMPLETED | 0.147079 | 0.150229 | — | Rank results, finite fields and resource placement verified |
| 2x4x1 | 8 | 2x4x1 | 1440x720x200 | LatitudeLongitudeGrid | COMPLETED | 0.150725 | 0.159511 | — | Rank results, finite fields and resource placement verified |
| 1x8x1 | 8 | 1x8x1 | 1440x720x200 | LatitudeLongitudeGrid | RUNNING | — | — | — | Exit 0:0; None |
| 16x1x1 | 16 | 16x1x1 | 1440x720x200 | LatitudeLongitudeGrid | COMPLETED | 0.089033 | 0.097464 | — | Rank results, finite fields and resource placement verified |
| 8x2x1 | 16 | 8x2x1 | 1440x720x200 | LatitudeLongitudeGrid | COMPLETED | 0.096162 | 0.097788 | — | Rank results, finite fields and resource placement verified |
| 4x4x1 | 16 | 4x4x1 | 1440x720x200 | LatitudeLongitudeGrid | COMPLETED | 0.099257 | 0.103579 | — | Rank results, finite fields and resource placement verified |
| 2x8x1 | 16 | 2x8x1 | 1440x720x200 | LatitudeLongitudeGrid | COMPLETED | 0.101643 | 0.105266 | — | Rank results, finite fields and resource placement verified |
| 1x16x1 | 16 | 1x16x1 | 1440x720x200 | LatitudeLongitudeGrid | COMPLETED | 0.111402 | 0.179838 | — | Rank results, finite fields and resource placement verified |

[4x1x1 configuration](gpu_partition_super_fine/4x1x1/configuration.md): local resolution **360–360 × 720–720 × 200**, retained free-surface substeps [21].

[2x2x1 configuration](gpu_partition_super_fine/2x2x1/configuration.md): local resolution **720–720 × 360–360 × 200**, retained free-surface substeps [21].

[8x1x1 configuration](gpu_partition_super_fine/8x1x1/configuration.md): local resolution **180–180 × 720–720 × 200**, retained free-surface substeps [21].

[4x2x1 configuration](gpu_partition_super_fine/4x2x1/configuration.md): local resolution **360–360 × 360–360 × 200**, retained free-surface substeps [21].

[2x4x1 configuration](gpu_partition_super_fine/2x4x1/configuration.md): local resolution **720–720 × 180–180 × 200**, retained free-surface substeps [21].

[16x1x1 configuration](gpu_partition_super_fine/16x1x1/configuration.md): local resolution **90–90 × 720–720 × 200**, retained free-surface substeps [21].

[8x2x1 configuration](gpu_partition_super_fine/8x2x1/configuration.md): local resolution **180–180 × 360–360 × 200**, retained free-surface substeps [21].

[4x4x1 configuration](gpu_partition_super_fine/4x4x1/configuration.md): local resolution **360–360 × 180–180 × 200**, retained free-surface substeps [21].

[2x8x1 configuration](gpu_partition_super_fine/2x8x1/configuration.md): local resolution **720–720 × 90–90 × 200**, retained free-surface substeps [21].

[1x16x1 configuration](gpu_partition_super_fine/1x16x1/configuration.md): local resolution **1440–1440 × 45–45 × 200**, retained free-surface substeps [21].
## gpu_scaling_super_super_fine

Highest completed count: **64 ranks**.

![gpu_scaling_super_super_fine](gpu_scaling_super_super_fine.svg)

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |
|---|---:|---|---|---|---|---:|---:|---|---|
| 4_ranks | 4 | 2x2x1 | 2880x1440x200 | LatitudeLongitudeGrid | RUNNING | — | — | — | Exit 0:0; None |
| 8_ranks | 8 | 4x2x1 | 2880x1440x200 | LatitudeLongitudeGrid | COMPLETED | 0.514316 | 0.517392 | — | Rank results, finite fields and resource placement verified |
| 16_ranks | 16 | 4x4x1 | 2880x1440x200 | LatitudeLongitudeGrid | COMPLETED | 0.269842 | 0.271461 | — | Rank results, finite fields and resource placement verified |
| 32_ranks | 32 | 8x4x1 | 2880x1440x200 | LatitudeLongitudeGrid | COMPLETED | 0.161687 | 0.170486 | — | Rank results, finite fields and resource placement verified |
| 64_ranks | 64 | 8x8x1 | 2880x1440x200 | LatitudeLongitudeGrid | COMPLETED | 0.109598 | 0.111415 | — | Rank results, finite fields and resource placement verified |
| 128_ranks | 128 | 16x8x1 | 2880x1440x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Nodes required for job are DOWN, DRAINED or reserved for jobs in higher priority partitions); estimated start 2026-10-08T14:35:10 (scheduler timezone) |
| 256_ranks | 256 | 16x16x1 | 2880x1440x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Nodes required for job are DOWN, DRAINED or reserved for jobs in higher priority partitions); estimated start N/A (scheduler timezone) |
| 512_ranks | 512 | 32x16x1 | 2880x1440x200 | LatitudeLongitudeGrid | RESOURCE_LIMIT | — | — | — | Requires 512; configured capacity is 264 |

[8_ranks configuration](gpu_scaling_super_super_fine/8_ranks/configuration.md): local resolution **720–720 × 720–720 × 200**, retained free-surface substeps [21].

[16_ranks configuration](gpu_scaling_super_super_fine/16_ranks/configuration.md): local resolution **720–720 × 360–360 × 200**, retained free-surface substeps [21].

[32_ranks configuration](gpu_scaling_super_super_fine/32_ranks/configuration.md): local resolution **360–360 × 360–360 × 200**, retained free-surface substeps [21].

[64_ranks configuration](gpu_scaling_super_super_fine/64_ranks/configuration.md): local resolution **360–360 × 180–180 × 200**, retained free-surface substeps [21].
## gpu_scaling_super_super_super_fine

Highest completed count: **64 ranks**.

Efficiency baseline: **16 measured ranks**.

![gpu_scaling_super_super_super_fine](gpu_scaling_super_super_super_fine.svg)

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |
|---|---:|---|---|---|---|---:|---:|---|---|
| 16_ranks | 16 | 4x4x1 | 5760x2880x200 | LatitudeLongitudeGrid | COMPLETED | 1.159040 | 1.271404 | 100.0% / 100.0% | Rank results, finite fields and resource placement verified |
| 32_ranks | 32 | 8x4x1 | 5760x2880x200 | LatitudeLongitudeGrid | COMPLETED | 0.586813 | 0.604331 | 98.8% / 105.2% | Rank results, finite fields and resource placement verified |
| 64_ranks | 64 | 8x8x1 | 5760x2880x200 | LatitudeLongitudeGrid | COMPLETED | 0.296665 | 0.346800 | 97.7% / 91.7% | Rank results, finite fields and resource placement verified |
| 128_ranks | 128 | 16x8x1 | 5760x2880x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (Priority); estimated start 2026-10-08T15:30:00 (scheduler timezone) |
| 256_ranks | 256 | 16x16x1 | 5760x2880x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (PartitionNodeLimit); estimated start N/A (scheduler timezone) |
| 512_ranks | 512 | 32x16x1 | 5760x2880x200 | LatitudeLongitudeGrid | RESOURCE_LIMIT | — | — | — | Requires 512; configured capacity is 264 |

[16_ranks configuration](gpu_scaling_super_super_super_fine/16_ranks/configuration.md): local resolution **1440–1440 × 720–720 × 200**, retained free-surface substeps [21].

[32_ranks configuration](gpu_scaling_super_super_super_fine/32_ranks/configuration.md): local resolution **720–720 × 720–720 × 200**, retained free-surface substeps [21].

[64_ranks configuration](gpu_scaling_super_super_super_fine/64_ranks/configuration.md): local resolution **720–720 × 360–360 × 200**, retained free-surface substeps [21].
## gpu_weak_scaling_super_fine

Highest completed count: **64 ranks**.

![gpu_weak_scaling_super_fine](gpu_weak_scaling_super_fine.svg)

| Case | Ranks | Partition | Global resolution | Grid type | State | Fastest s/step | Median s/step | Efficiency fastest / median | Details |
|---|---:|---|---|---|---|---:|---:|---|---|
| 1_ranks | 1 | 1x1x1 | 1440x720x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (ReqNodeNotAvail, UnavailableNodes:rg[12602,12903,13403]); estimated start N/A (scheduler timezone) |
| 4_ranks | 4 | 2x2x1 | 2880x1440x200 | LatitudeLongitudeGrid | RUNNING | — | — | — | Exit 0:0; None |
| 16_ranks | 16 | 4x4x1 | 5760x2880x200 | LatitudeLongitudeGrid | COMPLETED | 1.110443 | 1.261272 | — | Rank results, finite fields and resource placement verified |
| 64_ranks | 64 | 8x8x1 | 11520x5760x200 | LatitudeLongitudeGrid | COMPLETED | 1.176431 | 1.277216 | — | Rank results, finite fields and resource placement verified |
| 256_ranks | 256 | 16x16x1 | 23040x11520x200 | LatitudeLongitudeGrid | PENDING | — | — | — | (PartitionNodeLimit); estimated start N/A (scheduler timezone) |
| 1024_ranks | 1024 | 32x32x1 | 46080x23040x200 | LatitudeLongitudeGrid | RESOURCE_LIMIT | — | — | — | Requires 1024; configured capacity is 264 |

[16_ranks configuration](gpu_weak_scaling_super_fine/16_ranks/configuration.md): local resolution **1440–1440 × 720–720 × 200**, retained free-surface substeps [21].

[64_ranks configuration](gpu_weak_scaling_super_fine/64_ranks/configuration.md): local resolution **1440–1440 × 720–720 × 200**, retained free-surface substeps [21].

## GPU scaling comparison (DRAC table format)

Reference: Oceananigans-DRAC/docs/drac.md, section 8. These are Rorqual measurements, not the reference’s Nibi timings.
This suite uses five ten-step windows; the reference uses five 100-step windows. Tables use median seconds per step.
LatitudeLongitudeGrid; partitions are Px × Py × Pz. Nodes are measured from rank placement.
Throughput = global interior cells / median step time. Memory is maximum device-used GiB across ranks after timing, including CUDA context and buffers; it is not peak memory.
Missing memory measurements and unfinished timings are shown as —.

### Strong scaling

Strong efficiency = baseline time × baseline GPUs / (measured time × GPUs); ideal = 100%. Baselines: super_fine 1 GPU, super_super_fine 4 GPUs, super_super_super_fine 16 GPUs.

| Grid | Global resolution (cells) | GPUs | Nodes | Partition | Δt (s) | Median s/step | Efficiency | Throughput (cells/s) | Memory/GPU (GiB) | State |
|---|---|---:|---:|---|---:|---:|---:|---:|---:|---|
| super_fine | 1440 × 720 × 200 (207,360,000) | 1 | 1 | 1 × 1 × 1 | 60 | 0.965221 | 100.0% | 2.148e+08 | — | COMPLETED |
| super_fine | 1440 × 720 × 200 (207,360,000) | 2 | 1 | 2 × 1 × 1 | 60 | 0.498924 | 96.7% | 4.156e+08 | — | COMPLETED |
| super_fine | 1440 × 720 × 200 (207,360,000) | 4 | 1 | 2 × 2 × 1 | 60 | 0.255255 | 94.5% | 8.124e+08 | — | COMPLETED |
| super_fine | 1440 × 720 × 200 (207,360,000) | 8 | 2 | 4 × 2 × 1 | 60 | 0.150829 | 80.0% | 1.375e+09 | — | COMPLETED |
| super_fine | 1440 × 720 × 200 (207,360,000) | 16 | 4 | 4 × 4 × 1 | 60 | 0.107124 | 56.3% | 1.936e+09 | — | COMPLETED |
| super_fine | 1440 × 720 × 200 (207,360,000) | 32 | 8 | 8 × 4 × 1 | 60 | 0.130831 | 23.1% | 1.585e+09 | — | COMPLETED |
| super_fine | 1440 × 720 × 200 (207,360,000) | 64 | 16 | 8 × 8 × 1 | 60 | 0.088781 | 17.0% | 2.336e+09 | — | COMPLETED |
| super_fine | 1440 × 720 × 200 (207,360,000) | 128 | — | 16 × 8 × 1 | 60 | — | — | — | — | PENDING |
| super_fine | 1440 × 720 × 200 (207,360,000) | 256 | — | 16 × 16 × 1 | 60 | — | — | — | — | PENDING |
| super_super_fine | 2880 × 1440 × 200 (829,440,000) | 4 | — | 2 × 2 × 1 | 30 | — | — | — | — | RUNNING |
| super_super_fine | 2880 × 1440 × 200 (829,440,000) | 8 | 2 | 4 × 2 × 1 | 30 | 0.517392 | — | 1.603e+09 | 25.36 | COMPLETED |
| super_super_fine | 2880 × 1440 × 200 (829,440,000) | 16 | 4 | 4 × 4 × 1 | 30 | 0.271461 | — | 3.055e+09 | 14.11 | COMPLETED |
| super_super_fine | 2880 × 1440 × 200 (829,440,000) | 32 | 8 | 8 × 4 × 1 | 30 | 0.170486 | — | 4.865e+09 | 7.88 | COMPLETED |
| super_super_fine | 2880 × 1440 × 200 (829,440,000) | 64 | 16 | 8 × 8 × 1 | 30 | 0.111415 | — | 7.445e+09 | 4.77 | COMPLETED |
| super_super_fine | 2880 × 1440 × 200 (829,440,000) | 128 | — | 16 × 8 × 1 | 30 | — | — | — | — | PENDING |
| super_super_fine | 2880 × 1440 × 200 (829,440,000) | 256 | — | 16 × 16 × 1 | 30 | — | — | — | — | PENDING |
| super_super_super_fine | 5760 × 2880 × 200 (3,317,760,000) | 16 | 4 | 4 × 4 × 1 | 15 | 1.271404 | 100.0% | 2.610e+09 | 49.47 | COMPLETED |
| super_super_super_fine | 5760 × 2880 × 200 (3,317,760,000) | 32 | 8 | 8 × 4 × 1 | 15 | 0.604331 | 105.2% | 5.490e+09 | 25.87 | COMPLETED |
| super_super_super_fine | 5760 × 2880 × 200 (3,317,760,000) | 64 | 16 | 8 × 8 × 1 | 15 | 0.346800 | 91.7% | 9.567e+09 | 14.11 | COMPLETED |
| super_super_super_fine | 5760 × 2880 × 200 (3,317,760,000) | 128 | — | 16 × 8 × 1 | 15 | — | — | — | — | PENDING |
| super_super_super_fine | 5760 × 2880 × 200 (3,317,760,000) | 256 | — | 16 × 16 × 1 | 15 | — | — | — | — | PENDING |

### Weak scaling

Weak efficiency = one-GPU baseline time / measured time; ideal = 100%. Interior cells/GPU = 207,360,000.

| Grid | Global resolution (cells) | GPUs | Nodes | Partition | Δt (s) | Median s/step | Efficiency | Throughput (cells/s) | Memory/GPU (GiB) | State |
|---|---|---:|---:|---|---:|---:|---:|---:|---:|---|
| super_fine | 1440 × 720 × 200 (207,360,000) | 1 | — | 1 × 1 × 1 | 60 | — | — | — | — | PENDING |
| weak_4_ranks | 2880 × 1440 × 200 (829,440,000) | 4 | — | 2 × 2 × 1 | 30 | — | — | — | — | RUNNING |
| weak_16_ranks | 5760 × 2880 × 200 (3,317,760,000) | 16 | 4 | 4 × 4 × 1 | 15 | 1.261272 | — | 2.630e+09 | 49.47 | COMPLETED |
| weak_64_ranks | 11520 × 5760 × 200 (13,271,040,000) | 64 | 16 | 8 × 8 × 1 | 7.5 | 1.277216 | — | 1.039e+10 | 49.47 | COMPLETED |
| weak_256_ranks | 23040 × 11520 × 200 (53,084,160,000) | 256 | — | 16 × 16 × 1 | 3.75 | — | — | — | — | PENDING |

