# baseline: gpu_resolution

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](gpu_resolution.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [default](default/configuration.md) | 1 | 0.332311 | 0.384814 | Current suite checks |
| [fine](fine/configuration.md) | 1 | 3.582070 | 4.351423 | Current suite checks |
