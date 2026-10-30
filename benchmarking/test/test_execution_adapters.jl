using Test

module DirectAdapterTest
include(joinpath(@__DIR__, "../src/suite/execution/baseline/adapter.jl"))
end

function increment_window!(counter, Δt, steps, is_gpu, device)
    @test !is_gpu
    @test isnothing(device)
    counter[] += steps
    return nothing
end

@testset "Shared execution adapter contract" begin
    context = (is_gpu=false, device=nothing, options=Dict{String, Any}())
    counter = Ref(0)
    DirectAdapterTest.BenchmarkAdapter.execute_window!(increment_window!, counter, 1, 3, context)
    @test counter[] == 3
    @test isempty(DirectAdapterTest.BenchmarkAdapter.metadata()["package_versions"])
    @test all(package.name != "Dagger" for package in keys(Base.loaded_modules))
end

module DaggerAdapterTest
include(joinpath(@__DIR__, "../src/suite/execution/dagger/adapter.jl"))
end

@testset "Dagger uses the same execution interface" begin
    context = (is_gpu=false, device=nothing, options=Dict{String, Any}())
    counter = Ref(0)
    DaggerAdapterTest.BenchmarkAdapter.execute_window!(increment_window!, counter, 1, 3, context)
    @test counter[] == 3
    @test haskey(DaggerAdapterTest.BenchmarkAdapter.metadata()["package_versions"], "Dagger")
    DaggerAdapterTest.BenchmarkAdapter.execute_window!(increment_window!, counter, 1, 2, context)
    @test counter[] == 5
end
