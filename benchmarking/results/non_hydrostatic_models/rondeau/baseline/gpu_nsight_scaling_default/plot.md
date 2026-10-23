# baseline: gpu_nsight_scaling_default

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](gpu_nsight_scaling_default.svg)

![Kernel duration shares](gpu_nsight_scaling_default_kernels.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [1_ranks](1_ranks/configuration.md) | 1 | 0.808531 | 1.127963 | Current suite checks |
