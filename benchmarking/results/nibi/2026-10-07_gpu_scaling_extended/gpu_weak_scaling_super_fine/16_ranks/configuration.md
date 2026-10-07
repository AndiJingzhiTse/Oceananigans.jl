# Benchmark configuration

Series: gpu_weak_scaling_super_fine. Device: GPU; MPI ranks: 16; one thread/rank.
Grid: super_super_super_fine, 5760 × 2880 × 200, LatitudeLongitudeGrid.
Partition: 4 × 4 × 1.
Local resolution: x 1440–1440, y 720–720, z 200.
Float64; WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=15.0 s; free-surface substeps=30 requested; extend_halos=True.
Two untimed steps, 5 windows of 100 steps. Profile=False.
