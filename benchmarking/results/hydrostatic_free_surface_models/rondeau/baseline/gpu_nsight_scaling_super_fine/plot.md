# baseline: gpu_nsight_scaling_super_fine

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](gpu_nsight_scaling_super_fine.svg)

![Kernel duration shares](gpu_nsight_scaling_super_fine_kernels.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [2_ranks](2_ranks/configuration.md) | 2 | 1.002786 | 1.014295 | Current suite checks |
