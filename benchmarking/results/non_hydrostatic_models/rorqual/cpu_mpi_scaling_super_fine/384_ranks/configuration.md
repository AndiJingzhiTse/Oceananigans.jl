# Benchmark configuration

Model: NonhydrostaticModel; device: CPU.
Grid: 1440 × 720 × 200; LatitudeLongitudeGrid; Float64.
MPI partition: 24 × 16 × 1; 384 ranks; 1 threads/rank.
Local resolution per rank: x 60–60 × y 45–45 × z 200. Exact per-rank sizes are in results.json.
Timing: 2 untimed steps, 5 windows of 10 steps; Δt=60 simulated seconds.
Validation: Current suite: rank completeness, finite fields, placement and timings checked.
Original run: `non_hydrostatic_models/rorqual/2026-10-13_pressure_recovery_full_suite`; measured at 2026-10-13T16:42:35.679.

All recorded model and numerical settings are in configuration.json. The original per-rank measurements are in results.json.
