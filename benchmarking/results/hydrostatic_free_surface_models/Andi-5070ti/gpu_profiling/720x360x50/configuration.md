# Benchmark configuration

Model: HydrostaticFreeSurfaceModel; device: GPU.
Grid: 720 × 360 × 50; TripolarGrid; Float64.
MPI partition: 1 × 1 × 1; 1 ranks; 1 threads/rank.
Local resolution per rank: x 720–720 × y 360–360 × z 50. Exact per-rank sizes are in results.json.
Warmup steps were not recorded; timing: 1 windows of 2 steps; Δt=60.0 simulated seconds.
Validation: Historical: complete ranks and timing aggregates checked; finite-state/placement checks unavailable.
Original run: `hydrostatic_free_surface_models/Andi-5070ti/2026-09-22_nsys_gpu_720x360x50`; measured at 2026-09-22T14:34:45.889.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
