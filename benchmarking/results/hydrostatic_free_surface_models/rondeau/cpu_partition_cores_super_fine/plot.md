# cpu_partition_cores_super_fine

No completed, validated measurements.

<!-- current-rerun -->
## Current rerun

Study: `/local_scratch/ajtse/benchmark_studies/hydrostatic_free_surface_models/2026-10-13T193658Z/rondeau`. Original commands, allocation scripts and failure logs remain there.
Two untimed steps, then five synchronized windows of ten steps; one Julia thread per MPI rank.
This rerun validates all rank results, MPI communication, distinct resources and finite model fields.

| Case | Global resolution | MPI partition | Outcome | Details |
|---|---|---|---|---|
| 192x1x1 | 1440 × 720 × 200 | 192 × 1 × 1 | RESOURCE_LIMIT | Requires 192; configured capacity is 128 |
| 96x2x1 | 1440 × 720 × 200 | 96 × 2 × 1 | RESOURCE_LIMIT | Requires 192; configured capacity is 128 |
| 64x3x1 | 1440 × 720 × 200 | 64 × 3 × 1 | RESOURCE_LIMIT | Requires 192; configured capacity is 128 |
| 48x4x1 | 1440 × 720 × 200 | 48 × 4 × 1 | RESOURCE_LIMIT | Requires 192; configured capacity is 128 |
| 32x6x1 | 1440 × 720 × 200 | 32 × 6 × 1 | RESOURCE_LIMIT | Requires 192; configured capacity is 128 |
| 24x8x1 | 1440 × 720 × 200 | 24 × 8 × 1 | RESOURCE_LIMIT | Requires 192; configured capacity is 128 |
| 16x12x1 | 1440 × 720 × 200 | 16 × 12 × 1 | RESOURCE_LIMIT | Requires 192; configured capacity is 128 |
| 12x16x1 | 1440 × 720 × 200 | 12 × 16 × 1 | RESOURCE_LIMIT | Requires 192; configured capacity is 128 |
| 8x24x1 | 1440 × 720 × 200 | 8 × 24 × 1 | RESOURCE_LIMIT | Requires 192; configured capacity is 128 |
| 6x32x1 | 1440 × 720 × 200 | 6 × 32 × 1 | RESOURCE_LIMIT | Requires 192; configured capacity is 128 |
| 4x48x1 | 1440 × 720 × 200 | 4 × 48 × 1 | RESOURCE_LIMIT | Requires 192; configured capacity is 128 |
| 3x64x1 | 1440 × 720 × 200 | 3 × 64 × 1 | RESOURCE_LIMIT | Requires 192; configured capacity is 128 |
| 2x96x1 | 1440 × 720 × 200 | 2 × 96 × 1 | RESOURCE_LIMIT | Requires 192; configured capacity is 128 |
| 1x192x1 |  | 1 × 192 × 1 | GEOMETRY_LIMIT | Partition [1, 192, 1] has fewer than 7 local cells per horizontal direction |
