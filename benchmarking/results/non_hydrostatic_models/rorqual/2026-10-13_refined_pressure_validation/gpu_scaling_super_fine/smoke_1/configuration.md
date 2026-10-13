# Benchmark configuration

Series: gpu_scaling_super_fine. Device: GPU; MPI ranks: 1; one thread/rank.
Model: NonhydrostaticModel; surface: RigidLid.
Grid: validation_72x36x200, 72 × 36 × 200, LatitudeLongitudeGrid.
Partition: 1 × 1 × 1.
Local resolution: x 72–72, y 36–36, z 200.
Float64; momentum WENO7, tracers WENO7, ScalarDiffusivity, T/S, RungeKutta3.
Viscosity=0.001; diffusivity=1e-05 m²/s; pressure solver=ConjugateGradientPoissonSolver.
Pressure preconditioner=LocalFFTPreconditioner; iteration cap=5000; relative/absolute tolerances=1.4901161193847656e-08/1.4901161193847656e-08.
Δt=60 s; free-surface substeps=None requested; extend_halos=False.
Two untimed steps, 1 windows of 1 steps. Profile=False.
