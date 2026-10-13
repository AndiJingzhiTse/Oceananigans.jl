# Benchmark configuration

Model: HydrostaticFreeSurfaceModel; device: CPU.
Grid: 360 × 180 × 50; TripolarGrid; Float64.
MPI partition: 8 × 4 × 1; 32 ranks; 1 threads/rank.
Local resolution per rank: x 45–45 × y 45–45 × z 50. Exact per-rank sizes are in results.json.
Warmup steps were not recorded; timing: 5 windows of 10 steps; Δt=60.0 simulated seconds.
Validation: Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable.
Original run: `hydrostatic_free_surface_models/rondeau/2026-09-27_all`; measured at 2026-09-30T03:53:23.434.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
