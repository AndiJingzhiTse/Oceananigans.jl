# Pre-submission validation

- Five controller/reporting unit tests passed: all six grid partitions,
  per-rank artifact completeness, kernel aggregation, duplicate-GPU and
  finite-state rejection, partial job failure, and accounting outage fallback.
- Bash syntax passed for the rank launcher, allocation script and finalizer.
- Python controller compilation passed.
- Julia source parsed, and CUDA.CUDACore.cuProfilerStart/cuProfilerStop exist
  in the installed benchmark environment.
- GPU execution and actual CUPTI capture remain pending Slurm allocation.

Submitted allocations: 23324756 (1 GPU), 23324758 (2 GPUs), 23324759 (4 GPUs).
After-any report finalizer: 23324760.
Login-host monitor log: /scratch/anditse/nibi_nsight_watch.log.
