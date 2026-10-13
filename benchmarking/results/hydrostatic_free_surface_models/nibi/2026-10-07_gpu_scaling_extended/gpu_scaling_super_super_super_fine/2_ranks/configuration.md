# Benchmark configuration

Series: gpu_scaling_super_super_super_fine. Device: GPU; MPI ranks: 2; one thread/rank.
Grid: super_super_super_fine, 5760 × 2880 × 200, LatitudeLongitudeGrid.
Partition: 2 × 1 × 1.
Local resolution: x 2880–2880, y 2880–2880, z 200.
Float64; WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=15.0 s; free-surface substeps=30 requested; extend_halos=True.
Two untimed steps, 5 windows of 100 steps. Profile=False.
