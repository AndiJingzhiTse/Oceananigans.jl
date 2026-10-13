# Benchmark configuration

Series: cpu_partition_cores_super_fine. Device: CPU; MPI ranks: 192; one thread/rank.
Model: NonhydrostaticModel; surface: RigidLid.
Grid: super_fine, 1440 × 720 × 200, LatitudeLongitudeGrid.
Partition: 96 × 2 × 1.
Local resolution: x 15–15, y 360–360, z 200.
Float64; momentum WENO7, tracers WENO7, ScalarDiffusivity, T/S, RungeKutta3.
Viscosity=0.001; diffusivity=1e-05 m²/s; pressure solver=ConjugateGradientPoissonSolver.
Δt=60 s; free-surface substeps=None requested; extend_halos=False.
Two untimed steps, 5 windows of 10 steps. Profile=False.
