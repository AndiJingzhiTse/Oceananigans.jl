# Benchmark configuration

Series: cpu_mpi_scaling_super_fine. Device: CPU; MPI ranks: 16; one thread/rank.
Model: NonhydrostaticModel; surface: RigidLid.
Grid: smoke_200_levels, 72 × 36 × 200, LatitudeLongitudeGrid.
Partition: 4 × 4 × 1.
Local resolution: x 18–18, y 9–9, z 200.
Float64; momentum WENO7, tracers WENO7, ScalarDiffusivity, T/S, RungeKutta3.
Viscosity=0.001; diffusivity=1e-05 m²/s; pressure solver=ConjugateGradientPoissonSolver.
Δt=60 s; free-surface substeps=None requested; extend_halos=False.
Two untimed steps, 5 windows of 10 steps. Profile=False.
