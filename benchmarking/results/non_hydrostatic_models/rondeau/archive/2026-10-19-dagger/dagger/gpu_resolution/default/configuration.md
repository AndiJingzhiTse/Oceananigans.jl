# Benchmark configuration

Series: gpu_resolution. Device: GPU; MPI ranks: 1; one thread/rank.
Model: NonhydrostaticModel; surface: RigidLid.
Execution: dagger; Dagger wraps one timing window in one local CPU task.
Grid: default, 360 × 180 × 50, LatitudeLongitudeGrid.
Partition: 1 × 1 × 1.
Local resolution: x 360–360, y 180–180, z 50.
Float64; momentum WENO7, tracers WENO7, ScalarDiffusivity, T/S, RungeKutta3.
Viscosity=0.001; diffusivity=1e-05 m²/s; pressure solver=ConjugateGradientPoissonSolver.
Pressure preconditioner=LocalFFTPreconditioner; iteration cap=5000; relative/absolute tolerances=1.4901161193847656e-08/1.4901161193847656e-08.
Δt=60 s; free-surface substeps=None requested; extend_halos=False.
Two untimed steps, 5 windows of 10 steps. Profile=False.
