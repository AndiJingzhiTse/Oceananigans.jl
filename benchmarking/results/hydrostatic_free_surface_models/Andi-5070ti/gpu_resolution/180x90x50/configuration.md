# Benchmark configuration

Model: HydrostaticFreeSurfaceModel; device: GPU.
Grid: 180 × 90 × 50; LatitudeLongitudeGrid; Float64.
MPI partition: 1 × 1 × 1; 1 ranks; 1 threads/rank.
Local resolution per rank: x 180–180 × y 90–90 × z 50. Exact per-rank sizes are in results.json.
Warmup steps were not recorded; timing: 5 windows of 10 steps; Δt=60.0 simulated seconds.
Validation: Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable.
Original run: `hydrostatic_free_surface_models/Andi-5070ti/2026-09-17_gpu`; measured at 2026-09-17T14:52:19.553.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
