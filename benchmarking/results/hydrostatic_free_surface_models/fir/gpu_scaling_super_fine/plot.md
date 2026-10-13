# fir: gpu_scaling_super_fine

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](gpu_scaling_super_fine.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [1_ranks](1_ranks/configuration.md) | 1 | 0.964918 | 0.965420 | Current suite: rank completeness, finite fields, placement and timings checked |
| [2_ranks](2_ranks/configuration.md) | 2 | 0.495245 | 0.496732 | Current suite: rank completeness, finite fields, placement and timings checked |
| [4_ranks](4_ranks/configuration.md) | 4 | 0.254298 | 0.254961 | Current suite: rank completeness, finite fields, placement and timings checked |
