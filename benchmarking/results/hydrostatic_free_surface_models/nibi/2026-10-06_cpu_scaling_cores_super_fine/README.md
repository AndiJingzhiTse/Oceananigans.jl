# Replacement CPU scaling: three cores through full nodes

This is the active replacement for the
[initial 192-thread-per-rank CPU sweep](../2026-10-06_cpu_scaling_super_fine/README.md).
Its unfinished scaling allocations and finalizer were cancelled; completed
results and timeout evidence are retained in the original directory.

The fixed **1440 × 720 × 200** super-fine grid uses
**LatitudeLongitudeGrid**, Float64, earth_ocean without bathymetry,
WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3 and Δt=60 s.
Every benchmark uses two warmup steps and five windows of ten steps.

The default layout uses **one MPI rank per physical core and one explicitly
pinned Julia thread per rank**, avoiding the original 192-thread teams.
The core sequence starts at 3 and doubles. Nibi has 192 cores per standard
compute node (two 96-core sockets); thus 192 cores means one full node.

| Cores / MPI ranks | Nodes | MPI partition | Local resolution per rank |
|---:|---:|---|---|
| 3 | part of 1 | 3×1×1 | 480×720×200 |
| 6 | part of 1 | 3×2×1 | 480×360×200 |
| 12 | part of 1 | 4×3×1 | 360×240×200 |
| 24 | part of 1 | 6×4×1 | 240×180×200 |
| 48 | part of 1 | 8×6×1 | 180×120×200 |
| 96 | part of 1 | 12×8×1 | 120×90×200 |
| 192 | 1 | 16×12×1 | 90×60×200 |
| 384 | 2 | 24×16×1 | 60×45×200 |
| 768 | 4 | 32×24×1 | 45×30×200 |
| 1536 | 8 | 32×48×1 | 45×15×200 |
| 3072 | 16 | 64×48×1 | (22–23)×15×200 |
| 6144 | 32 | 96×64×1 | 15×(11–12)×200 |
| 12288 | 64 | 128×96×1 | (11–12)×(7–8)×200 |

Balanced `Sizes` partitions distribute remainder cells across ranks with
at most one cell difference in each direction; every global grid cell is
preserved. The next doubling, 24,576 cores (128 nodes), has no horizontal
partition with all local dimensions at least seven cells, as required by
the model's seven-cell halo. Vertical decomposition is not used. This
geometry limit is recorded separately from Slurm rejection or run failure.

All counts use `SplitExplicitFreeSurface(substeps=30, extend_halos=false)`.
This communicates halos at each barotropic substep and avoids the default
extended halos exceeding the small rank-local domains. The requested 30
substeps have 21 nonzero/retained averaging weights. The original sweep
used `extend_halos=true`; that strategy difference is recorded and must
be considered when comparing the two series. Default settings of the
shared benchmark case remain unchanged for existing callers.

Slurm requests exactly the tested core count, one core/task for MPI mode,
and the same Xeon generation (`--constraint=granite`). Partial-node runs
request memory separately: 64 GiB plus 4 GiB per local MPI rank, allowing
for the full grid and Julia processes. They reserve only their requested
cores, so other jobs may share the node. Full-node runs use exclusive
192-core nodes and all node memory. OpenBLAS and Julia GC each use one
thread per process; Julia's computation thread is pinned to its assigned
core. Distinct core affinities are verified across ranks on each node.
Nibi selects the Slurm partition automatically from the request's wall time,
memory per core and whole-node use; small-core runs need a high-memory class.

Wall-time limits are 24 hours for 3 cores, 12 hours for 6, 6 hours for 12,
and 3 hours for subsequent counts. Small-core full-grid runs take longer;
queued requests and timeouts are always distinguished from completed runs.

[Live status, timing plot and MPI efficiency](plot.md) use the validated
three-core baseline. Efficiency = t₃ × 3 / (tₚ × p). The maximum of rank
minimum/median ten-step window times is reported. No efficiency is claimed
before the three-core run completes and passes validation.

Each `<count>_cores/` records configuration.json/configuration.md with
MPI partition, global and local resolution, grid type, rank/thread counts
and model settings; raw results.json/results.md; CPU layout and per-thread
core affinities; raw job output, exit code, source/module/Slurm snapshots.
The root retains submission/accounting/queue evidence and a source and
environment snapshot. Rank results are gathered and written once on rank
zero, avoiding serial read/append/rewrite by thousands of ranks.

Submit and monitor from the repository root:

```bash
python3 benchmarking/results/nibi/cpu_core_scaling.py benchmarking/results/nibi/2026-10-06_cpu_scaling_cores_super_fine --submit
module load python/3.11 scipy-stack/2025a
python3 benchmarking/results/nibi/cpu_core_scaling.py benchmarking/results/nibi/2026-10-06_cpu_scaling_cores_super_fine --watch --commit
python3 -m unittest discover -s benchmarking/results/nibi -p 'test_cpu_core_scaling.py'
```

Submission automatically schedules a dependent CPU finalizer. A login
monitor records progress and commits terminal results; the finalizer
provides reporting after all jobs finish if the login monitor stops.
`--layout threads` is available for a separate explicitly pinned thread
sweep; it is not the default replacement series.
