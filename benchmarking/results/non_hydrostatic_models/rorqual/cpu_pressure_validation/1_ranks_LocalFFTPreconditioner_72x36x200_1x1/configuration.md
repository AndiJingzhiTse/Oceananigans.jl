# Benchmark configuration

Model: NonhydrostaticModel; device: CPU.
Grid: 72 × 36 × 200; LatitudeLongitudeGrid; Float64.
MPI partition: 1 × 1 × 1; 1 ranks; 1 threads/rank.
Local resolution per rank: x 72–72 × y 36–36 × z 200. Exact per-rank sizes are in results.json.
Timing: 2 untimed steps, 1 windows of 1 steps; Δt=60 simulated seconds.
Validation: Current suite: rank completeness, finite fields, placement and timings checked.
Original run: `non_hydrostatic_models/rorqual/2026-10-13_pressure_solver_validation`; measured at 2026-10-13T14:03:57.027.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
