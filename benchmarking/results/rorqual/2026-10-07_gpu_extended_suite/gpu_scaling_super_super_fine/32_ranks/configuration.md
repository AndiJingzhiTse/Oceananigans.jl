# Benchmark configuration

Series: gpu_scaling_super_super_fine. Device: GPU; MPI ranks: 32; one thread/rank.
Grid: super_super_fine, 2880 × 1440 × 200, LatitudeLongitudeGrid.
Partition: 8 × 4 × 1.
Local resolution: x 360–360, y 360–360, z 200.
Float64; WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=30.0 s; free-surface substeps=30 requested; extend_halos=True.
Two untimed steps, 5 windows of 10 steps. Profile=False.
