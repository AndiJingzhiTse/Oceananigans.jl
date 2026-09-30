# CPU scaling default 128-rank retry

Started at 2026-09-30 04:26:36 UTC on Rondeau with `CPU_COUNTS=128` and
suite `cpu_scaling_default`. The run used an 8 × 16 × 1 partition of the
360 × 180 × 50 tripolar grid. All 128 MPI ranks completed; the slowest
rank measured 0.822501 seconds per step. Local grids are 45 × 11 × 50
or 45 × 15 × 50. The validated JSON and Markdown report are in
`../../cpu_scaling_default/128_cores/`.

The earlier 16 × 8 × 1 attempt failed during immersed-boundary halo
communication; see the [initial run](../2026-09-30T014142Z_cpu_scaling_default/README.md).
This run retained Float64, WENOVectorInvariantDefault, WENO7, CATKE,
SplitRungeKutta3, T and S, spherical Coriolis, TEOS-10 seawater buoyancy,
one Julia thread per rank, a 60-second simulated time step, 2 warmup steps,
and 5 samples of 10 steps. Source revision and environment snapshots are
saved in this folder. The checkout had local changes at launch.
