# baseline benchmarks

Each series folder contains its configurations, measurements and provenance. Only completed measurements appear in timing tables and plots.

| Series | Completed cases | Report |
|---|---:|---|
| `gpu_resolution` | 2 | [Details](gpu_resolution/plot.md) |
| `gpu_scaling_super_fine` | 1 | [Details](gpu_scaling_super_fine/plot.md) |

## gpu_resolution

![gpu_resolution](gpu_resolution/gpu_resolution.svg)

| Case | Ranks | Global resolution | Partition | Fastest / median s per step | Median MPI efficiency | Validation |
|---|---:|---|---|---:|---:|---|
| [default](gpu_resolution/default/configuration.md) | 1 | 360 × 180 × 50 | 1 × 1 × 1 | 0.033996 / 0.034005 | — | Current suite checks |
| [fine](gpu_resolution/fine/configuration.md) | 1 | 720 × 360 × 100 | 1 × 1 × 1 | 0.248453 / 0.248570 | — | Current suite checks |

## gpu_scaling_super_fine

![gpu_scaling_super_fine](gpu_scaling_super_fine/gpu_scaling_super_fine.svg)

| Case | Ranks | Global resolution | Partition | Fastest / median s per step | Median MPI efficiency | Validation |
|---|---:|---|---|---:|---:|---|
| [2_ranks](gpu_scaling_super_fine/2_ranks/configuration.md) | 2 | 1440 × 720 × 200 | 2 × 1 × 1 | 0.950625 / 0.951745 | — | Current suite checks |
