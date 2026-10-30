# Rorqual GPU benchmark plan

[Resource/software settings](config.json) · [Authoritative workloads](series.json) · [Shared instructions](../../README.md)

This plan applies to both HydrostaticFreeSurfaceModel and NonhydrostaticModel,
each once as baseline and once with Dagger. The new Dagger execution method is
awaiting user instructions. This folder contains inputs and documentation, not measurements.

| Series | Cases |
|---|---|
| `gpu_resolution` | One GPU: 360 × 180 × 50; 720 × 360 × 100; 1440 × 720 × 200 |
| `gpu_scaling_default` | 360 × 180 × 50; 1, 2, 4, 8, 16 GPUs |
| `gpu_scaling_fine` | 720 × 360 × 100; 1, 2, 4, 8, 16 GPUs |
| `gpu_nsight_scaling_default` | 360 × 180 × 50; 1, 2, 4, 8, 16 GPUs, profiled |
| `gpu_nsight_scaling_fine` | 720 × 360 × 100; 1, 2, 4, 8, 16 GPUs, profiled |
| `gpu_partition_fine` | 720 × 360 × 100; 16 × 1 × 1; 8 × 2 × 1; 4 × 4 × 1; 2 × 8 × 1 |
| `gpu_weak_scaling` | default / 1 GPU(s), partition 1 × 1 × 1; fine / 4 GPU(s), partition 2 × 2 × 1; super_fine / 16 GPU(s), partition 4 × 4 × 1 |

Default = 360 × 180 × 50; fine = 720 × 360 × 100;
super_fine = 1440 × 720 × 200. All grids use LatitudeLongitudeGrid.
Unspecified scaling partitions are balanced. No cases beyond the listed bounds
are appended. CPU benchmarks and ensembles are not selected.

Weak scaling doubles cells/GPU at each step: 3,240,000; 6,480,000; 12,960,000.
Use the documented linear cell-count reference, not constant-work weak efficiency.

The GPU count here is a study limit, independent of the larger configured
cluster capacity. Software/account settings are retained from the existing
configuration; review them before a future Slurm submission.

- [hydrostatic_free_surface_models baseline, Dagger and comparisons](../../results/hydrostatic_free_surface_models/rorqual/README.md)
- [non_hydrostatic_models baseline, Dagger and comparisons](../../results/non_hydrostatic_models/rorqual/README.md)

Each model/server results folder contains `baseline/`, `dagger/` and generated
comparison reports when matched measurements exist. Existing root-level historical
series retain their original provenance; they are not new-plan measurements.
