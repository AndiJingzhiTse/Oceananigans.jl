# rondeau: cpu_mpi_scaling_super_fine

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](cpu_mpi_scaling_super_fine.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [96_ranks](96_ranks/configuration.md) | 96 | 13.242835 | 13.322377 | Current suite checks |
| [48_ranks](48_ranks/configuration.md) | 48 | 22.291999 | 22.308046 | Current suite checks |

<!-- current-rerun -->
## Current rerun

Study: `/local_scratch/ajtse/benchmark_studies/hydrostatic_free_surface_models/2026-10-13T193658Z/rondeau`. Original commands, allocation scripts and failure logs remain there.
Two untimed steps, then five synchronized windows of ten steps; one Julia thread per MPI rank.
This rerun validates all rank results, MPI communication, distinct resources and finite model fields.

Highest completed case: **96_ranks**.

| Case | Global resolution | MPI partition | Outcome | Details |
|---|---|---|---|---|
| 192_ranks | 1440 × 720 × 200 | 16 × 12 × 1 | RESOURCE_LIMIT | Requires 192; configured capacity is 128 |
| 96_ranks | 1440 × 720 × 200 | 12 × 8 × 1 | COMPLETED | Rank results, finite fields and resource placement verified |
| 48_ranks | 1440 × 720 × 200 | 8 × 6 × 1 | COMPLETED | Rank results, finite fields and resource placement verified |
