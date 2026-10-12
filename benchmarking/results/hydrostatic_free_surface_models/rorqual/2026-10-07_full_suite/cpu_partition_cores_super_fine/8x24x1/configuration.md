# Benchmark configuration

Series: cpu_partition_cores_super_fine. Device: CPU; MPI ranks: 192; one thread/rank.
Grid: super_fine, 1440 × 720 × 200, LatitudeLongitudeGrid.
Partition: 8 × 24 × 1.
Local resolution: x 180–180, y 30–30, z 200.
Float64; WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=60 s; free-surface substeps=30 requested; extend_halos=False.
Two untimed steps, 5 windows of 10 steps. Profile=False.
