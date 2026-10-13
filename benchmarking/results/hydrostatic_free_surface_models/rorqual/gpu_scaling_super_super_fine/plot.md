# rorqual: gpu_scaling_super_super_fine

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](gpu_scaling_super_super_fine.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [16_ranks](16_ranks/configuration.md) | 16 | 0.269842 | 0.271461 | Current suite: rank completeness, finite fields, placement and timings checked |
| [32_ranks](32_ranks/configuration.md) | 32 | 0.161687 | 0.170486 | Current suite: rank completeness, finite fields, placement and timings checked |
| [4_ranks](4_ranks/configuration.md) | 4 | 0.989070 | 0.995564 | Current suite: rank completeness, finite fields, placement and timings checked |
| [64_ranks](64_ranks/configuration.md) | 64 | 0.109598 | 0.111415 | Current suite: rank completeness, finite fields, placement and timings checked |
| [8_ranks](8_ranks/configuration.md) | 8 | 0.514316 | 0.517392 | Current suite: rank completeness, finite fields, placement and timings checked |
