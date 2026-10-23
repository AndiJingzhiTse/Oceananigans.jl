# Rondeau: nonhydrostatic baseline versus Dagger

Dagger submits one task per timing window, restricted to the current MPI process and its sole Julia computation thread. Oceananigans retains its existing MPI domain decomposition. Both paths synchronize CUDA before completing a window.

Speedup = baseline seconds per step / Dagger seconds per step. Above 1 favors Dagger; the equal-time reference is 1. Fastest and median timings are the maximum rank statistic. Only completed, validated pairs with matching configurations have ratios.

Nsight timings are compared only against the matching profiled variant. Shared-machine activity can affect timings; these are paired runs, not exclusive-node measurements.

Raw study and execution logs: `/local_scratch/ajtse/benchmark_studies/non_hydrostatic_models/2026-10-23-rondeau-small/rondeau`.

[Baseline records](baseline/plot.md) · [Dagger records](dagger/plot.md) · [All outcomes as CSV](comparison.csv)

Requested GPU weak-scaling sequence: 360 × 180 × 50 on 1 GPU, 720 × 360 × 100 on 2 GPUs, and 1440 × 720 × 200 on 4 GPUs. Cells/GPU are 3,240,000, 12,960,000 and 51,840,000: this increases work per GPU. Efficiency uses a linear cell-count reference, not constant-work weak efficiency.

## gpu_weak_scaling

| Case | Resolution / partition | Baseline outcome | Dagger outcome | Median s/step baseline / Dagger | Speedup |
|---|---|---|---|---:|---:|
| 1_ranks | 360x180x50 / 1x1x1 | RUNNING | PLANNED | — | — |
| 2_ranks | 720x360x100 / 2x1x1 | PLANNED | PLANNED | — | — |
| 4_ranks | 1440x720x200 / 2x2x1 | PLANNED | PLANNED | — | — |

No completed, validated pair is available.

1_ranks: baseline: Local allocation started; see job.out; dagger:

2_ranks: baseline: ; dagger:

4_ranks: baseline: ; dagger:

## gpu_scaling_fine

| Case | Resolution / partition | Baseline outcome | Dagger outcome | Median s/step baseline / Dagger | Speedup |
|---|---|---|---|---:|---:|
| 1_ranks | 720x360x100 / 1x1x1 | PLANNED | PLANNED | — | — |
| 2_ranks | 720x360x100 / 2x1x1 | PLANNED | PLANNED | — | — |
| 4_ranks | 720x360x100 / 2x2x1 | PLANNED | PLANNED | — | — |

No completed, validated pair is available.

1_ranks: baseline: ; dagger:

2_ranks: baseline: ; dagger:

4_ranks: baseline: ; dagger:

## gpu_nsight_scaling_default

| Case | Resolution / partition | Baseline outcome | Dagger outcome | Median s/step baseline / Dagger | Speedup |
|---|---|---|---|---:|---:|
| 1_ranks | 360x180x50 / 1x1x1 | PLANNED | PLANNED | — | — |
| 2_ranks | 360x180x50 / 2x1x1 | PLANNED | PLANNED | — | — |
| 4_ranks | 360x180x50 / 2x2x1 | PLANNED | PLANNED | — | — |

No completed, validated pair is available.

1_ranks: baseline: ; dagger:

2_ranks: baseline: ; dagger:

4_ranks: baseline: ; dagger:

## gpu_resolution

| Case | Resolution / partition | Baseline outcome | Dagger outcome | Median s/step baseline / Dagger | Speedup |
|---|---|---|---|---:|---:|
| default | 360x180x50 / 1x1x1 | PLANNED | PLANNED | — | — |
| fine | 720x360x100 / 1x1x1 | PLANNED | PLANNED | — | — |
| super_fine | 1440x720x200 / 1x1x1 | PLANNED | PLANNED | — | — |

No completed, validated pair is available.

default: baseline: ; dagger:

fine: baseline: ; dagger:

super_fine: baseline: ; dagger:

## cpu_mpiscaling_default

