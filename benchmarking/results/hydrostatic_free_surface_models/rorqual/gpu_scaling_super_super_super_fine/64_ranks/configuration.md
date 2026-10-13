# Benchmark configuration

Model: HydrostaticFreeSurfaceModel; device: GPU.
Grid: 5760 × 2880 × 200; LatitudeLongitudeGrid; Float64.
MPI partition: 8 × 8 × 1; 64 ranks; 1 threads/rank.
Local resolution per rank: x 720–720 × y 360–360 × z 200. Exact per-rank sizes are in results.json.
Timing: 2 untimed steps, 5 windows of 10 steps; Δt=15.0 simulated seconds.
Validation: Current suite: rank completeness, finite fields, placement and timings checked.
Original run: `hydrostatic_free_surface_models/rorqual/2026-10-07_gpu_extended_suite`; measured at 2026-10-08T09:38:30.687.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
