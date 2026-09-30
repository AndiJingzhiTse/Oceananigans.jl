# Rondeau suite — 2026-09-27

[Charts and performance tables](plots.md) cover adjacent CPU/GPU resolution scaling factors, CPU/GPU
MPI efficiency, and Nsight activity breakdowns. See the
[plotting instructions](../rondeau.md#plot-saved-results) to regenerate them.

Started at **2026-09-27 02:58:35 UTC** (2026-09-26 22:58:35 Toronto time).
The original folder was `2026-09-27T025835Z_all_3680654`.

Source revision: `bea98f6bc4a574dc6fb51b5cd9fc6fcfc247abfb`. The checkout had
local benchmark environment changes when the run started. The captured
`Manifest.toml` is an environment snapshot, not a project to instantiate here.
Hardware and Julia version snapshots are stored beside this file.

| Series | Completed configurations | Status |
|---|---|---|
| CPU resolution | 180 × 90 × 50, 360 × 180 × 50, 720 × 360 × 50 | Complete |
| GPU resolution | 180 × 90 × 50, 360 × 180 × 50, 720 × 360 × 50, 1440 × 720 × 50 | Complete |
| CPU MPI scaling default | 1, 2, 4, 8, 16, 32, 64, 128 ranks on 360 × 180 × 50 | Complete after targeted runs |
| CPU MPI scaling fine | 1, 2, 4, 8, 16, 32, 64, 128 ranks on 720 × 360 × 50 | Complete |
| GPU MPI scaling fine | 1, 2, 4 GPUs on 720 × 360 × 50 | Complete |
| GPU MPI scaling super fine | 1, 2, 4 GPUs on 1440 × 720 × 50 | Complete after targeted run |
| GPU profiling | 360 × 180 × 50, 720 × 360 × 50 | Complete |
| CPU profiling | 720 × 360 × 50 | Complete after targeted rerun |

Each completed configuration contains `results.json` and `results.md`. GPU
profiles also include `kernel_summary_cuda_gpu_kern_sum.csv`. Profiling timings
use fewer steps and samples than the timing series; compare the timing series
for performance measurements. For MPI results, use the slowest rank's step time.
CPU resolution switches from latitude longitude to tripolar geometry at 720.
Both CPU scaling series use tripolar geometry; GPU scaling fine uses tripolar
geometry and GPU scaling super fine uses plain latitude longitude geometry.
The benchmark bathymetry dataset has no 1440 × 720 tripolar file.
The 360 × 180 × 50 CPU resolution result is a different case from CPU scaling
default: it uses a plain latitude longitude grid without bathymetry.

The original CPU profiler launch rejected `--sampling-frequency=1000`. The
corrected case was rerun separately with `--sampling-period=1000000` and
`--backtrace=dwarf`. [CPU profiling provenance](run_metadata/2026-09-27T215707Z_nsys_cpu/README.md)
records the rerun. Its pie chart counts exclusive CPU leaf samples and includes
compilation and startup; 53.1% of samples have unresolved leaf symbols.

Raw logs and large profile files remain in this folder locally. Commands in
historical logs refer to the original folder name.

## CPU scaling extension

The 32-, 64-, and 128-rank cases were added in a targeted CPU scaling invocation
on 2026-09-27. All earlier result and report files were preserved byte for byte.
[Extension provenance](run_metadata/2026-09-27T200418Z_cpu_scaling/README.md)
records the command, revision, launcher changes, and environment snapshots.
The package manifest matches the original suite snapshot.

Step times below use the slowest rank; speedup is relative to the existing
one-rank MPI case (99.773 seconds per step).

| Ranks | Partition | Local grid | Seconds per step | Speedup |
|---|---|---|---|---|
| 32 | 8 × 4 × 1 | 90 × 90 × 50 | 5.836 | 17.10× |
| 64 | 8 × 8 × 1 | 90 × 45 × 50 | 3.784 | 26.37× |
| 128 | 16 × 8 × 1 | 45 × 45 × 50 | 2.142 | 46.58× |

## GPU super fine scaling extension

The 1440 × 720 × 50 latitude longitude run was added on 2026-09-30.
[Run provenance](run_metadata/2026-09-30T023910Z_gpu_scaling_super_fine/README.md)
records the MPI/GPU checks, CPU binding, environment, and individual results.
The one-GPU time of 0.503440 seconds per step agrees with the saved GPU
resolution result at the same grid (0.503266 seconds per step).

## CPU default scaling extension

The 360 × 180 × 50 tripolar scaling run was added on 2026-09-30.
[Run provenance](run_metadata/2026-09-30T014142Z_cpu_scaling_default/README.md)
records the per-rank grid sizes and the 128-rank partition retry. The final
128-rank time is 0.822501 seconds per step, or 30.671× speedup and 24.0% MPI
efficiency relative to the new one-rank baseline.
