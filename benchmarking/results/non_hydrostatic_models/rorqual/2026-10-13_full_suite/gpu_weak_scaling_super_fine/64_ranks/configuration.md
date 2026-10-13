# Benchmark configuration

Series: gpu_weak_scaling_super_fine. Device: GPU; MPI ranks: 64; one thread/rank.
Model: NonhydrostaticModel; surface: RigidLid.
Grid: weak_64_ranks, 11520 × 5760 × 200, LatitudeLongitudeGrid.
Partition: 8 × 8 × 1.
Local resolution: x 1440–1440, y 720–720, z 200.
Float64; momentum WENO7, tracers WENO7, ScalarDiffusivity, T/S, RungeKutta3.
Viscosity=0.001; diffusivity=1e-05 m²/s; pressure solver=ConjugateGradientPoissonSolver.
Δt=7.5 s; free-surface substeps=None requested; extend_halos=False.
Two untimed steps, 5 windows of 10 steps. Profile=False.
