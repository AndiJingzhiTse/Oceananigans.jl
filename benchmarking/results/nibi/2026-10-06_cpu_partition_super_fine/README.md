# Four-node CPU partition comparison on the super-fine grid

Global grid **1440 × 720 × 200**, four full 192-core CPU nodes (**768 cores**).
One MPI rank per node uses 192 Julia threads bound to its physical cores.
The three cases run sequentially on the same allocated nodes, each in
fresh Julia/MPI processes:

| Partition | Local grid per CPU node | Cells per node |
|---|---|---:|
| 4×1×1 | 360 × 720 × 200 | 51,840,000 |
| 2×2×1 | 720 × 360 × 200 | 51,840,000 |
| 1×4×1 | 1440 × 180 × 200 | 51,840,000 |

Float64, earth_ocean, latitude–longitude without bathymetry,
WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3, Δt=60 s,
two warmup steps, then five windows of ten steps per case.
Slurm account `def-fpoulin_cpu`, partition `cpubase_bynode_b1`, whole-node
memory, and a three-hour allocation limit cover all three cases.

[Status and comparison plot](plot.md) compare maximum rank fastest/median
window step times. Speedup uses the fresh 2×2×1 measurement as reference.
Only validated results enter the plot. A failed case preserves its evidence
and allows the following case to run while time remains.

Each partition directory retains raw results, logs, exit code, CPU layout,
affinity, thread count, Slurm allocation and source/module snapshots.
A dependent CPU finalizer and login monitor generate the report and
commit validated measurements and terminal job outcomes.
