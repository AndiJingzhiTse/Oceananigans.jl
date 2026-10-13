# Benchmark configuration

Series: gpu_weak_scaling_super_fine. Device: GPU; MPI ranks: 128; one thread/rank.
Grid: weak_128_gpus, 23040 × 5760 × 200, LatitudeLongitudeGrid.
Partition: 16 × 8 × 1.
Local resolution: x 1440–1440, y 720–720, z 200.
Float64; WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=3.75 s; free-surface substeps=30 requested; extend_halos=True.
Two untimed steps, 5 windows of 100 steps. Profile=False.
