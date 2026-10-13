# nibi: cpu_partition_hybrid_super_fine

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](cpu_partition_hybrid_super_fine.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [1x4x1](1x4x1/configuration.md) | 4 | 50.645297 | 52.108303 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [2x2x1](2x2x1/configuration.md) | 4 | 55.448350 | 56.550017 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [4x1x1](4x1x1/configuration.md) | 4 | 51.668704 | 52.765599 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
