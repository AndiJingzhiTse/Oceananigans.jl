# Benchmark configuration

Model: HydrostaticFreeSurfaceModel; device: CPU.
Grid: 72 × 36 × 8; LatitudeLongitudeGrid; Float64.
MPI partition: 2 × 1 × 1; 2 ranks; 1 threads/rank.
Local resolution per rank: x 36–36 × y 36–36 × z 8. Exact per-rank sizes are in results.json.
Timing: 2 untimed steps, 5 windows of 10 steps; Δt=60 simulated seconds.
Validation: Current suite: rank completeness, finite fields, placement and timings checked.
Original run: `hydrostatic_free_surface_models/suite_validation/2026-10-07_cpu_mpi`; measured at 2026-10-07T05:33:00.295.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
