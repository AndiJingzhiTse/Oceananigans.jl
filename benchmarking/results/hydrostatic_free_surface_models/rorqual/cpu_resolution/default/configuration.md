# Benchmark configuration

Model: HydrostaticFreeSurfaceModel; device: CPU.
Grid: 360 × 180 × 50; LatitudeLongitudeGrid; Float64.
MPI partition: 1 × 1 × 1; 1 ranks; 1 threads/rank.
Local resolution per rank: x 360–360 × y 180–180 × z 50. Exact per-rank sizes are in results.json.
Timing: 2 untimed steps, 5 windows of 10 steps; Δt=60 simulated seconds.
Validation: Current suite: rank completeness, finite fields, placement and timings checked.
Original run: `hydrostatic_free_surface_models/rorqual/2026-10-07_cpu_retry`; measured at 2026-10-07T15:32:25.955.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
