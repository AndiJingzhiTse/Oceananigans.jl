# Benchmark configuration

Series: gpu_scaling_super_fine. Device: GPU; MPI ranks: 2; one thread/rank.
Model: HydrostaticFreeSurfaceModel; surface: SplitExplicitFreeSurface.
Execution: baseline; Dagger wraps one timing window in one local CPU task.
Grid: super_fine, 1440 × 720 × 200, LatitudeLongitudeGrid.
Partition: 2 × 1 × 1.
Local resolution: x 720–720, y 720–720, z 200.
Float64; momentum WENOVectorInvariantDefault, tracers WENO7, CATKE, T/S, SplitRungeKutta3.
Viscosity=None; diffusivity=None m²/s; pressure solver=None.
Pressure preconditioner=None; iteration cap=None; relative/absolute tolerances=None/None.
Δt=60 s; free-surface substeps=30 requested; extend_halos=True.
Two untimed steps, 5 windows of 10 steps. Profile=False.
