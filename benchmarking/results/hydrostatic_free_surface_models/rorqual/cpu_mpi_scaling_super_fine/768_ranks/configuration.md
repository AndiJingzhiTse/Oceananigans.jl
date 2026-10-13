# Benchmark configuration

Model: HydrostaticFreeSurfaceModel; device: CPU.
Grid: 1440 × 720 × 200; LatitudeLongitudeGrid; Float64.
MPI partition: 32 × 24 × 1; 768 ranks; 1 threads/rank.
Local resolution per rank: x 45–45 × y 30–30 × z 200. Exact per-rank sizes are in results.json.
Timing: 2 untimed steps, 5 windows of 10 steps; Δt=60 simulated seconds.
Validation: Current suite: rank completeness, finite fields, placement and timings checked.
Original run: `hydrostatic_free_surface_models/rorqual/2026-10-07_cpu_retry`; measured at 2026-10-07T15:21:49.439.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
