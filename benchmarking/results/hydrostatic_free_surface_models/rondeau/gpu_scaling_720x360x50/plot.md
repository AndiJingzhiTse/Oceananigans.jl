# rondeau: gpu_scaling_720x360x50

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](gpu_scaling_720x360x50.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [1_ranks](1_ranks/configuration.md) | 1 | 0.133612 | 0.133664 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [2_ranks](2_ranks/configuration.md) | 2 | 0.083338 | 0.084888 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [4_ranks](4_ranks/configuration.md) | 4 | 0.060002 | 0.060339 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
