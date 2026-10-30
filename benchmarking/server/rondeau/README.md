# Rondeau GPU benchmark plan

[Resource/software settings](config.json) · [Authoritative workloads](series.json) · [Shared instructions](../../README.md)

This plan applies to both HydrostaticFreeSurfaceModel and NonhydrostaticModel,
each once as baseline and once with Dagger. The new Dagger execution method is
awaiting user instructions. This folder contains inputs and documentation, not measurements.

| Series | Cases |
|---|---|
| `gpu_resolution` | One GPU: 360 × 180 × 50; 720 × 360 × 100 |
| `gpu_scaling_default` | 360 × 180 × 50; 1, 2, 4 GPUs |
| `gpu_scaling_fine` | 720 × 360 × 100; 1, 2, 4 GPUs |
| `gpu_nsight_scaling_default` | 360 × 180 × 50; 1, 2, 4 GPUs, profiled |
| `gpu_nsight_scaling_fine` | 720 × 360 × 100; 1, 2, 4 GPUs, profiled |
| `gpu_weak_scaling` | default / 1 GPU(s), partition 1 × 1 × 1; fine / 4 GPU(s), partition 2 × 2 × 1 |

Default = 360 × 180 × 50; fine = 720 × 360 × 100;
super_fine = 1440 × 720 × 200. All grids use LatitudeLongitudeGrid.
Unspecified scaling partitions are balanced. No cases beyond the listed bounds
are appended. Partition benchmarks, CPU benchmarks and ensembles are not selected.
The six series contain 16 cases per model and execution mode.

Weak scaling doubles cells/GPU at each step: 3,240,000; 6,480,000.
Use the documented linear cell-count reference, not constant-work weak efficiency.

Rondeau uses local execution and has no scheduler. Check live GPU ownership
before running; wait for occupied GPUs without reserving idle ones.
The superseded hydrostatic wrapper controller was stopped while waiting for GPUs.
Its [historical runbook](history/hydrostatic_dagger_2026-10-30.md) and completed
measurements are retained. No replacement jobs have been launched.

- [hydrostatic_free_surface_models baseline, Dagger and comparisons](../../results/hydrostatic_free_surface_models/rondeau/README.md)
- [non_hydrostatic_models baseline, Dagger and comparisons](../../results/non_hydrostatic_models/rondeau/README.md)

Each model/server results folder contains `baseline/`, `dagger/` and generated
comparison reports when matched measurements exist. Existing root-level historical
series retain their original provenance; they are not new-plan measurements.
