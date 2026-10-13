# rorqual: cpu_resolution

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](cpu_resolution.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [default](default/configuration.md) | 1 | 9.133294 | 9.150603 | Current suite: rank completeness, finite fields, placement and timings checked |
| [fine](fine/configuration.md) | 1 | 71.099241 | 71.252001 | Current suite: rank completeness, finite fields, placement and timings checked |
| [super_fine](super_fine/configuration.md) | 1 | 574.466632 | 575.534054 | Current suite: rank completeness, finite fields, placement and timings checked |
