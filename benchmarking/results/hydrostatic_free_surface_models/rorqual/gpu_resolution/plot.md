# rorqual: gpu_resolution

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](gpu_resolution.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [default](default/configuration.md) | 1 | 0.017257 | 0.017261 | Current suite: rank completeness, finite fields, placement and timings checked |
| [fine](fine/configuration.md) | 1 | 0.119260 | 0.119324 | Current suite: rank completeness, finite fields, placement and timings checked |
| [super_fine](super_fine/configuration.md) | 1 | 0.966834 | 0.967193 | Current suite: rank completeness, finite fields, placement and timings checked |
