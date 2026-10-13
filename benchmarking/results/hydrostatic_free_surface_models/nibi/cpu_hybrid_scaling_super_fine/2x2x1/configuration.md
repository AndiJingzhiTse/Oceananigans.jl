# Benchmark configuration

Model: HydrostaticFreeSurfaceModel; device: CPU.
Grid: 1440 × 720 × 200; LatitudeLongitudeGrid; Float64.
MPI partition: 2 × 2 × 1; 4 ranks; 192 threads/rank.
Local resolution per rank: x 720–720 × y 360–360 × z 200. Exact per-rank sizes are in results.json.
Warmup steps were not recorded; timing: 5 windows of 10 steps; Δt=60.0 simulated seconds.
Validation: Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable.
Original run: `hydrostatic_free_surface_models/nibi/2026-10-06_cpu_scaling_super_fine`; measured at 2026-10-06T10:17:31.956.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
