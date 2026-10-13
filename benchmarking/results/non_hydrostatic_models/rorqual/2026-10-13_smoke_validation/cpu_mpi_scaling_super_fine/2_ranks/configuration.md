# Benchmark configuration

Series: cpu_mpi_scaling_super_fine. Device: CPU; MPI ranks: 2; one thread/rank.
Model: NonhydrostaticModel; surface: RigidLid.
Grid: smoke, 72 × 36 × 8, LatitudeLongitudeGrid.
Partition: 2 × 1 × 1.
Local resolution: x 36–36, y 36–36, z 8.
Float64; momentum WENO7, tracers WENO7, ScalarDiffusivity, T/S, RungeKutta3.
Viscosity=0.001; diffusivity=1e-05 m²/s; pressure solver=ConjugateGradientPoissonSolver.
Δt=60 s; free-surface substeps=None requested; extend_halos=False.
Two untimed steps, 5 windows of 10 steps. Profile=False.
