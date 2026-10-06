# Super-fine grid partition comparison

This series compares three decompositions of the same global
**1440 × 720 × 200** grid, with **four H100 GPUs and four MPI ranks**:

| Partition | Local grid per rank | Cells per rank |
|---|---|---:|
| 4×1×1 | 360 × 720 × 200 | 51,840,000 |
| 2×2×1 | 720 × 360 × 200 | 51,840,000 |
| 1×4×1 | 1440 × 180 × 200 | 51,840,000 |

The three cases run sequentially in the listed order within one four-GPU
allocation on one node. Every case starts fresh Julia/MPI processes,
verifies distinct GPUs and CUDA-aware MPI, and builds a new model.
This keeps the same allocated GPU set and avoids running competing cases simultaneously.

Settings match the existing Nibi super-fine benchmarks: Float64,
latitude–longitude without bathymetry, WENOVectorInvariantDefault,
WENO7, CATKE, T/S, SplitRungeKutta3, Δt = 60 s, two warmup steps,
then five timing windows of ten steps each.

The allocation requests four H100 GPUs, eight CPUs per rank, 64 GiB host
memory, and a 30-minute limit covering all three cases. Julia and OpenBLAS
each use one thread per rank. Fresh cases can incur compilation cost during
setup/warmup; their timed windows follow the same procedure as the reference.

The generated `plot.md` and `partition_comparison.svg` compare fastest and
median step times. Relative speedup uses the fresh `2x2x1` measurement as
the reference. Only validated four-rank results enter the chart.
Each partition directory contains its own results, logs, exit code,
hardware/module snapshots, and source revision. Allocation-level Slurm
status and submission records live here; environment snapshots are in
`run_metadata/`.

Run and monitor using the [parent instructions](../README.md).

Submitted as GPU job **23304598**. CPU job **23304609** runs after the
allocation finishes to validate results, generate the comparison plot,
and commit the collected records. See the [comparison report](plot.md)
for the latest recorded status and measurements.
