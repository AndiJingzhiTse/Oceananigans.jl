# Benchmark configuration

Model: HydrostaticFreeSurfaceModel; device: GPU.
Grid: 1440 × 720 × 200; LatitudeLongitudeGrid; Float64.
MPI partition: 32 × 1 × 1; 32 ranks; 1 threads/rank.
Local resolution per rank: x 45–45 × y 720–720 × z 200. Exact per-rank sizes are in results.json.
Timing: 2 untimed steps, 5 windows of 100 steps; Δt=60 simulated seconds.
Validation: Current suite: rank completeness, finite fields, placement and timings checked.
Original run: `hydrostatic_free_surface_models/nibi/2026-10-07_gpu_scaling_extended`; measured at 2026-10-12T13:29:38.182.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
