# Unified suite CPU MPI smoke validation

Slurm job **23372331** completed with exit **0** on Nibi. This is a small
validation case, not a production super_fine performance result.

- Actual grid: **72 × 36 × 8 LatitudeLongitudeGrid**, no bathymetry.
- MPI partition: **2 × 1 × 1**; local grid **36 × 36 × 8**.
- Two MPI ranks, one Julia computation thread and one pinned physical core/rank.
- Shared production model and timing path: Float64, WENOVectorInvariantDefault,
  WENO7, CATKE, T/S, SplitRungeKutta3, Δt=60 s, requested free-surface substeps=30,
  extend_halos=false; two untimed steps, five ten-step windows.
- MPI ring, distinct physical cores, finite model fields, all rank results,
  individual timing windows and aggregate recomputation passed.
- Current controller refresh/validation accepted the captured worker output.

The exact worker used by the job is saved here. SHA-256: `66c16e10a3c10fe5fb4b8d42233471433a28939c0180c964c712e1e339ca48bd`.
The execution logs, configuration, runtime metadata and raw timings are retained.
The original scratch run and report are at
`/scratch/anditse/benchmark_suite_smoke_2026-10-07/`.

Additional checks: 16 unified planner/report/snapshot tests and 17 historical
Nibi regression tests passed; Julia syntax/API checks, shell syntax checks and
historical Rondeau dry runs passed. GPU profiling execution needs a GPU allocation;
its launch settings, artifact validation and reporting are covered by tests.
