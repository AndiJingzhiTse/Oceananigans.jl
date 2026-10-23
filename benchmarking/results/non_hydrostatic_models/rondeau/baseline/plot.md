# baseline benchmarks

Each series folder contains its configurations, measurements and provenance. Only completed measurements appear in timing tables and plots.

| Series | Completed cases | Report |
|---|---:|---|
| `gpu_nsight_scaling_default` | 2 | [Details](gpu_nsight_scaling_default/plot.md) |
| `gpu_scaling_fine` | 3 | [Details](gpu_scaling_fine/plot.md) |
| `gpu_weak_scaling` | 2 | [Details](gpu_weak_scaling/plot.md) |

## gpu_nsight_scaling_default

![gpu_nsight_scaling_default](gpu_nsight_scaling_default/gpu_nsight_scaling_default.svg)

![gpu_nsight_scaling_default_kernels](gpu_nsight_scaling_default/gpu_nsight_scaling_default_kernels.svg)

| Case | Ranks | Global resolution | Partition | Fastest / median s per step | Median MPI efficiency | Validation |
|---|---:|---|---|---:|---:|---|
| [1_ranks](gpu_nsight_scaling_default/1_ranks/configuration.md) | 1 | 360 × 180 × 50 | 1 × 1 × 1 | 0.808531 / 1.127963 | 100.0% | Current suite checks |
| [2_ranks](gpu_nsight_scaling_default/2_ranks/configuration.md) | 2 | 360 × 180 × 50 | 2 × 1 × 1 | 1.843828 / 2.828368 | 19.9% | Current suite checks |

## gpu_scaling_fine

![gpu_scaling_fine](gpu_scaling_fine/gpu_scaling_fine.svg)

| Case | Ranks | Global resolution | Partition | Fastest / median s per step | Median MPI efficiency | Validation |
|---|---:|---|---|---:|---:|---|
| [1_ranks](gpu_scaling_fine/1_ranks/configuration.md) | 1 | 720 × 360 × 100 | 1 × 1 × 1 | 3.499310 / 4.023600 | 100.0% | Current suite checks |
| [2_ranks](gpu_scaling_fine/2_ranks/configuration.md) | 2 | 720 × 360 × 100 | 2 × 1 × 1 | 7.418771 / 8.388280 | 24.0% | Current suite checks |
| [4_ranks](gpu_scaling_fine/4_ranks/configuration.md) | 4 | 720 × 360 × 100 | 2 × 2 × 1 | 4.423683 / 4.997257 | 20.1% | Current suite checks |

## gpu_weak_scaling

![gpu_weak_scaling](gpu_weak_scaling/gpu_weak_scaling.svg)

| Case | Ranks | Global resolution | Partition | Fastest / median s per step | Median MPI efficiency | Validation |
|---|---:|---|---|---:|---:|---|
| [1_ranks](gpu_weak_scaling/1_ranks/configuration.md) | 1 | 360 × 180 × 50 | 1 × 1 × 1 | 0.345378 / 0.383486 | 100.0% | Current suite checks |
| [2_ranks](gpu_weak_scaling/2_ranks/configuration.md) | 2 | 720 × 360 × 100 | 2 × 1 × 1 | 7.732817 / 8.453616 | 18.1% | Current suite checks |
