# GPU scaling super fine extension

These 50-level measurements were superseded by the
[200-level rerun](../../gpu_scaling_super_fine/rerun.md) on 2026-10-05.
The current results folders contain that replacement; the timings below
describe the original run and are preserved as historical provenance.

Started at 2026-09-30 02:39:10 UTC on Rondeau. Results were added to
`../../gpu_scaling_super_fine/` after the original 2026-09-27 suite.
This extension uses a 1440 × 720 × 50 plain latitude longitude grid without
bathymetry. The benchmark bathymetry dataset has no tripolar file at this
resolution. All other model and timing options match the fine GPU scaling run:
Float64, WENOVectorInvariantDefault, WENO7, CATKE, SplitRungeKutta3, T and S,
60 simulated seconds per step, 2 warmup steps, and 5 samples of 10 steps.

The run used `gpu_mpiexec_wrapper.sh` as `MPIEXEC`. It removed the suite's
default `--map-by core --bind-to core` arguments and supplied
`--rankfile gpu_rankfile.txt`. Rank 0/1/2/3 were bound to cores
48/16/112/80 respectively, corresponding to the CPU affinity of GPU 0/1/2/3
reported by `nvidia-smi topo -m`. The wrapper used `/tmp/rondeau_gpu_rankfile`
at run time; that exact file is preserved here as `gpu_rankfile.txt`.
The placement avoided the cores used by a concurrent CPU scaling run.
The GPU and CPU series still shared the server's memory and I/O resources.

| GPUs | Partition | Local grid | Slowest rank (s/step) | MPI efficiency |
|---:|---|---|---:|---:|
| 1 | 1 × 1 × 1 | 1440 × 720 × 50 | 0.503440 | 100.0% |
| 2 | 1 × 2 × 1 | 1440 × 360 × 50 | 0.257514 | 97.7% |
| 4 | 2 × 2 × 1 | 720 × 360 × 50 | 0.140908 | 89.3% |

All MPI/CUDA checks passed. The run folder also contains the repository
revision, Julia version, hardware snapshots, and manifest captured at launch.
