# Benchmark configuration

Series: gpu_scaling_fine. Device: GPU; MPI ranks: 2; one thread/rank.
Model: NonhydrostaticModel; surface: RigidLid.
Execution: baseline; Dagger wraps one timing window in one local CPU task.
Grid: fine, 720 × 360 × 100, LatitudeLongitudeGrid.
Partition: 2 × 1 × 1.
Local resolution: x 360–360, y 360–360, z 100.
Float64; momentum WENO7, tracers WENO7, ScalarDiffusivity, T/S, RungeKutta3.
Viscosity=0.001; diffusivity=1e-05 m²/s; pressure solver=ConjugateGradientPoissonSolver.
Pressure preconditioner=LocalFFTPreconditioner; iteration cap=5000; relative/absolute tolerances=1.4901161193847656e-08/1.4901161193847656e-08.
Δt=60 s; free-surface substeps=None requested; extend_halos=False.
Two untimed steps, 5 windows of 10 steps. Profile=False.
