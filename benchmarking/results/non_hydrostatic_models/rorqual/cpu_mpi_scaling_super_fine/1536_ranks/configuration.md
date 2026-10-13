# Benchmark configuration

Model: NonhydrostaticModel; device: CPU.
Grid: 1440 × 720 × 200; LatitudeLongitudeGrid; Float64.
MPI partition: 32 × 48 × 1; 1536 ranks; 1 threads/rank.
Local resolution per rank: x 45–45 × y 15–15 × z 200. Exact per-rank sizes are in results.json.
Timing: 2 untimed steps, 5 windows of 10 steps; Δt=60 simulated seconds.
Validation: Current suite: rank completeness, finite fields, placement and timings checked.
Original run: `non_hydrostatic_models/rorqual/2026-10-13_pressure_recovery_full_suite`; measured at 2026-10-13T15:59:42.186.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
