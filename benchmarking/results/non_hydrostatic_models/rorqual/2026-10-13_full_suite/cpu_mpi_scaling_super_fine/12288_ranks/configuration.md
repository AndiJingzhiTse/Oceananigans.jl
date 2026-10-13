# Benchmark configuration

Series: cpu_mpi_scaling_super_fine. Device: CPU; MPI ranks: 12288; one thread/rank.
Model: NonhydrostaticModel; surface: RigidLid.
Grid: super_fine, 1440 × 720 × 200, LatitudeLongitudeGrid.
Partition: 128 × 96 × 1.
Local resolution: x 11–12, y 7–8, z 200.
Float64; momentum WENO7, tracers WENO7, ScalarDiffusivity, T/S, RungeKutta3.
Viscosity=0.001; diffusivity=1e-05 m²/s; pressure solver=ConjugateGradientPoissonSolver.
Δt=60 s; free-surface substeps=None requested; extend_halos=False.
Two untimed steps, 5 windows of 10 steps. Profile=False.
