# Benchmark configuration

Series: cpu_resolution. Device: CPU; MPI ranks: 1; one thread/rank.
Model: HydrostaticFreeSurfaceModel; surface: SplitExplicitFreeSurface.
Grid: 2880x1440x400, 2880 × 1440 × 400, LatitudeLongitudeGrid.
Partition: 1 × 1 × 1.
Local resolution: x 2880–2880, y 1440–1440, z 400.
Float64; momentum WENOVectorInvariantDefault, tracers WENO7, CATKE, T/S, SplitRungeKutta3.
Viscosity=None; diffusivity=None m²/s; pressure solver=None.
Pressure preconditioner=None; iteration cap=None; relative/absolute tolerances=None/None.
Δt=30.0 s; free-surface substeps=30 requested; extend_halos=False.
Two untimed steps, 5 windows of 10 steps. Profile=False.
