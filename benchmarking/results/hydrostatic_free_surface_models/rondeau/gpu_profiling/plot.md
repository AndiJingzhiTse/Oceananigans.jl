# rondeau: gpu_profiling

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](gpu_profiling.svg)

![Kernel duration shares](gpu_profiling_kernels.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [360x180x50](360x180x50/configuration.md) | 1 | 0.039191 | 0.039191 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [720x360x50](720x360x50/configuration.md) | 1 | 0.134866 | 0.134866 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
