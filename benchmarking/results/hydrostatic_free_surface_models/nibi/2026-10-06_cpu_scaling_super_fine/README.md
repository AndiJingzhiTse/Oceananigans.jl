# CPU strong scaling on the super-fine grid

**Superseded:** use the [replacement core scaling series](../2026-10-06_cpu_scaling_cores_super_fine/README.md). Completed results are retained; unfinished jobs were cancelled.

Fixed global grid **1440 × 720 × 200**, starting at one full 192-core
Nibi CPU node, then 2, 4, 8, 16, 32, 64, 128, 256, and 512 nodes
(192 through 98,304 cores), followed by **675 nodes (129,600 cores)**,
the largest exact horizontal decomposition within the 699-node partition.
Each node runs one MPI rank with 192 Julia
threads bound to its physical cores; OpenBLAS uses one thread.

The horizontal grid partition is chosen to divide both dimensions exactly
and keep local horizontal grids balanced. The four-node scaling case uses
2×2×1. No vertical decomposition is used. This is hybrid MPI/thread scaling,
with a constant 192 threads per rank, rather than one MPI rank per core.

Slurm uses `def-fpoulin_cpu`, `cpubase_bynode_b1`, whole nodes and all node
memory, and one hour per scaling run. A test-only 1024-node request records
the next resource limit without allocating resources. The partition has
699 configured nodes; 1024 horizontal ranks also cannot evenly divide
1440×720. The final 675-node case uses 45×15×1; counts from 676 to 699
cannot divide the horizontal grid exactly. Actual submission failures stop
further requests and are preserved.

Benchmark settings match the Nibi GPU series: Float64, earth_ocean,
latitude–longitude without bathymetry, WENOVectorInvariantDefault, WENO7,
CATKE, T/S, SplitRungeKutta3, Δt=60 s, two warmup steps, then five windows
of ten steps. Each count has an independent Julia/MPI launch.

[Status, timings, highest verified count, and efficiency plot](plot.md)
are generated from validated results. Efficiency is relative to the
one-node (192-core) baseline, using the maximum of rank minimum/median
window times. Pending requests never count as successful runs.

Each `<count>_nodes/<partition>/` retains results.json, the suite report,
raw job output, exit code, timestamps, CPU affinity/thread/node information,
modules, and Slurm/source snapshots. Top-level records retain every
submission, accounting and queue evidence. Environment and source
snapshots are in `run_metadata/`.

A dependent CPU finalizer and login monitor update the plot and commit
completed measurements and terminal job outcomes. Queue estimates can
change; no queued count is promised to start by its estimate.

See the [analysis of the initial slowdown](analysis.md) for verified timing
comparisons, CPU utilization, timeout evidence and proposed diagnostics.
