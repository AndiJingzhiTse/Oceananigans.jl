# Benchmark configuration

Series: gpu_nsight_scaling_super_fine. Device: GPU; MPI ranks: 4; one thread/rank.
Model: HydrostaticFreeSurfaceModel; surface: SplitExplicitFreeSurface.
Grid: super_fine, 1440 × 720 × 200, LatitudeLongitudeGrid.
Partition: 2 × 2 × 1.
Local resolution: x 720–720, y 360–360, z 200.
Float64; momentum WENOVectorInvariantDefault, tracers WENO7, CATKE, T/S, SplitRungeKutta3.
Viscosity=None; diffusivity=None m²/s; pressure solver=None.
Pressure preconditioner=None; iteration cap=None; relative/absolute tolerances=None/None.
Δt=60 s; free-surface substeps=30 requested; extend_halos=True.
Two untimed steps, 5 windows of 10 steps. Profile=True.

Alternative measured efficiency baseline: 2 GPUs; smaller baseline exhausted VRAM.
