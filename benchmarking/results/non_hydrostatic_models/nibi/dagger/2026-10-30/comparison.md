# Nibi H100 baseline versus Dagger

Matched pairs run sequentially in the same allocation, alternating order by GPU count. One MPI rank and one Julia computation thread per assigned H100. Dagger submits and fetches one synchronized task per timing window on the current process/thread.

Two untimed steps, then five ten-step windows. Fastest and median seconds/step are the maximum across ranks of each rank statistic. Speedup = baseline / Dagger; ideal equal time = 1. Only completed validated pairs with matching configurations enter comparisons. Each variant uses its measured one-GPU baseline for strong-scaling efficiency.

| Series | GPUs | Global resolution | MPI partition | Grid | Baseline | Dagger | Median s/step baseline / Dagger | Speedup |
|---|---:|---|---|---|---|---|---|---:|
| gpu_scaling_fine | 16 | 720x360x100 | 4x4x1 | LatitudeLongitudeGrid | PENDING | PENDING | — | — |
| gpu_scaling_fine | 1 | 720x360x100 | 1x1x1 | LatitudeLongitudeGrid | PENDING | PENDING | — | — |
| gpu_scaling_fine | 2 | 720x360x100 | 2x1x1 | LatitudeLongitudeGrid | PENDING | PENDING | — | — |
| gpu_scaling_fine | 4 | 720x360x100 | 2x2x1 | LatitudeLongitudeGrid | PENDING | PENDING | — | — |
| gpu_scaling_fine | 8 | 720x360x100 | 4x2x1 | LatitudeLongitudeGrid | PENDING | PENDING | — | — |
| gpu_scaling_super_fine | 16 | 1440x720x200 | 4x4x1 | LatitudeLongitudeGrid | PENDING | PENDING | — | — |
| gpu_scaling_super_fine | 1 | 1440x720x200 | 1x1x1 | LatitudeLongitudeGrid | PENDING | PENDING | — | — |
| gpu_scaling_super_fine | 2 | 1440x720x200 | 2x1x1 | LatitudeLongitudeGrid | PENDING | PENDING | — | — |
| gpu_scaling_super_fine | 4 | 1440x720x200 | 2x2x1 | LatitudeLongitudeGrid | PENDING | PENDING | — | — |
| gpu_scaling_super_fine | 8 | 1440x720x200 | 4x2x1 | LatitudeLongitudeGrid | PENDING | PENDING | — | — |
