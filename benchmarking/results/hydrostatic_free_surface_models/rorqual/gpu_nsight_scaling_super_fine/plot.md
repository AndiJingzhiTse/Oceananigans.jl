# rorqual: gpu_nsight_scaling_super_fine

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](gpu_nsight_scaling_super_fine.svg)

![Kernel duration shares](gpu_nsight_scaling_super_fine_kernels.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [16_ranks](16_ranks/configuration.md) | 16 | 0.106867 | 0.117125 | Current suite: rank completeness, finite fields, placement and timings checked; original remote trace checksums retained |
| [1_ranks](1_ranks/configuration.md) | 1 | 0.973019 | 0.973334 | Current suite: rank completeness, finite fields, placement and timings checked; original remote trace checksums retained |
| [2_ranks](2_ranks/configuration.md) | 2 | 0.498359 | 0.501470 | Current suite: rank completeness, finite fields, placement and timings checked; original remote trace checksums retained |
| [32_ranks](32_ranks/configuration.md) | 32 | 0.090823 | 0.116467 | Current suite: rank completeness, finite fields, placement and timings checked; original remote trace checksums retained |
| [4_ranks](4_ranks/configuration.md) | 4 | 0.294648 | 0.295675 | Current suite: rank completeness, finite fields, placement and timings checked; original remote trace checksums retained |
| [64_ranks](64_ranks/configuration.md) | 64 | 0.084528 | 0.150939 | Current suite: rank completeness, finite fields, placement and timings checked; original remote trace checksums retained |
| [8_ranks](8_ranks/configuration.md) | 8 | 0.155678 | 0.157967 | Current suite: rank completeness, finite fields, placement and timings checked; original remote trace checksums retained |
