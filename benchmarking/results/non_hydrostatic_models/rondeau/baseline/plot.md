# baseline benchmarks

Each series folder contains its configurations, measurements and provenance. Only completed measurements appear in timing tables and plots.

| Series | Completed cases | Report |
|---|---:|---|
| `cpu_mpi_scaling_super_fine` | 1 | [Details](cpu_mpi_scaling_super_fine/plot.md) |
| `gpu_partition_super_fine` | 3 | [Details](gpu_partition_super_fine/plot.md) |
| `gpu_resolution` | 2 | [Details](gpu_resolution/plot.md) |

## cpu_mpi_scaling_super_fine

![cpu_mpi_scaling_super_fine](cpu_mpi_scaling_super_fine/cpu_mpi_scaling_super_fine.svg)

| Case | Ranks | Global resolution | Partition | Fastest / median s per step | Median MPI efficiency | Validation |
|---|---:|---|---|---:|---:|---|
| [96_ranks](cpu_mpi_scaling_super_fine/96_ranks/configuration.md) | 96 | 1440 × 720 × 200 | 12 × 8 × 1 | 400.382148 / 435.539057 | — | Current suite checks |

## gpu_partition_super_fine

![gpu_partition_super_fine](gpu_partition_super_fine/gpu_partition_super_fine.svg)

| Case | Ranks | Global resolution | Partition | Fastest / median s per step | Median MPI efficiency | Validation |
|---|---:|---|---|---:|---:|---|
| [1x2x1](gpu_partition_super_fine/1x2x1/configuration.md) | 2 | 1440 × 720 × 200 | 1 × 2 × 1 | 89.194775 / 94.371561 | — | Current suite checks |
| [1x4x1](gpu_partition_super_fine/1x4x1/configuration.md) | 4 | 1440 × 720 × 200 | 1 × 4 × 1 | 74.195676 / 98.142010 | — | Current suite checks |
| [4x1x1](gpu_partition_super_fine/4x1x1/configuration.md) | 4 | 1440 × 720 × 200 | 4 × 1 × 1 | 141.924302 / 147.908429 | — | Current suite checks |

## gpu_resolution

![gpu_resolution](gpu_resolution/gpu_resolution.svg)

| Case | Ranks | Global resolution | Partition | Fastest / median s per step | Median MPI efficiency | Validation |
|---|---:|---|---|---:|---:|---|
| [default](gpu_resolution/default/configuration.md) | 1 | 360 × 180 × 50 | 1 × 1 × 1 | 1.160721 / 1.398244 | — | Current suite checks |
| [fine](gpu_resolution/fine/configuration.md) | 1 | 720 × 360 × 100 | 1 × 1 × 1 | 10.094606 / 10.642403 | — | Current suite checks |
