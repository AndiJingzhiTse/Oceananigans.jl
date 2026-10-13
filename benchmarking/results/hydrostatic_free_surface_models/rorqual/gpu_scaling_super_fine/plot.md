# rorqual: gpu_scaling_super_fine

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](gpu_scaling_super_fine.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [16_ranks](16_ranks/configuration.md) | 16 | 0.098755 | 0.107124 | Current suite: rank completeness, finite fields, placement and timings checked |
| [1_ranks](1_ranks/configuration.md) | 1 | 0.964997 | 0.965221 | Current suite: rank completeness, finite fields, placement and timings checked |
| [2_ranks](2_ranks/configuration.md) | 2 | 0.493953 | 0.498924 | Current suite: rank completeness, finite fields, placement and timings checked |
| [32_ranks](32_ranks/configuration.md) | 32 | 0.080087 | 0.130831 | Current suite: rank completeness, finite fields, placement and timings checked |
| [4_ranks](4_ranks/configuration.md) | 4 | 0.253451 | 0.255255 | Current suite: rank completeness, finite fields, placement and timings checked |
| [64_ranks](64_ranks/configuration.md) | 64 | 0.074548 | 0.088781 | Current suite: rank completeness, finite fields, placement and timings checked |
| [8_ranks](8_ranks/configuration.md) | 8 | 0.146426 | 0.150829 | Current suite: rank completeness, finite fields, placement and timings checked |
