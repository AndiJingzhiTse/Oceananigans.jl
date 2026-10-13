# rondeau: gpu_scaling_super_fine

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](gpu_scaling_super_fine.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [2_ranks](2_ranks/configuration.md) | 2 | 0.991023 | 0.992988 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [4_ranks](4_ranks/configuration.md) | 4 | 0.517122 | 0.521209 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
