# Benchmark configuration

Series: gpu_weak_scaling_super_fine. Device: GPU; MPI ranks: 32; one thread/rank.
Grid: weak_32_gpus, 11520 × 2880 × 200, LatitudeLongitudeGrid.
Partition: 8 × 4 × 1.
Local resolution: x 1440–1440, y 720–720, z 200.
Float64; WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=7.5 s; free-surface substeps=30 requested; extend_halos=True.
Two untimed steps, 5 windows of 100 steps. Profile=False.
