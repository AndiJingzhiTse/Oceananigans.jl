# Benchmark configuration

Series: cpu_mpi_scaling_super_fine. Device: CPU; MPI ranks: 12288; one thread/rank.
Grid: super_fine, 1440 × 720 × 200, LatitudeLongitudeGrid.
Partition: 128 × 96 × 1.
Local resolution: x 11–12, y 7–8, z 200.
Float64; WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=60 s; free-surface substeps=30 requested; extend_halos=False.
Two untimed steps, 5 windows of 10 steps. Profile=False.
