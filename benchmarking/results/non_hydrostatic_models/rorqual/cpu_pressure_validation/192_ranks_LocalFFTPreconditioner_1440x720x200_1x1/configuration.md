# Benchmark configuration

Model: NonhydrostaticModel; device: CPU.
Grid: 1440 × 720 × 200; LatitudeLongitudeGrid; Float64.
MPI partition: 16 × 12 × 1; 192 ranks; 1 threads/rank.
Local resolution per rank: x 90–90 × y 60–60 × z 200. Exact per-rank sizes are in results.json.
Timing: 2 untimed steps, 1 windows of 1 steps; Δt=60 simulated seconds.
Validation: Current suite: rank completeness, finite fields, placement and timings checked.
Original run: `non_hydrostatic_models/rorqual/2026-10-13_refined_pressure_validation`; measured at 2026-10-13T14:57:26.723.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
