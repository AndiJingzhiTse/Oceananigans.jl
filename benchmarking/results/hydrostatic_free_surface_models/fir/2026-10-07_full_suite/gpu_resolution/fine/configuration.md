# Benchmark configuration

Series: gpu_resolution. Device: GPU; MPI ranks: 1; one thread/rank.
Grid: fine, 720 × 360 × 100, LatitudeLongitudeGrid.
Partition: 1 × 1 × 1.
Local resolution: x 720–720, y 360–360, z 100.
Float64; WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=60 s; free-surface substeps=30 requested; extend_halos=True.
Two untimed steps, 5 windows of 10 steps. Profile=False.
