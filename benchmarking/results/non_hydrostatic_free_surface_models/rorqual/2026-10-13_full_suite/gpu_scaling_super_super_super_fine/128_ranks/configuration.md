# Benchmark configuration

Series: gpu_scaling_super_super_super_fine. Device: GPU; MPI ranks: 128; one thread/rank.
Model: NonhydrostaticModel; surface: RigidLid.
Grid: super_super_super_fine, 5760 × 2880 × 200, LatitudeLongitudeGrid.
Partition: 16 × 8 × 1.
Local resolution: x 360–360, y 360–360, z 200.
Float64; momentum WENO7, tracers WENO7, ScalarDiffusivity, T/S, RungeKutta3.
Viscosity=0.001; diffusivity=1e-05 m²/s; pressure solver=ConjugateGradientPoissonSolver.
Δt=15.0 s; free-surface substeps=None requested; extend_halos=False.
Two untimed steps, 5 windows of 10 steps. Profile=False.
