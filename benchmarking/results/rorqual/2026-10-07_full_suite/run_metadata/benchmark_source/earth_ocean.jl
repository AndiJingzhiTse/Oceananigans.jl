#####
##### Earth ocean benchmark case
#####
##### Global ocean simulation using HydrostaticFreeSurfaceModel
##### with a TripolarGrid and realistic Earth bathymetry.
#####

using SeawaterPolynomials.TEOS10: TEOS10EquationOfState

"""
    earth_ocean(arch = CPU();
                float_type = Float32,
                Nx = 360, Ny = 180, Nz = 50,
                grid_type = "tripolar",
                momentum_advection = WENOVectorInvariant(),
                tracer_advection = WENO(order=7),
                zstar_coordinate = false,
                coriolis = HydrostaticSphericalCoriolis(),
                buoyancy = SeawaterBuoyancy(equation_of_state=TEOS10EquationOfState()),
                closure = CATKEVerticalDiffusivity(),
                timestepper = :SplitRungeKutta3,
                tracers = (:T, :S))

Create a `HydrostaticFreeSurfaceModel` for the Earth ocean benchmark case
with realistic Earth bathymetry.

# Arguments
- `arch`: Architecture to run on (`CPU()` or `GPU()`)

# Keyword Arguments
- `float_type`: Floating point precision (`Float32` or `Float64`)
- `Nx, Ny, Nz`: Grid resolution (longitude, latitude, vertical)
- `grid_type`: `"tripolar"` for a TripolarGrid, `"lat_lon"` for a plain LatitudeLongitudeGrid, or `"immersed_lat_lon"` for a LatitudeLongitudeGrid with bathymetry
- `zstar_coordinate`: zstar if `true`, z coordinate if `false`
- `momentum_advection`: Momentum advection scheme (default: `WENOVectorInvariant()`)
- `tracer_advection`: Tracer advection scheme (default: `WENO(order=7)`)
- `coriolis`: Coriolis force (default: `HydrostaticSphericalCoriolis()`; `nothing` disables it)
- `buoyancy`: Buoyancy formulation (default: seawater TEOS10; `nothing` disables it)
- `closure`: Turbulence closure (default: `CATKEVerticalDiffusivity()`)
- `timestepper`: Time stepping scheme (default: `:SplitRungeKutta3`)
- `tracers`: Tuple of tracer names (default: `(:T, :S)`)
- `extend_free_surface_halos`: Extend free-surface halos for substepping (default: `true`).
  Set to `false` to communicate at each substep when rank-local domains are small.
"""
function earth_ocean(arch = CPU();
                     float_type = Float32,
                     Nx = 360, Ny = 180, Nz = 50,
                     grid_type = "tripolar",
                     zstar_coordinate = false,
                     momentum_advection = WENOVectorInvariant(),
                     tracer_advection = WENO(order=7),
                     coriolis = HydrostaticSphericalCoriolis(),
                     buoyancy = SeawaterBuoyancy(equation_of_state=TEOS10EquationOfState()),
                     closure = CATKEVerticalDiffusivity(),
                     timestepper = :SplitRungeKutta3,
                     tracers = (:T, :S),
                     extend_free_surface_halos = true)

    grid_type in ("tripolar", "lat_lon", "immersed_lat_lon") ||
        error("Unknown grid_type: $grid_type. Use \"tripolar\", \"lat_lon\", or \"immersed_lat_lon\".")

    Oceananigans.defaults.FloatType = float_type

    depth = 5000  # meters
    z = ExponentialDiscretization(Nz, -depth, 0; scale=depth/4, mutable=zstar_coordinate)

    if grid_type == "tripolar"
        underlying_grid = TripolarGrid(arch;
            size = (Nx, Ny, Nz),
            halo = (7, 7, 7),
            z
        )
    else # lat_lon or immersed_lat_lon
        underlying_grid = LatitudeLongitudeGrid(arch;
            size = (Nx, Ny, Nz),
            halo = (7, 7, 7),
            longitude = (0, 360),
            latitude = (-80, 85),
            z
        )
    end

    if grid_type == "lat_lon"
        grid = underlying_grid
    else
        type_str = grid_type == "tripolar" ? "tripolar" : "latlon"
        filename = "bathymetry_$(type_str)_$(Nx)x$(Ny).jld2"
        filepath = joinpath(datadep"benchmark_bathymetry", filename)
        bottom_height = jldopen(filepath) do file
            bh = file["bottom_height"]
            ndims(bh) == 3 ? dropdims(bh, dims=3) : bh
        end

        grid = ImmersedBoundaryGrid(underlying_grid, PartialCellBottom(bottom_height);
            active_cells_map = true
        )
    end

    free_surface = SplitExplicitFreeSurface(; substeps=30, extend_halos=extend_free_surface_halos)

    model = HydrostaticFreeSurfaceModel(grid;
        momentum_advection,
        tracer_advection,
        coriolis,
        buoyancy,
        closure,
        free_surface,
        tracers,
        timestepper
    )

    # Initial conditions: baroclinic wave excitation
    Tᵢ(λ, φ, z) = 30 * (1 - tanh((abs(φ) - 45) / 8)) / 2 + rand()
    Sᵢ(λ, φ, z) = 28 - 5e-3 * z + rand()

    ic = Dict{Symbol,Any}()
    :T in tracers && (ic[:T] = Tᵢ)
    :S in tracers && (ic[:S] = Sᵢ)
    # Extra tracers beyond T/S get zero (default)

    set!(model; ic...)

    return model
end
