# CPU profiling rerun provenance

Started at 2026-09-27 21:57:07 UTC on Rondeau. Only the previously failed
CPU profiling case was rerun to obtain the CPU sample pie chart.
Resolution and MPI scaling measurements were not rerun.

```bash
source ~/.config/oceananigans/rondeau-env.sh
OUTPUT_ROOT=/local_scratch/ajtse/rondeau-plot-profiles \
    bash benchmarking/results/rondeau/run_rondeau_suite.sh nsys_cpu
```

The invocation also set `CPU_COUNTS=1`, which has no effect on the CPU
profiling case. The profile uses one Julia thread, a 720 × 360 × 50 tripolar
grid, Float64, WENOVectorInvariantDefault, WENO7, CATKE, SplitRungeKutta3,
tracers T and S, dt = 60 seconds, two warmup steps and one sample of two
measured steps. Nsight Systems uses process-tree sampling, a 1,000,000-cycle
sampling period and DWARF backtraces. Compilation and startup are captured.

The captured revision and environment snapshots describe this rerun rather
than the original suite. Plotting changes were in progress during the rerun;
the benchmark launcher was unchanged from the captured revision.

The compact `cpu_sample_summary.csv` is generated from the exported local
capture by `plot_rondeau_results.py --cpu-sqlite`. Every composite sampling
event is assigned exactly once to its stack-depth-zero frame, with absent
frames retained as unresolved. Unresolved address entries are aggregated by
module; all resolved leaf symbols are retained. Full captures, SQLite files and raw logs remain
local and are not committed.

The rerun completed successfully. Its package manifest matches the original
suite snapshot byte for byte. The profiled measurement was 100.471697 seconds
per step; use the separate timing series for performance comparisons.
