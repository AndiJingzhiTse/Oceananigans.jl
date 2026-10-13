# GPU scaling — DRAC-style comparison

Measured values use the slowest rank’s median seconds per step. Throughput is global interior cells/median time.
Strong efficiency = Tbaseline × Nbaseline / (Tn × N). Weak efficiency = T₁/Tn; interior cells/GPU remain fixed.
GPU memory is the maximum device-used GiB across ranks after timing, including CUDA context and any cached allocations; it is not a peak model-only allocation.
Pending/failed rows retain their state and no invented measurements. [Reference methodology](../../../../../Oceananigans-DRAC/docs/drac.md).

## Strong scaling

| Resolution (cells) | GPUs | Nodes | Partition | Δt (s) | Median s/step | Efficiency | Throughput (cells/s) | Memory/GPU (GiB) | State |
|---|---:|---:|---|---:|---:|---:|---:|---:|---|
| 1440x720x200 | 1 | 1 | 1x1x1 | 60 | — | — | — | — | PENDING |
| 1440x720x200 | 2 | 1 | 2x1x1 | 60 | — | — | — | — | PENDING |
| 1440x720x200 | 4 | 1 | 4x1x1 | 60 | — | — | — | — | PENDING |
| 1440x720x200 | 8 | 1 | 8x1x1 | 60 | — | — | — | — | PENDING |
| 1440x720x200 | 16 | 2 | 16x1x1 | 60 | — | — | — | — | PENDING |
| 1440x720x200 | 32 | 4 | 32x1x1 | 60 | 0.065708 | 100.0% | 3.156e+09 | 3.49 | COMPLETED |
| 1440x720x200 | 64 | None |  | None | — | — | — | — | GEOMETRY_LIMIT |
| 2880x1440x200 | 1 | 1 | 1x1x1 | 30.0 | — | — | — | — | MEMORY_ESTIMATE_LIMIT |
| 2880x1440x200 | 2 | 1 | 2x1x1 | 30.0 | — | — | — | — | MEMORY_ESTIMATE_LIMIT |
| 2880x1440x200 | 4 | 1 | 4x1x1 | 30.0 | — | — | — | — | PENDING |
| 2880x1440x200 | 8 | 1 | 8x1x1 | 30.0 | — | — | — | — | PENDING |
| 2880x1440x200 | 16 | 2 | 16x1x1 | 30.0 | — | — | — | — | PENDING |
| 2880x1440x200 | 32 | 4 | 32x1x1 | 30.0 | 0.160913 | 100.0% | 5.155e+09 | 8.95 | COMPLETED |
| 2880x1440x200 | 64 | 8 | 64x1x1 | 30.0 | — | — | — | — | PENDING |
| 2880x1440x200 | 128 | None |  | None | — | — | — | — | GEOMETRY_LIMIT |
| 5760x2880x200 | 1 | 1 | 1x1x1 | 15.0 | — | — | — | — | MEMORY_ESTIMATE_LIMIT |
| 5760x2880x200 | 2 | 1 | 2x1x1 | 15.0 | — | — | — | — | MEMORY_ESTIMATE_LIMIT |
| 5760x2880x200 | 4 | 1 | 4x1x1 | 15.0 | — | — | — | — | MEMORY_ESTIMATE_LIMIT |
| 5760x2880x200 | 8 | 1 | 8x1x1 | 15.0 | — | — | — | — | MEMORY_ESTIMATE_LIMIT |
| 5760x2880x200 | 16 | 2 | 16x1x1 | 15.0 | — | — | — | — | PENDING |
| 5760x2880x200 | 32 | 4 | 32x1x1 | 15.0 | — | — | — | — | PENDING |
| 5760x2880x200 | 64 | 8 | 64x1x1 | 15.0 | — | — | — | — | PENDING |
| 5760x2880x200 | 128 | 16 | 128x1x1 | 15.0 | — | — | — | — | PENDING |
| 5760x2880x200 | 256 | None |  | None | — | — | — | — | GEOMETRY_LIMIT |

gpu_scaling_super_fine baseline: **32 GPUs**.

gpu_scaling_super_super_fine baseline: **32 GPUs**.
## Weak scaling

| Resolution (cells) | GPUs | Nodes | Partition | Δt (s) | Median s/step | Efficiency | Throughput (cells/s) | Memory/GPU (GiB) | State |
|---|---:|---:|---|---:|---:|---:|---:|---:|---|
| 1440x720x200 | 1 | 1 | 1x1x1 | 60 | — | — | — | — | PENDING |
| 2880x720x200 | 2 | 1 | 2x1x1 | 30.0 | — | — | — | — | PENDING |
| 2880x1440x200 | 4 | 1 | 2x2x1 | 30.0 | — | — | — | — | PENDING |
| 5760x1440x200 | 8 | 1 | 4x2x1 | 15.0 | — | — | — | — | PENDING |
| 5760x2880x200 | 16 | 2 | 4x4x1 | 15.0 | — | — | — | — | PENDING |
| 11520x2880x200 | 32 | 4 | 8x4x1 | 7.5 | — | — | — | — | PENDING |
| 11520x5760x200 | 64 | 8 | 8x8x1 | 7.5 | — | — | — | — | PENDING |
| 23040x5760x200 | 128 | 16 | 16x8x1 | 3.75 | — | — | — | — | PENDING |
| 23040x11520x200 | 256 | 32 | 16x16x1 | 3.75 | — | — | — | — | RESOURCE_LIMIT |

Full configuration, local resolutions, failure details, source revisions and job IDs are in [plot.md](plot.md) and each case directory.
Time steps decrease with the finest horizontal spacing (60, 30, 15, … s); efficiency compares wall time per model step, not equal simulated duration.
