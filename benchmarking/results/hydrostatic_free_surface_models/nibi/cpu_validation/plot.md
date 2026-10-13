# nibi: cpu_validation

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](cpu_validation.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [2_ranks_72x36x8](2_ranks_72x36x8/configuration.md) | 2 | 0.056037 | 0.057248 | Current suite: rank completeness, finite fields, placement and timings checked |
