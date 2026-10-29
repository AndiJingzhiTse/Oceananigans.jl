using Test
using TOML: TOML

include(joinpath(@__DIR__, "../src/pressure_solver_benchmark.jl"))
using .PressureSolverBenchmark

configuration_path = joinpath(@__DIR__, "../pressure_solver/smoke.toml")
configuration = TOML.parsefile(configuration_path)

@testset "Pressure study configuration" begin
    @test isnothing(validate_configuration(configuration))
    for (key, value) in (("resolution", [7, 8, 8]), ("partition", [0, 1, 1]),
                         ("partition", [1, 1, 2]), ("partition", [3, 1, 1]),
                         ("float_type", "Float16"), ("steps_per_window", 0),
                         ("windows", 0), ("timestep", 0), ("viscosity", -1))
        @test_throws ErrorException validate_configuration(merge(configuration, Dict(key => value)))
    end
end

@testset "Native GPU pressure and timestep acceptance" begin
    mktempdir() do output
        result = run_case(configuration_path, output)
        @test result.pressure_validation.passed
        @test result.model_validation.passed
        @test all(>(0), result.pressure_timing.maximum_rank_seconds)
        @test length(result.timestep_timing.maximum_rank_seconds) == configuration["windows"]
        @test isfile(joinpath(output, "rank_0.json"))
    end
end
