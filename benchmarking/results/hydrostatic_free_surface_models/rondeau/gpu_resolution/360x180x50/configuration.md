# Benchmark configuration

Model: HydrostaticFreeSurfaceModel; device: GPU.
Grid: 360 × 180 × 50; LatitudeLongitudeGrid; Float64.
MPI partition: 1 × 1 × 1; 1 ranks; 1 threads/rank.
Local resolution per rank: x 360–360 × y 180–180 × z 50. Exact per-rank sizes are in results.json.
Warmup steps were not recorded; timing: 5 windows of 10 steps; Δt=60.0 simulated seconds.
Validation: Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable.
Original run: `hydrostatic_free_surface_models/rondeau/2026-09-27_all`; measured at 2026-09-27T04:52:55.784.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
