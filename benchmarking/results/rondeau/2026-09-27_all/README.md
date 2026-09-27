# Rondeau suite — 2026-09-27

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
| CPU MPI scaling | 1, 2, 4, 8, 16, 32, 64, 128 ranks on 720 × 360 × 50 | Complete |
| GPU MPI scaling | 1, 2, 4 GPUs on 720 × 360 × 50 | Complete |
| GPU profiling | 360 × 180 × 50, 720 × 360 × 50 | Complete |
| CPU profiling | 720 × 360 × 50 | Failed before launching Julia |

Each completed configuration contains `results.json` and `results.md`. GPU
profiles also include `kernel_summary_cuda_gpu_kern_sum.csv`. Profiling timings
use fewer steps and samples than the timing series; compare the timing series
for performance measurements. For MPI results, use the slowest rank's step time.
CPU resolution switches from latitude longitude to tripolar geometry at 720.

The CPU profiler rejected `--sampling-frequency=1000`; no CPU profile or results
were produced. The suite now uses `--sampling-period=1000000` and
`--backtrace=dwarf`, both supported by Rondeau's Nsight Systems 2024.5.1.
The corrected CPU benchmark profile has not been rerun.

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
