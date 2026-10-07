# Benchmark configuration

Series: cpu_resolution. Device: CPU; MPI ranks: 1; one thread/rank.
Grid: default, 360 × 180 × 50, LatitudeLongitudeGrid.
Partition: 1 × 1 × 1.
Local resolution: x 360–360, y 180–180, z 50.
Float64; WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=60 s; free-surface substeps=30 requested; extend_halos=False.
Two untimed steps, 5 windows of 10 steps. Profile=False.
