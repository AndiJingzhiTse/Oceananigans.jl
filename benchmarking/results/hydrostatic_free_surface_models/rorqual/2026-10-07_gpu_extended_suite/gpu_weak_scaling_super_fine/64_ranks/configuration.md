# Benchmark configuration

Series: gpu_weak_scaling_super_fine. Device: GPU; MPI ranks: 64; one thread/rank.
Grid: weak_64_ranks, 11520 × 5760 × 200, LatitudeLongitudeGrid.
Partition: 8 × 8 × 1.
Local resolution: x 1440–1440, y 720–720, z 200.
Float64; WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=7.5 s; free-surface substeps=30 requested; extend_halos=True.
Two untimed steps, 5 windows of 10 steps. Profile=False.
