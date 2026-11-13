# Benchmark configuration

Series: gpu_weak_scaling_512_x. Device: GPU; MPI ranks: 1; one thread/rank.
Model: HydrostaticFreeSurfaceModel; surface: SplitExplicitFreeSurface.
Execution: baseline; Adapter direct; timing contract oceananigans/timestep_window/v1.
Grid: 512x512x512, 512 × 512 × 512, RectilinearGrid.
Partition: 1 × 1 × 1.
Local resolution: x 512–512, y 512–512, z 512.
Domain extent (m): [512000, 512000, 5120]; cell spacing (m): [1000, 1000, 10]; topology: ['Periodic', 'Periodic', 'Bounded'].
Float64; momentum WENO5, tracer advection WENO5, closure=None, tracers=['b'], SplitRungeKutta3.
Buoyancy=BuoyancyTracer; Coriolis=None; initial condition=b=1e-5*z+1e-6*cospi(x/64000)*cospi(y/64000)*sinpi(z/5120); u=0.1; v=0.05; w=0.
Viscosity=None; diffusivity=None m²/s; pressure solver=None.
Pressure preconditioner=None; iteration cap=None; relative/absolute tolerances=None/None.
Δt=10 s; free-surface substeps=30 requested; extend_halos=True.
Initial-condition seed=None plus MPI rank when set.
Two untimed steps, 5 windows of 10 steps. Profile=False.
