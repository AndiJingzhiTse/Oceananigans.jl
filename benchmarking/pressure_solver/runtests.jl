module NativePressureSolverTests
include(joinpath(@__DIR__, "../test/test_pressure_solver.jl"))
end

module ChunkedPressureSolverTests
include(joinpath(@__DIR__, "../test/test_chunked_fft_pressure_solver.jl"))
end
