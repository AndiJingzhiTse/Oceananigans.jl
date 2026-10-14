# rondeau: cpu_mpi_scaling_super_fine

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](cpu_mpi_scaling_super_fine.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [96_ranks](96_ranks/configuration.md) | 96 | 13.242835 | 13.322377 | Current suite checks |
| [48_ranks](48_ranks/configuration.md) | 48 | 22.291999 | 22.308046 | Current suite checks |
| [24_ranks](24_ranks/configuration.md) | 24 | 41.004804 | 41.094211 | Current suite checks |
| [12_ranks](12_ranks/configuration.md) | 12 | 77.926198 | 78.058682 | Current suite checks |
| [6_ranks](6_ranks/configuration.md) | 6 | 148.776940 | 148.953459 | Current suite checks |

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
| 24_ranks | 1440 × 720 × 200 | 6 × 4 × 1 | COMPLETED | Rank results, finite fields and resource placement verified |
| 12_ranks | 1440 × 720 × 200 | 4 × 3 × 1 | COMPLETED | Rank results, finite fields and resource placement verified |
| 6_ranks | 1440 × 720 × 200 | 3 × 2 × 1 | COMPLETED | Rank results, finite fields and resource placement verified |
