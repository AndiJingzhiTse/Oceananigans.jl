# Benchmark configuration

Series: gpu_resolution. Device: GPU; MPI ranks: 1; one thread/rank.
Model: HydrostaticFreeSurfaceModel; surface: SplitExplicitFreeSurface.
Grid: default, 360 × 180 × 50, LatitudeLongitudeGrid.
Partition: 1 × 1 × 1.
Local resolution: x 360–360, y 180–180, z 50.
Float64; momentum WENOVectorInvariantDefault, tracers WENO7, CATKE, T/S, SplitRungeKutta3.
Viscosity=None; diffusivity=None m²/s; pressure solver=None.
Pressure preconditioner=None; iteration cap=None; relative/absolute tolerances=None/None.
Δt=60 s; free-surface substeps=30 requested; extend_halos=True.
Two untimed steps, 5 windows of 10 steps. Profile=False.
