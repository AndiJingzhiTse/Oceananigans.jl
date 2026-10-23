# Nonhydrostatic Dagger preflight checks

Development validation on a 72 × 36 × 8 LatitudeLongitudeGrid, partition 2 × 1 × 1, two MPI ranks. Each variant completed two warmup steps and five windows of ten steps. These small checks are not production performance measurements; no speedups are inferred from them.

| Device | Execution | MPI / finite fields | Checked pressure solves per rank | Maximum final true residual | Tolerance |
|---|---|---|---:|---:|---:|
| CPU | baseline | PASS | 157 | 1.42814656822e-08 | 1.49011611938e-08 |
| CPU | dagger | PASS | 157 | 1.42814656822e-08 | 1.49011611938e-08 |
| GPU | baseline | PASS | 157 | 1.39337485396e-08 | 1.49011611938e-08 |
| GPU | dagger | PASS | 157 | 1.39337485396e-08 | 1.49011611938e-08 |

Dagger version: 0.22.7. Julia: 1.12.7. GPU checks use `JULIA_CUDA_MEMORY_POOL=none`, matching the production launcher. The initial default-pool attempt emitted CUDA IPC warnings and was stopped; its log is retained in scratch.

A scoped-wrapper smoke check also verified mutation of the original object on the single computation thread.

Raw checks and logs: `/local_scratch/ajtse/benchmark_studies/non_hydrostatic_models/2026-10-19-dagger/rondeau/pilot`.
