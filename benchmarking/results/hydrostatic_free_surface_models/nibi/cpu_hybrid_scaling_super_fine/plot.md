# nibi: cpu_hybrid_scaling_super_fine

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](cpu_hybrid_scaling_super_fine.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [1x1x1](1x1x1/configuration.md) | 1 | 42.336905 | 42.712967 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [1x2x1](1x2x1/configuration.md) | 2 | 39.997439 | 44.307615 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [2x2x1](2x2x1/configuration.md) | 4 | 57.774982 | 58.626502 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
