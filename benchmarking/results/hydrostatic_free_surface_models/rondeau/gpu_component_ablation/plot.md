# rondeau: gpu_component_ablation

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](gpu_component_ablation.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [baseline](baseline/configuration.md) | 1 | 0.036953 | 0.036988 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [no_buoyancy](no_buoyancy/configuration.md) | 1 | 0.020543 | 0.020568 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [no_closure](no_closure/configuration.md) | 1 | 0.014414 | 0.014475 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [no_coriolis](no_coriolis/configuration.md) | 1 | 0.036615 | 0.036649 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [no_tracer_advection](no_tracer_advection/configuration.md) | 1 | 0.033992 | 0.034004 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [no_tracers](no_tracers/configuration.md) | 1 | 0.016565 | 0.016587 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
