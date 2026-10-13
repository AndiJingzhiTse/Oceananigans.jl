# rondeau: gpu_resolution

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](gpu_resolution.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [1440x720x50](1440x720x50/configuration.md) | 1 | 0.503266 | 0.503473 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [180x90x50](180x90x50/configuration.md) | 1 | 0.011853 | 0.011891 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [360x180x50](360x180x50/configuration.md) | 1 | 0.033800 | 0.033816 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [720x360x50](720x360x50/configuration.md) | 1 | 0.125816 | 0.125869 | Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable |
| [default](default/configuration.md) | 1 | 0.033990 | 0.034029 | Current suite checks |
| [fine](fine/configuration.md) | 1 | 0.248365 | 0.248458 | Current suite checks |

<!-- current-rerun -->
## Current rerun

Study: `/local_scratch/ajtse/benchmark_studies/hydrostatic_free_surface_models/2026-10-13T193658Z/rondeau`. Original commands, allocation scripts and failure logs remain there.
Two untimed steps, then five synchronized windows of ten steps; one Julia thread per MPI rank.
This rerun validates all rank results, MPI communication, distinct resources and finite model fields.

Highest completed case: **fine**.

| Case | Global resolution | MPI partition | Outcome | Details |
|---|---|---|---|---|
| default | 360 × 180 × 50 | 1 × 1 × 1 | COMPLETED | Rank results, finite fields and resource placement verified |
| fine | 720 × 360 × 100 | 1 × 1 × 1 | COMPLETED | Rank results, finite fields and resource placement verified |
| super_fine | 1440 × 720 × 200 | 1 × 1 × 1 | FAILED | GPU VRAM exhausted; see original job.out and profiler logs in scratch study |
