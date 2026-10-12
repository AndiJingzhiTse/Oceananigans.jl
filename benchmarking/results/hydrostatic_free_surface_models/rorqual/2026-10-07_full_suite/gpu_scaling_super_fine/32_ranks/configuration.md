# Benchmark configuration

Series: gpu_scaling_super_fine. Device: GPU; MPI ranks: 32; one thread/rank.
Grid: super_fine, 1440 × 720 × 200, LatitudeLongitudeGrid.
Partition: 8 × 4 × 1.
Local resolution: x 180–180, y 180–180, z 200.
Float64; WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=60 s; free-surface substeps=30 requested; extend_halos=True.
Two untimed steps, 5 windows of 10 steps. Profile=False.
