# rorqual benchmarks

Each series folder contains its configurations, measurements and provenance. Only completed measurements appear in timing tables and plots.

| Series | Completed cases | Report |
|---|---:|---|
| `cpu_mpi_scaling_super_fine` | 3 | [Details](cpu_mpi_scaling_super_fine/plot.md) |
| `cpu_pressure_validation` | 8 | [Details](cpu_pressure_validation/plot.md) |
| `cpu_resolution` | 1 | [Details](cpu_resolution/plot.md) |

## cpu_mpi_scaling_super_fine

![cpu_mpi_scaling_super_fine](cpu_mpi_scaling_super_fine/cpu_mpi_scaling_super_fine.svg)

| Case | Ranks | Global resolution | Partition | Fastest / median s per step | Median MPI efficiency | Validation |
|---|---:|---|---|---:|---:|---|
| [192_ranks](cpu_mpi_scaling_super_fine/192_ranks/configuration.md) | 192 | 1440 × 720 × 200 | 16 × 12 × 1 | 127.564623 / 135.670963 | — | Current suite: rank completeness, finite fields, placement and timings checked |
| [384_ranks](cpu_mpi_scaling_super_fine/384_ranks/configuration.md) | 384 | 1440 × 720 × 200 | 24 × 16 × 1 | 50.417595 / 51.516729 | — | Current suite: rank completeness, finite fields, placement and timings checked |
| [1536_ranks](cpu_mpi_scaling_super_fine/1536_ranks/configuration.md) | 1536 | 1440 × 720 × 200 | 32 × 48 × 1 | 14.147107 / 14.490786 | — | Current suite: rank completeness, finite fields, placement and timings checked |

## cpu_pressure_validation

![cpu_pressure_validation](cpu_pressure_validation/cpu_pressure_validation.svg)

| Case | Ranks | Global resolution | Partition | Fastest / median s per step | Median MPI efficiency | Validation |
|---|---:|---|---|---:|---:|---|
| [1_ranks_LocalFFTPreconditioner_72x36x200_1x1](cpu_pressure_validation/1_ranks_LocalFFTPreconditioner_72x36x200_1x1/configuration.md) | 1 | 72 × 36 × 200 | 1 × 1 × 1 | 1.500630 / 1.500630 | — | Current suite: rank completeness, finite fields, placement and timings checked |
| [2_ranks_model_72x36x8_5x10](cpu_pressure_validation/2_ranks_model_72x36x8_5x10/configuration.md) | 2 | 72 × 36 × 8 | 2 × 1 × 1 | 0.042401 / 0.092381 | — | Current suite: rank completeness, finite fields, placement and timings checked |
| [16_ranks_ColumnwiseTridiagonalPreconditioner_72x36x200_1x1](cpu_pressure_validation/16_ranks_ColumnwiseTridiagonalPreconditioner_72x36x200_1x1/configuration.md) | 16 | 72 × 36 × 200 | 4 × 4 × 1 | 0.754874 / 0.754874 | — | Current suite: rank completeness, finite fields, placement and timings checked |
| [16_ranks_LocalFFTPreconditioner_72x36x200_1x1](cpu_pressure_validation/16_ranks_LocalFFTPreconditioner_72x36x200_1x1/configuration.md) | 16 | 72 × 36 × 200 | 4 × 4 × 1 | 0.250728 / 0.250728 | — | Current suite: rank completeness, finite fields, placement and timings checked |
| [16_ranks_VerticalLinePreconditioner_72x36x200_1x1](cpu_pressure_validation/16_ranks_VerticalLinePreconditioner_72x36x200_1x1/configuration.md) | 16 | 72 × 36 × 200 | 4 × 4 × 1 | 1.749642 / 1.749642 | — | Current suite: rank completeness, finite fields, placement and timings checked |
| [16_ranks_model_72x36x200_2x2](cpu_pressure_validation/16_ranks_model_72x36x200_2x2/configuration.md) | 16 | 72 × 36 × 200 | 4 × 4 × 1 | 3.354035 / 4.578106 | — | Current suite: rank completeness, finite fields, placement and timings checked |
| [16_ranks_model_72x36x200_5x10](cpu_pressure_validation/16_ranks_model_72x36x200_5x10/configuration.md) | 16 | 72 × 36 × 200 | 4 × 4 × 1 | 7.633759 / 10.754958 | — | Current suite: rank completeness, finite fields, placement and timings checked |
| [192_ranks_LocalFFTPreconditioner_1440x720x200_1x1](cpu_pressure_validation/192_ranks_LocalFFTPreconditioner_1440x720x200_1x1/configuration.md) | 192 | 1440 × 720 × 200 | 16 × 12 × 1 | 121.662908 / 121.662908 | — | Current suite: rank completeness, finite fields, placement and timings checked |

## cpu_resolution

![cpu_resolution](cpu_resolution/cpu_resolution.svg)

| Case | Ranks | Global resolution | Partition | Fastest / median s per step | Median MPI efficiency | Validation |
|---|---:|---|---|---:|---:|---|
| [default](cpu_resolution/default/configuration.md) | 1 | 360 × 180 × 50 | 1 × 1 × 1 | 225.153769 / 276.558927 | — | Current suite: rank completeness, finite fields, placement and timings checked |
