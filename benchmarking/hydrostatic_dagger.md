# Rondeau hydrostatic GPU baseline versus Dagger

Use the original whole-function wrapper in `src/suite/worker.jl`:
baseline calls `synchronized_window!` directly; Dagger spawns that same function
once per timing window and immediately fetches it. Each rank retains its model,
MPI communicator, one computation thread and assigned GPU. No solver or model
kernel is replaced by a Dagger implementation.

## Cases

| Series | Resolution and resources |
|---|---|
| `gpu_resolution` | 360 × 180 × 50, 720 × 360 × 100, 1440 × 720 × 200; one GPU |
| `gpu_scaling_super_fine` | 1440 × 720 × 200; 1, 2 and 4 GPUs |
| `gpu_partition_super_fine` | 1440 × 720 × 200; all horizontal partitions on 1, 2 and 4 GPUs |
| `gpu_nsight_scaling_super_fine` | 1440 × 720 × 200; 1, 2 and 4 GPUs with Nsight |
| `gpu_weak_scaling_super_fine` | 1440 × 720 × 200 on one GPU; 2880 × 1440 × 200 on four GPUs |
| `gpu_scaling_super_super_fine` | 2880 × 1440 × 200; four-GPU baseline |
| `gpu_scaling_super_super_super_fine` | 5760 × 2880 × 200; requires at least 16 GPUs, unavailable here |

There are 18 physically eligible cases per variant (36 executions) and additional
explicit resource/geometry boundaries. Memory failures remain recorded outcomes;
do not lower resolution or change numerical settings to make a case pass.
CPU series are excluded. Available smaller cases run before cases waiting for
larger GPU allocations. Four-GPU cases require all four devices to be idle.

Both paths use HydrostaticFreeSurfaceModel, LatitudeLongitudeGrid without
bathymetry, Float64, WENOVectorInvariantDefault momentum, WENO7 T/S advection,
CATKE, TEOS10 buoyancy, spherical Coriolis and SplitRungeKutta3.
The timestep is 60 simulated seconds through 1440 × 720 × 200, then 30 and
15 seconds at the two larger horizontal resolutions. Request 30 free-surface
substeps with extended halos; record the actual retained substeps.
Seed initial perturbations with 1234 plus rank in both variants.

Two untimed warmup steps precede five synchronized windows of ten steps.
Report fastest and median seconds per step using the slowest-rank statistic.
Alternate variant order between cases and use the same physical GPUs per pair.
Profiler comparisons use only the corresponding profiled baseline.
These are paired shared-server measurements, not repeatability or exclusive-node
claims. Speedup = baseline / Dagger, with equal time = 1.

## Execution

Run from the sole checkout `/u/ajtse/Oceananigans.jl`. The isolated environment,
config, execution logs and study are under `.runtime/hydrostatic_dagger_2026-10-30/`.
The config pins Julia, CUDA-aware OpenMPI and one computation thread per rank.
No files are written to `/tmp`, `/var/tmp` or `/local_scratch`.

```sh
export TMPDIR=/u/ajtse/Oceananigans.jl/.runtime/tmp
export TMP="$TMPDIR" TEMP="$TMPDIR" OMPI_MCA_orte_tmpdir_base="$TMPDIR"
export PYTHONDONTWRITEBYTECODE=1
python3 benchmarking/scripts/compare_dagger.py \
  --config .runtime/hydrostatic_dagger_2026-10-30/config.json \
  --project .runtime/hydrostatic_dagger_2026-10-30/environment \
  --study .runtime/hydrostatic_dagger_2026-10-30/study \
  --publish benchmarking/results/hydrostatic_free_surface_models/rondeau \
  --model HydrostaticFreeSurfaceModel --gpu-only --wait-for-gpus --commit \
  --series gpu_resolution,gpu_scaling_super_fine,gpu_partition_super_fine,gpu_nsight_scaling_super_fine,gpu_weak_scaling_super_fine,gpu_scaling_super_super_fine,gpu_scaling_super_super_super_fine
```

Use `--plan` to review without executing. The same command resumes completed
terminal outcomes; inspect any `RUNNING` marker before resuming an interrupted
controller. Each execution has a 30-minute limit including startup, timing and
profiler processing. Actual prior runs suggest minutes per feasible case;
budget approximately 1–3 hours of execution plus an unknown wait for four idle
GPUs. The process exits and releases resources when its case completes.

Inspect `study/progress.json`, `controller.log`, per-case `job.out` and the
variant `suite.json` files under that runtime directory. The controller records
waiting states without occupying GPUs. It checks source fingerprints before
each case, so stop the study before switching branches or editing physics.
It stops before a new Nsight capture if less than 32 GiB of storage is free.

## Retained records

Publish only accepted cases under
`results/hydrostatic_free_surface_models/rondeau/{baseline,dagger}/<series>/`.
`comparison.md` and `comparison.csv` compare every selected series and include
failures and resource limits without inventing ratios. `previous_results.md`
preserves the earlier machine report; those historical measurements are not
substituted for the fresh paired baseline.

Large captures stay in each variant's `<series>/raw_profiles/` directory with
checksums and sizes in `profile_manifest.json`. Closed execution evidence is
archived under `run_records/` and excluded from Git. Temporary originals are
removed only after the owning run exits and copies are verified. Scientific
metadata and reports are committed separately from these large raw artifacts.
