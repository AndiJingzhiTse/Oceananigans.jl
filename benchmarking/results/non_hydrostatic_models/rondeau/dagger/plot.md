# dagger benchmarks

Each series folder contains its configurations, measurements and provenance. Only completed measurements appear in timing tables and plots.

| Series | Completed cases | Report |
|---|---:|---|
| `gpu_scaling_fine` | 2 | [Details](gpu_scaling_fine/plot.md) |
| `gpu_weak_scaling` | 2 | [Details](gpu_weak_scaling/plot.md) |

## gpu_scaling_fine

![gpu_scaling_fine](gpu_scaling_fine/gpu_scaling_fine.svg)

| Case | Ranks | Global resolution | Partition | Fastest / median s per step | Median MPI efficiency | Validation |
|---|---:|---|---|---:|---:|---|
| [1_ranks](gpu_scaling_fine/1_ranks/configuration.md) | 1 | 720 × 360 × 100 | 1 × 1 × 1 | 3.618161 / 4.177695 | 100.0% | Current suite checks |
| [2_ranks](gpu_scaling_fine/2_ranks/configuration.md) | 2 | 720 × 360 × 100 | 2 × 1 × 1 | 7.743739 / 8.343843 | 25.0% | Current suite checks |

## gpu_weak_scaling

![gpu_weak_scaling](gpu_weak_scaling/gpu_weak_scaling.svg)

| Case | Ranks | Global resolution | Partition | Fastest / median s per step | Median MPI efficiency | Validation |
|---|---:|---|---|---:|---:|---|
| [1_ranks](gpu_weak_scaling/1_ranks/configuration.md) | 1 | 360 × 180 × 50 | 1 × 1 × 1 | 0.341672 / 0.379911 | 100.0% | Current suite checks |
| [2_ranks](gpu_weak_scaling/2_ranks/configuration.md) | 2 | 720 × 360 × 100 | 2 × 1 × 1 | 7.510817 / 8.359179 | 18.2% | Current suite checks |
