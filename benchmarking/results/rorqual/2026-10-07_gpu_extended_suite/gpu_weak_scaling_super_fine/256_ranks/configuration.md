# Benchmark configuration

Series: gpu_weak_scaling_super_fine. Device: GPU; MPI ranks: 256; one thread/rank.
Grid: weak_256_ranks, 23040 × 11520 × 200, LatitudeLongitudeGrid.
Partition: 16 × 16 × 1.
Local resolution: x 1440–1440, y 720–720, z 200.
Float64; WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=3.75 s; free-surface substeps=30 requested; extend_halos=True.
Two untimed steps, 5 windows of 10 steps. Profile=False.
