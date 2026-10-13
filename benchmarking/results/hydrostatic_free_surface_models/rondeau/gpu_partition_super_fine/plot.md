# rondeau: gpu_partition_super_fine

Latest accepted measurement for each case. Configuration links record the actual grid, partition, numerical methods, timing protocol and validation limits.

![Timing and scaling](gpu_partition_super_fine.svg)

| Case | MPI ranks | Fastest s/step | Median s/step | Validation |
|---|---:|---:|---:|---|
| [2x1x1](2x1x1/configuration.md) | 2 | 0.951312 | 0.953770 | Current suite checks |
| [1x2x1](1x2x1/configuration.md) | 2 | 0.991286 | 0.992599 | Current suite checks |
| [4x1x1](4x1x1/configuration.md) | 4 | 0.487795 | 0.534275 | Current suite checks |

<!-- current-rerun -->
## Current rerun

Study: `/local_scratch/ajtse/benchmark_studies/hydrostatic_free_surface_models/2026-10-13T193658Z/rondeau`. Original commands, allocation scripts and failure logs remain there.
Two untimed steps, then five synchronized windows of ten steps; one Julia thread per MPI rank.
This rerun validates all rank results, MPI communication, distinct resources and finite model fields.

Highest completed case: **4x1x1**.

| Case | Global resolution | MPI partition | Outcome | Details |
|---|---|---|---|---|
| 1x1x1 | 1440 × 720 × 200 | 1 × 1 × 1 | FAILED | GPU VRAM exhausted; see original job.out and profiler logs in scratch study |
| 2x1x1 | 1440 × 720 × 200 | 2 × 1 × 1 | COMPLETED | Rank results, finite fields and resource placement verified |
| 1x2x1 | 1440 × 720 × 200 | 1 × 2 × 1 | COMPLETED | Rank results, finite fields and resource placement verified |
| 4x1x1 | 1440 × 720 × 200 | 4 × 1 × 1 | COMPLETED | Rank results, finite fields and resource placement verified |
| 8x1x1 | 1440 × 720 × 200 | 8 × 1 × 1 | RESOURCE_LIMIT | Requires 8; configured capacity is 4 |
| 4x2x1 | 1440 × 720 × 200 | 4 × 2 × 1 | RESOURCE_LIMIT | Requires 8; configured capacity is 4 |
| 2x4x1 | 1440 × 720 × 200 | 2 × 4 × 1 | RESOURCE_LIMIT | Requires 8; configured capacity is 4 |
| 1x8x1 | 1440 × 720 × 200 | 1 × 8 × 1 | RESOURCE_LIMIT | Requires 8; configured capacity is 4 |
| 16x1x1 | 1440 × 720 × 200 | 16 × 1 × 1 | RESOURCE_LIMIT | Requires 16; configured capacity is 4 |
| 8x2x1 | 1440 × 720 × 200 | 8 × 2 × 1 | RESOURCE_LIMIT | Requires 16; configured capacity is 4 |
| 4x4x1 | 1440 × 720 × 200 | 4 × 4 × 1 | RESOURCE_LIMIT | Requires 16; configured capacity is 4 |
| 2x8x1 | 1440 × 720 × 200 | 2 × 8 × 1 | RESOURCE_LIMIT | Requires 16; configured capacity is 4 |
| 1x16x1 | 1440 × 720 × 200 | 1 × 16 × 1 | RESOURCE_LIMIT | Requires 16; configured capacity is 4 |
| 32x1x1 | 1440 × 720 × 200 | 32 × 1 × 1 | RESOURCE_LIMIT | Requires 32; configured capacity is 4 |
| 16x2x1 | 1440 × 720 × 200 | 16 × 2 × 1 | RESOURCE_LIMIT | Requires 32; configured capacity is 4 |
| 8x4x1 | 1440 × 720 × 200 | 8 × 4 × 1 | RESOURCE_LIMIT | Requires 32; configured capacity is 4 |
| 4x8x1 | 1440 × 720 × 200 | 4 × 8 × 1 | RESOURCE_LIMIT | Requires 32; configured capacity is 4 |
| 2x16x1 | 1440 × 720 × 200 | 2 × 16 × 1 | RESOURCE_LIMIT | Requires 32; configured capacity is 4 |
| 1x32x1 |  | 1 × 32 × 1 | GEOMETRY_LIMIT | Partition [1, 32, 1] has fewer than 23 local cells per horizontal direction |
| 64x1x1 |  | 64 × 1 × 1 | GEOMETRY_LIMIT | Partition [64, 1, 1] has fewer than 23 local cells per horizontal direction |
| 32x2x1 | 1440 × 720 × 200 | 32 × 2 × 1 | RESOURCE_LIMIT | Requires 64; configured capacity is 4 |
| 16x4x1 | 1440 × 720 × 200 | 16 × 4 × 1 | RESOURCE_LIMIT | Requires 64; configured capacity is 4 |
| 8x8x1 | 1440 × 720 × 200 | 8 × 8 × 1 | RESOURCE_LIMIT | Requires 64; configured capacity is 4 |
| 4x16x1 | 1440 × 720 × 200 | 4 × 16 × 1 | RESOURCE_LIMIT | Requires 64; configured capacity is 4 |
| 2x32x1 |  | 2 × 32 × 1 | GEOMETRY_LIMIT | Partition [2, 32, 1] has fewer than 23 local cells per horizontal direction |
| 1x64x1 |  | 1 × 64 × 1 | GEOMETRY_LIMIT | Partition [1, 64, 1] has fewer than 23 local cells per horizontal direction |
