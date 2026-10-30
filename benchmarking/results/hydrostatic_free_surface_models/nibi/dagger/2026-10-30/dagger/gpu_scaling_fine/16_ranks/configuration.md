# Benchmark configuration

Series: gpu_scaling_fine. Device: GPU; MPI ranks: 16; one thread/rank.
Model: HydrostaticFreeSurfaceModel; surface: SplitExplicitFreeSurface.
Execution: dagger; Dagger wraps one timing window in one local CPU task.
Grid: fine, 720 × 360 × 100, LatitudeLongitudeGrid.
Partition: 4 × 4 × 1.
Local resolution: x 180–180, y 90–90, z 100.
Float64; momentum WENOVectorInvariantDefault, tracers WENO7, CATKE, T/S, SplitRungeKutta3.
Viscosity=None; diffusivity=None m²/s; pressure solver=None.
Pressure preconditioner=None; iteration cap=None; relative/absolute tolerances=None/None.
Δt=60 s; free-surface substeps=30 requested; extend_halos=True.
Two untimed steps, 5 windows of 10 steps. Profile=False.
