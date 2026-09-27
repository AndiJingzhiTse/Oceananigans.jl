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
| CPU MPI scaling | 1, 2, 4, 8, 16 ranks on 720 × 360 × 50 | Complete |
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
