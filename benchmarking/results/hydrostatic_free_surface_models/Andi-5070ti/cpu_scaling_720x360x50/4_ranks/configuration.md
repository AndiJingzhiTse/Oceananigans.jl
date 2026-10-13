# Benchmark configuration

Model: HydrostaticFreeSurfaceModel; device: CPU.
Grid: 720 × 360 × 50; TripolarGrid; Float64.
MPI partition: 2 × 2 × 1; 4 ranks; 1 threads/rank.
Local resolution per rank: x 360–360 × y 180–180 × z 50. Exact per-rank sizes are in results.json.
Warmup steps were not recorded; timing: 5 windows of 10 steps; Δt=60.0 simulated seconds.
Validation: Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable.
Original run: `hydrostatic_free_surface_models/Andi-5070ti/2026-09-18_cpu_distributed`; measured at 2026-09-18T23:04:31.526.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
