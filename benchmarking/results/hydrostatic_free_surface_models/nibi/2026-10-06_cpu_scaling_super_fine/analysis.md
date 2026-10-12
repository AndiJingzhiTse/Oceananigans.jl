# Analysis of the initial CPU scaling results — October 6, 2026

The regression is real in the recorded measurements. Four nodes are about
36.5% slower than one node using fastest windows, and 37.3% slower using
median windows. This series measures an untuned hybrid configuration:
one MPI rank per node with 192 Julia threads. Its efficiency includes
thread scheduling, serial work, memory locality and MPI waiting; it does
not isolate communication efficiency.

| Nodes | Cores | Fastest s/step | Median s/step | Fastest speedup | Ideal fastest s/step | Fastest efficiency |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 192 | 42.336905 | 42.712967 | 1.000× | 42.336905 | 100.0% |
| 2 | 384 | 39.997439 | 44.307615 | 1.058× | 21.168452 | 52.9% |
| 4 | 768 | 57.774982 | 58.626502 | 0.733× | 10.584226 | 18.3% |

The timing units and arithmetic are correct: each window measures ten
steps, and the report divides its elapsed time by ten. Per-rank minimum
and median times are aggregated by taking the maximum across ranks. The
JSON records have the correct local grids, all ranks are present, and all
records report 192 threads on the same Xeon 6972P hardware model. Slurm
allocated exclusive nodes with 192 physical cores per task and no SMT.

Four-node fastest rank times range from 57.493 to 57.775 s/step, a spread
of about 0.5%. Rank timing agreement does not exclude a slow rank forcing
other ranks to wait, but the loss is not an accidental extra rank or
incorrect aggregation. Minimum and median statistics both show it, so
choosing another plotted statistic would not resolve the regression.

The independent [four-node partition comparison](../2026-10-06_cpu_partition_super_fine/plot.md)
replicates the slow throughput on the same allocated nodes within that
series: 4×1×1 takes 51.668704 s/step; 2×2×1 takes 55.448350; 1×4×1 takes
50.645297. The best layout is about 9.5% faster than 2×2×1, but remains
about 19.6% slower than the separate one-node measurement. Changing layout
helps modestly and does not account for the whole regression.

## CPU utilization evidence

[Captured Slurm accounting](analysis_accounting.txt) gives these averages
for each Julia benchmark step (`.1`), including imports, compilation,
model construction, warmup and timed windows:

| Nodes | Allocated cores | Average active core equivalents | CPU utilization |
|---:|---:|---:|---:|
| 1 | 192 | 44.35 | 23.10% |
| 2 | 384 | 66.74 | 17.38% |
| 4 | 768 | 103.20 | 13.44% |
| 8 | 1536 | 183.79 | 11.97% |
| 16 | 3072 | 329.46 | 10.72% |
| 32 | 6144 | 654.16 | 10.65% |

Average active cores = TotalCPU seconds / elapsed seconds. Utilization
divides this by allocated cores. These are whole-step averages, not a
profile of the timed windows; they establish poor use of the allocations
but cannot separate MPI wait, thread synchronization, serial phases or
compilation. Memory stalls alone also cannot be inferred from CPU time.
The 8-, 16- and 32-node allocations ended in TIMEOUT at the one-hour limit;
`INTERRUPTED` in the live report means their case never wrote a final exit
code/results file. It does not mean they remain running. All three had
entered the timed benchmark phase before timeout.

## Leading explanation and what remains unproved

The strongest configuration concern is using a 192-thread team for every
CPU kernel without tuning or explicitly pinning individual Julia threads.
The node has two sockets and six NUMA domains of 32 cores each. Its recorded
process affinity is `0-191`: this allows execution anywhere on the node.
The script does not assign a distinct physical core to each Julia thread,
and does not control NUMA placement of model arrays.
[Slurm's binding documentation](https://slurm.schedmd.com/cpu_management.html)
describes binding tasks to CPU masks;
[Julia's threading documentation](https://docs.julialang.org/en/v1.10/manual/multi-threading/)
describes task migration between threads. Neither process affinity nor a
reported thread count proves efficient use of all cores.

Local source evidence makes thread-launch overhead a concrete suspect:

- [CPU architecture backend](../../../../src/Architectures.jl) uses
  `KernelAbstractions.CPU()`. Installed KernelAbstractions 0.9.43 defaults
  to `static=false`; its `src/cpu.jl`, lines 98–125, spawns a task for each
  participating thread and waits for the team on each kernel invocation.
- [CPU workgroup layout](../../../../src/Utils/kernel_launching.jl), lines
  147–152, assigns a contiguous first-dimension row to a workgroup. Small
  horizontal kernels offer relatively little work per thread as local
  grids shrink, while the requested team remains 192 threads.
- [The model](../../../src/earth_ocean.jl) fixes the split-explicit free
  surface at 30 requested substeps. Its
  [substepping loop](../../../../src/Models/HydrostaticFreeSurfaceModels/SplitExplicitFreeSurfaces/step_split_explicit_free_surface.jl)
  repeatedly invokes small horizontal kernels, in addition to the large
  three-dimensional kernels and distributed halo exchanges.

These facts support a hypothesis of excessive thread-team synchronization,
possible NUMA/locality penalties and added MPI/halo overhead outweighing
the shrinking local workload. No timed-region profile or controlled
thread-count experiment has yet measured their individual contributions.
It would be premature to identify NUMA, network bandwidth, or one specific
kernel as the confirmed root cause. The previous validation checks verified
allocation and result consistency; they did not validate performance.
Using 192 Julia threads without first measuring thread scaling was an
unvalidated performance assumption in the initial benchmark setup.

## Targeted next experiments

Keep the original data and isolate the execution configuration before
extending wall time or interpreting large-node failures as a scaling limit:

1. On the same one-node allocation and fixed global grid, compare 32, 64,
   96 and 192 threads with explicit per-thread core pinning. Record actual
   thread affinities and NUMA placement; profile only after warmup.
2. Profile timestep components, CPU task scheduling and MPI waits on one
   and four nodes. Record individual window wall times and CPU time, not
   only whole-allocation averages.
3. Compare full-node hybrid layouts such as six MPI ranks × 32 threads
   (one rank per NUMA domain) or two ranks × 96 threads (one per socket).
   Keep 192 allocated cores per node and choose matching exact grid
   partitions. These change the MPI decomposition and should form a
   separate comparison rather than silently replacing the original
   four-rank partition series.
4. Rerun one, two and four nodes with the measured best configuration.
   Only then use its one-node baseline to assess scaling to more nodes.

No benchmark settings or queued jobs were changed during this analysis.
