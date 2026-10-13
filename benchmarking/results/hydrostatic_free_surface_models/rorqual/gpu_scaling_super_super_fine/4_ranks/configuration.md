# Benchmark configuration

Model: HydrostaticFreeSurfaceModel; device: GPU.
Grid: 2880 × 1440 × 200; LatitudeLongitudeGrid; Float64.
MPI partition: 2 × 2 × 1; 4 ranks; 1 threads/rank.
Local resolution per rank: x 1440–1440 × y 720–720 × z 200. Exact per-rank sizes are in results.json.
Timing: 2 untimed steps, 5 windows of 10 steps; Δt=30.0 simulated seconds.
Validation: Current suite: rank completeness, finite fields, placement and timings checked.
Original run: `hydrostatic_free_surface_models/rorqual/2026-10-07_gpu_extended_suite`; measured at 2026-10-08T13:49:43.956.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
