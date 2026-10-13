# rondeau: gpu_resolution

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](gpu_resolution.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [1440x720x50](1440x720x50/configuration.md) | 1 | 0.503266 | 0.503473 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [180x90x50](180x90x50/configuration.md) | 1 | 0.011853 | 0.011891 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [360x180x50](360x180x50/configuration.md) | 1 | 0.033800 | 0.033816 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [720x360x50](720x360x50/configuration.md) | 1 | 0.125816 | 0.125869 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
