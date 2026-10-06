# Tiny CPU check: the new opt-in free-surface setting preserves serial results.
using Test, OceananigansBenchmarks, Oceananigans
using Oceananigans.Architectures: CPU
using Oceananigans.Fields: interior
using Oceananigans.Grids: halo_size

models = [earth_ocean(CPU(); Nx=16, Ny=12, Nz=8, grid_type="lat_lon", float_type=Float64,
                      extend_free_surface_halos=extend) for extend in (true, false)]
for model in models
    set!(model, T=(λ, φ, z) -> 15 + 0.001z, S=35)
    many_time_steps!(model, 1, 2)
    @test all(isfinite, interior(model.tracers.T))
    @test halo_size(model.free_surface.displacement.grid)[1:2] == (7, 7)
end
@test interior(models[1].tracers.T) ≈ interior(models[2].tracers.T)
@test interior(models[1].free_surface.displacement) ≈ interior(models[2].free_surface.displacement)
println("PASS: free-surface halo setting preserves tiny serial model results")
