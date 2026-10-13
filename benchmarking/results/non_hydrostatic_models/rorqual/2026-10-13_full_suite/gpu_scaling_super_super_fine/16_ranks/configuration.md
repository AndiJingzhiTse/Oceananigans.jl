# Benchmark configuration

Series: gpu_scaling_super_super_fine. Device: GPU; MPI ranks: 16; one thread/rank.
Model: NonhydrostaticModel; surface: RigidLid.
Grid: super_super_fine, 2880 × 1440 × 200, LatitudeLongitudeGrid.
Partition: 4 × 4 × 1.
Local resolution: x 720–720, y 360–360, z 200.
Float64; momentum WENO7, tracers WENO7, ScalarDiffusivity, T/S, RungeKutta3.
Viscosity=0.001; diffusivity=1e-05 m²/s; pressure solver=ConjugateGradientPoissonSolver.
Δt=30.0 s; free-surface substeps=None requested; extend_halos=False.
Two untimed steps, 5 windows of 10 steps. Profile=False.
