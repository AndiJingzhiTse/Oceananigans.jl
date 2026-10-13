# Extended Nibi GPU benchmarking — October 7, 2026

Reference: [DRAC scaling guide](../../../../../Oceananigans-DRAC/docs/drac.md).
All grids use LatitudeLongitudeGrid without bathymetry, Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S and SplitRungeKutta3.
One MPI rank/GPU; 30 requested free-surface substeps, extended halos; two untimed steps.
Strong/weak scaling uses five 100-step windows following DRAC. Partition comparisons use five ten-step windows.

| Series | Resolution / work | Submitted GPU counts | Partition / Δt |
|---|---|---|---|
| Strong super_fine | 1440×720×200 | 1, 2, 4, 8, 16, 32 | x-only; 60 s |
| Strong super_super_fine | 2880×1440×200 | 4, 8, 16, 32, 64 | x-only; 30 s |
| Strong super_super_super_fine | 5760×2880×200 | 16, 32, 64, 128 | x-only; 15 s |
| Weak scaling | 207,360,000 interior cells/GPU; starts 1440×720×200 | 1, 2, 4, 8, 16, 32, 64, 128 | Balanced expansion; 60, 30, 30, 15, 15, 7.5, 7.5, 3.75 s |
| Partition comparison | 1440×720×200 | 2, 4, 8, 16 | All horizontal factor pairs; 60 s |

Eight-GPU layouts: 8×1×1, 4×2×1, 2×4×1, 1×8×1.
Sixteen-GPU layouts: 16×1×1, 8×2×1, 4×4×1, 2×8×1, 1×16×1.
All layouts at one GPU count share one allocation and run sequentially with fresh MPI/Julia processes.

[DRAC-style strong/weak table](scaling.md) and [full report/plots](plot.md) distinguish measured results from pending allocations and limits.
Strong efficiency uses the smallest validated count for that grid. Weak efficiency is T₁/Tₙ with fixed interior cells per GPU.
Device-used GiB/GPU is measured after the timing windows, includes context/cache overhead, and is not a peak allocation.

Larger grids omit smaller GPU counts following DRAC’s H100 memory-fit baselines; these are estimates, not observed failures.
For x-only splitting, the next strong counts 64 / 128 / 256 leave only 22–23 local x cells, below the 23-cell extended-halo requirement.
The next weak count, 256 GPUs, exceeds the configured 232 full-H100 cluster capacity.

Accepted GPU allocations: **27**, covering **37 cases**.
After-any report finalizer: **23439432**.
Login-host monitor log: `/scratch/anditse/nibi_gpu_scaling_extended_watch.log`.

## Job IDs

| Series | GPU count → job |
|---|---|
| gpu_partition_super_fine | 2 → 23439404, 4 → 23439405, 8 → 23439406, 16 → 23439407 |
| gpu_scaling_super_fine | 1 → 23439408, 2 → 23439409, 4 → 23439410, 8 → 23439411, 16 → 23439412, 32 → 23439413 |
| gpu_scaling_super_super_fine | 4 → 23439414, 8 → 23439415, 16 → 23439416, 32 → 23439417, 64 → 23439418 |
| gpu_scaling_super_super_super_fine | 16 → 23439419, 32 → 23439420, 64 → 23439421, 128 → 23439422 |
| gpu_weak_scaling_super_fine | 1 → 23439423, 2 → 23439424, 4 → 23439426, 8 → 23439427, 16 → 23439428, 32 → 23439429, 64 → 23439430, 128 → 23439431 |

## Validation

Twenty suite tests passed, including all new partition layouts, constant weak work per GPU, reduced time steps, larger-grid baselines, throughput and strong/weak efficiency tables.
Julia worker syntax and CUDA MemoryInfo API fields were verified. Legacy partition-report regression tests passed.
The reference environment rename is supported by the new DRAC profile. A compatibility env/nibi.sh was restored in the adjacent DRAC checkout (commit 120322b) so already submitted historical jobs retain their environment/depot.
No new performance values are claimed until all ranks validate.
