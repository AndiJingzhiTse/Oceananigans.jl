# Benchmark configuration

Series: cpu_mpi_scaling_super_fine. Device: CPU; MPI ranks: 16; one thread/rank.
Model: NonhydrostaticModel; surface: RigidLid.
Grid: super_fine, 72 × 36 × 200, LatitudeLongitudeGrid.
Partition: 4 × 4 × 1.
Local resolution: x 18–18, y 9–9, z 200.
Float64; momentum WENO7, tracers WENO7, ScalarDiffusivity, T/S, RungeKutta3.
Viscosity=0.001; diffusivity=1e-05 m²/s; pressure solver=ConjugateGradientPoissonSolver.
Pressure preconditioner=ColumnwiseTridiagonalPreconditioner; iteration cap=5000; relative/absolute tolerances=1.4901161193847656e-08/1.4901161193847656e-08.
Δt=60 s; free-surface substeps=None requested; extend_halos=False.
Two untimed steps, 1 windows of 1 steps. Profile=False.
