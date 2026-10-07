# Benchmark configuration

Series: gpu_scaling_super_super_fine. Device: GPU; MPI ranks: 8; one thread/rank.
Grid: super_super_fine, 2880 × 1440 × 200, LatitudeLongitudeGrid.
Partition: 8 × 1 × 1.
Local resolution: x 360–360, y 1440–1440, z 200.
Float64; WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=30.0 s; free-surface substeps=30 requested; extend_halos=True.
Two untimed steps, 5 windows of 100 steps. Profile=False.
