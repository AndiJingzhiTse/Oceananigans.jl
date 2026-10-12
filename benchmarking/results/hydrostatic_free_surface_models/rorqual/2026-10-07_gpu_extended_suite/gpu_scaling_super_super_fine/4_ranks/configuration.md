# Benchmark configuration

Series: gpu_scaling_super_super_fine. Device: GPU; MPI ranks: 4; one thread/rank.
Grid: super_super_fine, 2880 × 1440 × 200, LatitudeLongitudeGrid.
Partition: 2 × 2 × 1.
Local resolution: x 1440–1440, y 720–720, z 200.
Float64; WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=30.0 s; free-surface substeps=30 requested; extend_halos=True.
Two untimed steps, 5 windows of 10 steps. Profile=False.
