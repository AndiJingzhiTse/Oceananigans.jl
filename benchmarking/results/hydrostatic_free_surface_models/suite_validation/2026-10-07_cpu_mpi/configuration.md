# Benchmark configuration

Series: cpu_mpi_scaling_super_fine. Device: CPU; MPI ranks: 2; one thread/rank.
Grid: smoke_validation, 72 × 36 × 8, LatitudeLongitudeGrid.
Partition: 2 × 1 × 1.
Local resolution: x 36–36, y 36–36, z 8.
Float64; WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=60 s; free-surface substeps=30 requested; extend_halos=False.
Two untimed steps, 5 windows of 10 steps. Profile=False.
