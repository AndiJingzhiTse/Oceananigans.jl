# gpu_weak_scaling_super_fine

No completed, validated measurements.

<!-- current-rerun -->
## Current rerun

Study: `/local_scratch/ajtse/benchmark_studies/hydrostatic_free_surface_models/2026-10-13T193658Z/rondeau`. Original commands, allocation scripts and failure logs remain there.
Two untimed steps, then five synchronized windows of ten steps; one Julia thread per MPI rank.
This rerun validates all rank results, MPI communication, distinct resources and finite model fields.

| Case | Global resolution | MPI partition | Outcome | Details |
|---|---|---|---|---|
| 1_ranks | 1440 × 720 × 200 | 1 × 1 × 1 | FAILED | GPU VRAM exhausted; see original job.out and profiler logs in scratch study |
| 4_ranks | 2880 × 1440 × 200 | 2 × 2 × 1 | FAILED | GPU VRAM exhausted; see original job.out and profiler logs in scratch study |
| 16_ranks | 5760 × 2880 × 200 | 4 × 4 × 1 | RESOURCE_LIMIT | Requires 16; configured capacity is 4 |
