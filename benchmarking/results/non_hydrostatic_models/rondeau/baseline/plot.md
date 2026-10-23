# baseline benchmarks

Each series folder contains its configurations, measurements and provenance. Only completed measurements appear in timing tables and plots.

| Series | Completed cases | Report |
|---|---:|---|
| `gpu_weak_scaling` | 2 | [Details](gpu_weak_scaling/plot.md) |

## gpu_weak_scaling

![gpu_weak_scaling](gpu_weak_scaling/gpu_weak_scaling.svg)

| Case | Ranks | Global resolution | Partition | Fastest / median s per step | Median MPI efficiency | Validation |
|---|---:|---|---|---:|---:|---|
| [1_ranks](gpu_weak_scaling/1_ranks/configuration.md) | 1 | 360 × 180 × 50 | 1 × 1 × 1 | 0.345378 / 0.383486 | 100.0% | Current suite checks |
| [2_ranks](gpu_weak_scaling/2_ranks/configuration.md) | 2 | 720 × 360 × 100 | 2 × 1 × 1 | 7.732817 / 8.453616 | 18.1% | Current suite checks |
