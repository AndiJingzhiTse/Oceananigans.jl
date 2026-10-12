# Benchmark configuration

Series: gpu_weak_scaling_super_fine. Device: GPU; MPI ranks: 1024; one thread/rank.
Grid: weak_1024_ranks, 46080 × 23040 × 200, LatitudeLongitudeGrid.
Partition: 32 × 32 × 1.
Local resolution: x 1440–1440, y 720–720, z 200.
Float64; WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=1.875 s; free-surface substeps=30 requested; extend_halos=True.
Two untimed steps, 5 windows of 10 steps. Profile=False.
