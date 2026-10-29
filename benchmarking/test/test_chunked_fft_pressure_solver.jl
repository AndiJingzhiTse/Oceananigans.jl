using Test
using Random: MersenneTwister, randn
using CUDA: CUDA
using Oceananigans
using Oceananigans.Architectures: on_architecture
using Oceananigans.Fields: interior
using Oceananigans.Solvers: FFTBasedPoissonSolver
using FFTW: FFTW

include(joinpath(@__DIR__, "../src/pressure_solver_benchmark.jl"))
include(joinpath(@__DIR__, "../src/chunked_fft_pressure_solver.jl"))
using .PressureSolverBenchmark
using .ChunkedFFTPressureSolvers

@testset "Chunked FFT inverse and model trajectory" begin
    for float_type in (Float32, Float64), resolution in ((16, 12, 8), (17, 19, 23))
        grid = RectilinearGrid(GPU(), float_type; size=resolution, extent=(2π, 2π, 2π),
                               topology=(Periodic, Periodic, Periodic))
        native = FFTBasedPoissonSolver(grid, FFTW.ESTIMATE)
        reference, pressure = CenterField(grid), CenterField(grid)
        source = randn(MersenneTwister(1234), float_type, resolution)
        source .-= sum(source) / length(source)
        device_source = on_architecture(GPU(), source)
        solve_rhs!(reference, native, device_source)
        expected = Array(interior(reference))
        for execution in (SerialChunks(), AsyncChunks(), DaggerChunks()), chunks in (1, 4)
            solver = ChunkedFFTBasedPoissonSolver(grid; execution, chunks)
            for scale in (one(float_type), float_type(2), zero(float_type))
                solve_rhs!(pressure, solver, scale .* device_source)
                actual = Array(interior(pressure))
                @test all(isfinite, actual)
                @test isapprox(actual, scale .* expected; rtol=100eps(float_type), atol=100eps(float_type))
            end
        end
    end

    grid = RectilinearGrid(GPU(), Float64; size=(16, 12, 8), extent=(2π, 2π, 2π),
                           topology=(Periodic, Periodic, Periodic))
    @test_throws ArgumentError ChunkedFFTBasedPoissonSolver(grid; chunks=0)
    @test_throws ArgumentError ChunkedFFTBasedPoissonSolver(grid; chunks=32)
    bounded = RectilinearGrid(GPU(); size=(16, 12, 8), extent=(2π, 2π, 2π))
    @test_throws ArgumentError ChunkedFFTBasedPoissonSolver(bounded)
    stretched = RectilinearGrid(GPU(); size=(16, 12, 8), x=(0, 2π), y=(0, 2π),
                                z=collect(range(0, 1; length=9)) .^ 2,
                                topology=(Periodic, Periodic, Periodic))
    @test_throws ArgumentError ChunkedFFTBasedPoissonSolver(stretched)

    models = map((:native, :serial_chunks, :async_chunks, :dagger_chunks)) do backend
        solver = make_solver(grid, Val(backend), Dict("chunks_per_stage" => 4))
        model = NonhydrostaticModel(grid; pressure_solver=solver, timestepper=:RungeKutta3,
                                   advection=Centered(order=2), buoyancy=nothing,
                                   closure=ScalarDiffusivity(ν=0.01), tracers=())
        set!(model, u=(x, y, z) -> sin(x) * cos(y) * cos(z),
                    v=(x, y, z) -> -cos(x) * sin(y) * cos(z), w=0)
        for _ in 1:3
            time_step!(model, 0.001)
        end
        CUDA.synchronize()
        return model
    end
    for model in models[2:end], name in (:u, :v, :w)
        @test Array(interior(getproperty(model.velocities, name))) ≈
              Array(interior(getproperty(models[1].velocities, name)))
    end
end
