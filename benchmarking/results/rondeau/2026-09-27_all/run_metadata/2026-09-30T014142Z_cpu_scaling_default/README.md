# CPU scaling default extension

Started at 2026-09-30 01:41:42 UTC on Rondeau. Validated 1–64 rank results
were moved to `../../cpu_scaling_default/`. All cases use a 360 × 180 × 50
tripolar grid with immersed partial-cell bathymetry, one Julia thread per
rank, Float64, WENOVectorInvariantDefault, WENO7, CATKE,
SplitRungeKutta3, T and S, a 60-second simulated time step, 2 warmup
steps, and 5 samples of 10 steps. Each result file has one record per rank;
the chart uses the slowest rank.

The first 128-rank attempt used the fine-series 16 × 8 × 1 partition. It
aborted during immersed-boundary halo communication with `MPI_ERR_IN_STATUS`
and produced no usable timing. Its log remains under
`cpu_scaling_default/128_cores/run.log` in this metadata folder. The
successful [128-rank retry](../2026-09-30T042636Z_cpu_scaling_default_128_retry/README.md)
used 8 × 16 × 1, which divides the tripolar x direction evenly. The retry
result was moved to the same `../../cpu_scaling_default/` series.

The first run captured revision `81f14ef261de6ea7bdfe6612ed5316123a0e9524`
plus local launcher changes. The retry captured revision
`bc597069c244d401d5cbf8112f357fe4ee6fad32`. Between those runs, the
workspace gained optional `coriolis` and `buoyancy` arguments in the
benchmark runner and `earth_ocean`; their defaults preserve spherical
Coriolis and TEOS-10 seawater buoyancy used by the 1–64 rank cases.
Environment and hardware snapshots for each launch are saved beside their
respective README files.

| CPU ranks | Partition | Local grid(s) | Slowest rank (s/step) |
|---:|---|---|---:|
| 1 | 1 × 1 × 1 | 360 × 180 × 50 | 25.226968 |
| 2 | 1 × 2 × 1 | 360 × 90 × 50 | 15.939943 |
| 4 | 2 × 2 × 1 | 180 × 90 × 50 | 8.648960 |
| 8 | 2 × 4 × 1 | 180 × 45 × 50 | 4.970663 |
| 16 | 4 × 4 × 1 | 90 × 45 × 50 | 2.949576 |
| 32 | 8 × 4 × 1 | 45 × 45 × 50 | 1.635220 |
| 64 | 8 × 8 × 1 | 45 × 22 × 50; 45 × 26 × 50 | 1.222766 |
| 128 | 8 × 16 × 1 | 45 × 11 × 50; 45 × 15 × 50 | 0.822501 |
