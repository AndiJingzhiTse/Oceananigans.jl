# Benchmark configuration

Model: HydrostaticFreeSurfaceModel; device: GPU.
Grid: 1440 × 720 × 200; LatitudeLongitudeGrid; Float64.
MPI partition: 2 × 2 × 1; 4 ranks; 1 threads/rank.
Local resolution per rank: x 720–720 × y 360–360 × z 200. Exact per-rank sizes are in results.json.
Timing: 2 untimed steps, 5 windows of 10 steps; Δt=60 simulated seconds.
Validation: Current suite: rank completeness, finite fields, placement and timings checked; original remote trace checksums retained.
Original run: `hydrostatic_free_surface_models/rorqual/2026-10-07_full_suite`; measured at 2026-10-07T07:17:57.860.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
