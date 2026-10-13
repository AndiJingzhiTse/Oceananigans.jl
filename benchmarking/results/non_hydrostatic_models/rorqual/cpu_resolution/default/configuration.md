# Benchmark configuration

Model: NonhydrostaticModel; device: CPU.
Grid: 360 × 180 × 50; LatitudeLongitudeGrid; Float64.
MPI partition: 1 × 1 × 1; 1 ranks; 1 threads/rank.
Local resolution per rank: x 360–360 × y 180–180 × z 50. Exact per-rank sizes are in results.json.
Timing: 2 untimed steps, 5 windows of 10 steps; Δt=60 simulated seconds.
Validation: Current suite: rank completeness, finite fields, placement and timings checked.
Original run: `non_hydrostatic_models/rorqual/2026-10-13_full_suite`; measured at 2026-10-13T13:03:51.554.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
