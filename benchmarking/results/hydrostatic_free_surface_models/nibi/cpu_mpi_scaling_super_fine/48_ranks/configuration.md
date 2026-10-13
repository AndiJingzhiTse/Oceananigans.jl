# Benchmark configuration

Model: HydrostaticFreeSurfaceModel; device: CPU.
Grid: 1440 × 720 × 200; LatitudeLongitudeGrid; Float64.
MPI partition: 8 × 6 × 1; 48 ranks; 1 threads/rank.
Local resolution per rank: x 180–180 × y 120–120 × z 200. Exact per-rank sizes are in results.json.
Timing: 2 untimed steps, 5 windows of 10 steps; Δt=60 simulated seconds.
Validation: Historical: complete ranks, finite fields and timing aggregates checked; original placement record retained.
Original run: `hydrostatic_free_surface_models/nibi/2026-10-06_cpu_scaling_cores_super_fine`; measured at 2026-10-06T17:41:50.932.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
