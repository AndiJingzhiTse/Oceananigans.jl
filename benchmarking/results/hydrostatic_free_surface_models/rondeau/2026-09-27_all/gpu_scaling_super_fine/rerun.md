# GPU super fine rerun — 1440 × 720 × 200

Started at 2026-10-05T17:26:09.669539+00:00 on Rondeau from revision `68e882783607867e637d1c558135ff0a8f4968d7`.
The 1-, 2-, and 4-GPU cases replace the previous 50-level results in this
same folder. The global grid is 1440 × 720 × 200, plain latitude longitude
without bathymetry. Parameters are Float64, WENOVectorInvariantDefault,
WENO7, CATKE, SplitRungeKutta3, T and S, dt = 60 simulated seconds,
2 warmup steps, and 5 samples of 10 steps. Each rank has one Julia thread.

The benchmark manifest SHA256 is `ef972b872bd1722adbffce2f604cbd60cc142b6a884e242cfd05e45f861f49f8`.
Julia 1.12.7 uses the configured CUDA-aware Open MPI 4.1.7 environment.
The suite launcher was bypassed for this targeted replacement.

```bash
source ~/.config/oceananigans/rondeau-env.sh
export CUDA_VISIBLE_DEVICES=0,1,2,3
export JULIA_CUDA_MEMORY_POOL=none OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
rankfile=benchmarking/results/rondeau/2026-09-27_all/run_metadata/2026-09-30T023910Z_gpu_scaling_super_fine/gpu_rankfile.txt
# Use count/partition pairs 1/1x1x1, 2/1x2x1, and 4/2x2x1.
mpiexec -n "$count" --rankfile "$rankfile" --report-bindings \
  julia --threads=1 --project=benchmarking benchmarking/run_benchmarks.jl \
  --float_type=Float64 --momentum_advection=WENOVectorInvariantDefault \
  --tracer_advection=WENO7 --closure=CATKE --timestepper=SplitRungeKutta3 \
  --tracers=T,S --dt=60 --warmup_steps=2 --time_steps=10 --samples=5 \
  --device=GPU --size=1440x720x200 --grid_type=lat_lon --distributed \
  --partition="$partition" \
  --output="benchmarking/results/rondeau/2026-09-27_all/gpu_scaling_super_fine/${count}_gpus/results.json"
```

Each count runs `check_rondeau_mpi.jl GPU "$count"` first with the same launcher
and binding. Rank 0/1/2/3 map to GPUs 0/1/2/3 and CPU cores 48/16/112/80,
respectively, matching GPU NUMA affinity. MPI checks and raw benchmark logs
remain in the existing configuration folders and are ignored by Git.

The one-GPU case [failed before warmup](1_gpus/attempt.md) because the grid
exceeded one A100's available memory. Its old 50-level result was removed.

Both the 2- and 4-GPU cases completed successfully, and MPI/CUDA checks
passed for all three attempted counts. Times use the slowest rank.

| GPUs | Partition | Local grid | Seconds per step | Speedup vs 2 GPUs | Relative MPI efficiency |
|---:|---|---|---:|---:|---:|
| 2 | 1 × 2 × 1 | 1440 × 360 × 200 | 0.991023 | 1.000× | 100.0% |
| 4 | 2 × 2 × 1 | 720 × 360 × 200 | 0.517122 | 1.916× | 95.8% |

The two-GPU baseline is normalized to 100%. This reports scaling from two
to four GPUs; it does not estimate efficiency relative to an unmeasured
one-GPU execution. The former 50-level results remain in Git history.
