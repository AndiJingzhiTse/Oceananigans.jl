# Benchmark configuration

Model: HydrostaticFreeSurfaceModel; device: CPU.
Grid: 1440 × 720 × 200; LatitudeLongitudeGrid; Float64.
MPI partition: 8 × 6 × 1; 48 ranks; 1 threads/rank.
Local resolution per rank: x 180–180 × y 120–120 × z 200. Exact per-rank sizes are in results.json.
Timing: 2 untimed steps, 5 windows of 10 steps; Δt=60 simulated seconds.
Validation: Current suite: rank completeness, finite fields, placement and timings checked.
Original run: `hydrostatic_free_surface_models/rorqual/2026-10-07_cpu_retry`; measured at 2026-10-07T15:31:35.834.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
