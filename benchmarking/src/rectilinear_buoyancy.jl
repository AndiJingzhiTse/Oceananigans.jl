# Matched Cartesian workload for hydrostatic/nonhydrostatic weak scaling.
function rectilinear_buoyancy(arch, config)
    Nx, Ny, Nz = Int.(config["global_resolution"])
    Lx, Ly, Lz = config["domain_extent_m"]
    grid = RectilinearGrid(arch, Float64;
        size=(Nx, Ny, Nz), halo=(3, 3, 3),
        topology=(Periodic, Periodic, Bounded), x=(0, Lx), y=(0, Ly), z=(-Lz, 0))
    advection = WENO(Float64; order=5)
    common = (; momentum_advection=advection, tracer_advection=advection,
                buoyancy=BuoyancyTracer(), tracers=(:b,), closure=nothing, coriolis=nothing)
    model = if config["model_type"] == "HydrostaticFreeSurfaceModel"
        free_surface = SplitExplicitFreeSurface(;
            substeps=config["free_surface_substeps"], extend_halos=config["extend_free_surface_halos"])
        HydrostaticFreeSurfaceModel(grid; common..., free_surface, timestepper=:SplitRungeKutta3)
    elseif config["model_type"] == "NonhydrostaticModel"
        NonhydrostaticModel(grid; common..., timestepper=:RungeKutta3)
    else
        error("Unknown rectilinear benchmark model")
    end
    # Stable stratification plus a smooth perturbation repeating across x slabs.
    bᵢ(x, y, z) = 1e-5 * z + 1e-6 * cospi(x / 64000) * cospi(y / 64000) * sinpi(z / 5120)
    set!(model; b=bᵢ, u=1//10, v=1//20)
    return model
end
