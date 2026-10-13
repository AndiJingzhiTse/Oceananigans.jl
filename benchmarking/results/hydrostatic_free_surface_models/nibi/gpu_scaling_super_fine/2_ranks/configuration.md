# Benchmark configuration

Model: HydrostaticFreeSurfaceModel; device: GPU.
Grid: 1440 × 720 × 200; LatitudeLongitudeGrid; Float64.
MPI partition: 1 × 2 × 1; 2 ranks; 1 threads/rank.
Local resolution per rank: x 1440–1440 × y 360–360 × z 200. Exact per-rank sizes are in results.json.
Warmup steps were not recorded; timing: 5 windows of 10 steps; Δt=60.0 simulated seconds.
Validation: Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable.
Original run: `hydrostatic_free_surface_models/nibi/2026-10-05_gpu_scaling`; measured at 2026-10-05T04:47:21.478.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
