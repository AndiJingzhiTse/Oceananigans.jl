# Benchmark configuration

Series: cpu_resolution. Device: CPU; MPI ranks: 1; one thread/rank.
Model: HydrostaticFreeSurfaceModel; surface: SplitExplicitFreeSurface.
Grid: fine, 720 × 360 × 100, LatitudeLongitudeGrid.
Partition: 1 × 1 × 1.
Local resolution: x 720–720, y 360–360, z 100.
Float64; momentum WENOVectorInvariantDefault, tracers WENO7, CATKE, T/S, SplitRungeKutta3.
Viscosity=None; diffusivity=None m²/s; pressure solver=None.
Pressure preconditioner=None; iteration cap=None; relative/absolute tolerances=None/None.
Δt=60 s; free-surface substeps=30 requested; extend_halos=False.
Two untimed steps, 5 windows of 10 steps. Profile=False.