| Case | Resolution / partition | Baseline outcome | Dagger outcome | Median s/step baseline / Dagger | Speedup |
|---|---|---|---|---:|---:|
| 128_ranks | 360x180x50 / 8x16x1 | PLANNED | PLANNED | — | — |
| 16_ranks | 360x180x50 / 4x4x1 | PLANNED | PLANNED | — | — |
| 1_ranks | 360x180x50 / 1x1x1 | PLANNED | PLANNED | — | — |
| 2_ranks | 360x180x50 / 2x1x1 | PLANNED | PLANNED | — | — |
| 32_ranks | 360x180x50 / 8x4x1 | PLANNED | PLANNED | — | — |
| 4_ranks | 360x180x50 / 2x2x1 | PLANNED | PLANNED | — | — |
| 64_ranks | 360x180x50 / 8x8x1 | PLANNED | PLANNED | — | — |
| 8_ranks | 360x180x50 / 4x2x1 | PLANNED | PLANNED | — | — |

No completed, validated pair is available.

128_ranks: baseline: ; dagger:

16_ranks: baseline: ; dagger:

1_ranks: baseline: ; dagger:

2_ranks: baseline: ; dagger:

32_ranks: baseline: ; dagger:

4_ranks: baseline: ; dagger:

64_ranks: baseline: ; dagger:

8_ranks: baseline: ; dagger:

## cpu_partition_default

| Case | Resolution / partition | Baseline outcome | Dagger outcome | Median s/step baseline / Dagger | Speedup |
|---|---|---|---|---:|---:|
| 128x1x1 |  /  | GEOMETRY_LIMIT | GEOMETRY_LIMIT | — | — |
| 16x8x1 | 360x180x50 / 16x8x1 | PLANNED | PLANNED | — | — |
| 1x128x1 |  /  | GEOMETRY_LIMIT | GEOMETRY_LIMIT | — | — |
| 2x64x1 |  /  | GEOMETRY_LIMIT | GEOMETRY_LIMIT | — | — |
| 32x4x1 | 360x180x50 / 32x4x1 | PLANNED | PLANNED | — | — |
| 4x32x1 |  /  | GEOMETRY_LIMIT | GEOMETRY_LIMIT | — | — |
| 64x2x1 |  /  | GEOMETRY_LIMIT | GEOMETRY_LIMIT | — | — |
| 8x16x1 | 360x180x50 / 8x16x1 | PLANNED | PLANNED | — | — |

No completed, validated pair is available.

128x1x1: baseline: Partition [128, 1, 1] has fewer than 7 local cells per horizontal direction; dagger: Partition [128, 1, 1] has fewer than 7 local cells per horizontal direction

16x8x1: baseline: ; dagger:

1x128x1: baseline: Partition [1, 128, 1] has fewer than 7 local cells per horizontal direction; dagger: Partition [1, 128, 1] has fewer than 7 local cells per horizontal direction

2x64x1: baseline: Partition [2, 64, 1] has fewer than 7 local cells per horizontal direction; dagger: Partition [2, 64, 1] has fewer than 7 local cells per horizontal direction

32x4x1: baseline: ; dagger:

4x32x1: baseline: Partition [4, 32, 1] has fewer than 7 local cells per horizontal direction; dagger: Partition [4, 32, 1] has fewer than 7 local cells per horizontal direction

64x2x1: baseline: Partition [64, 2, 1] has fewer than 7 local cells per horizontal direction; dagger: Partition [64, 2, 1] has fewer than 7 local cells per horizontal direction

8x16x1: baseline: ; dagger:

## cpu_resolution

| Case | Resolution / partition | Baseline outcome | Dagger outcome | Median s/step baseline / Dagger | Speedup |
|---|---|---|---|---:|---:|
| default | 360x180x50 / 1x1x1 | PLANNED | PLANNED | — | — |
| fine | 720x360x100 / 1x1x1 | PLANNED | PLANNED | — | — |
| super_fine | 1440x720x200 / 1x1x1 | PLANNED | PLANNED | — | — |

No completed, validated pair is available.

default: baseline: ; dagger:

fine: baseline: ; dagger:

super_fine: baseline: ; dagger:

