module ChunkedFFTPressureSolvers

using CUDA: CUDA
using Dagger: Dagger
using LinearAlgebra: mul!
using KernelAbstractions: @kernel, @index
using Oceananigans: GPU, Periodic
using Oceananigans.Fields: indices
using Oceananigans.Grids: XYZRegularRG, topology
using Oceananigans.Solvers: FFTBasedPoissonSolver, copy_real_component!
using Oceananigans.Utils: launch!
using FFTW: FFTW

import Oceananigans.Architectures: architecture
import Oceananigans.Solvers: solve!
import Oceananigans.Models.NonhydrostaticModels: compute_source_term!
import ..PressureSolverBenchmark: make_solver, solver_storage, backend_metadata

export ChunkedFFTBasedPoissonSolver, SerialChunks, AsyncChunks, DaggerChunks

struct SerialChunks end
struct AsyncChunks end
struct DaggerChunks end

struct FFTChunk{R, A, F, B, S}
    ranges :: R
    buffer :: A
    forward_plan :: F
    backward_plan :: B
    stream :: S
end

struct ChunkedFFTBasedPoissonSolver{S, T, E}
    native :: S
    stages :: T
    execution :: E
end

function build_stage(storage, dimension, chunks)
    split_dimension = dimension == 1 ? 2 : 1
    length = size(storage, split_dimension)
    chunks <= length || throw(ArgumentError("Chunk count exceeds transverse dimension"))
    return map(1:chunks) do index
        first = fld((index - 1) * length, chunks) + 1
        last = fld(index * length, chunks)
        ranges = ntuple(d -> d == split_dimension ? (first:last) : axes(storage, d), 3)
        buffer = similar(storage, Base.length.(ranges))
        stream = CUDA.CuStream()
        forward_plan, backward_plan = CUDA.stream!(stream) do
            forward = CUDA.CUFFT.plan_fft!(buffer, (dimension,))
            backward = CUDA.CUFFT.plan_ifft!(buffer, (dimension,))
            return forward, backward
        end
        return FFTChunk(ranges, buffer, forward_plan, backward_plan, stream)
    end
end

"""
    ChunkedFFTBasedPoissonSolver(grid; execution=SerialChunks(), chunks=4)

Construct an experimental single-GPU periodic Cartesian pressure solver.
Each stage transforms independent, disjoint batches of full-length pencils.
The serial and Dagger variants use identical plans, copies and workspaces.
Dependent stages wait for all CUDA work from the previous stage to complete.
"""
function ChunkedFFTBasedPoissonSolver(grid; execution=SerialChunks(), chunks=4)
    grid isa XYZRegularRG || throw(ArgumentError("Only regular RectilinearGrid is supported"))
    architecture(grid) isa GPU || throw(ArgumentError("Only a single local GPU is supported"))
    topology(grid) == (Periodic, Periodic, Periodic) ||
        throw(ArgumentError("Only fully periodic grids are supported"))
    execution isa Union{SerialChunks, AsyncChunks, DaggerChunks} || throw(ArgumentError("Unknown execution strategy"))
    chunks > 0 || throw(ArgumentError("Chunk count must be positive"))
    native = FFTBasedPoissonSolver(grid, FFTW.ESTIMATE)
    stages = ntuple(dimension -> build_stage(native.storage, dimension, chunks), 3)
    return ChunkedFFTBasedPoissonSolver(native, stages, execution)
end

architecture(solver::ChunkedFFTBasedPoissonSolver) = architecture(solver.native)

function execute_chunk!(storage, chunk, backward)
    CUDA.stream!(chunk.stream) do
        region = view(storage, chunk.ranges...)
        copyto!(chunk.buffer, region)
        plan = backward ? chunk.backward_plan : chunk.forward_plan
        mul!(chunk.buffer, plan, chunk.buffer)
        copyto!(region, chunk.buffer)
    end
    CUDA.synchronize(chunk.stream)
    return nothing
end

function execute_stage!(storage, stage, backward, ::SerialChunks)
    for chunk in stage
        execute_chunk!(storage, chunk, backward)
    end
    return nothing
end

function execute_stage!(storage, stage, backward, ::DaggerChunks)
    tasks = map(stage) do chunk
        # Chunk writes are disjoint; resources stay on their owning process.
        return Dagger.@spawn scope=Dagger.scope(worker=1, thread=1) execute_chunk!(storage, chunk, backward)
    end
    fetch.(tasks)
    return nothing
end

function execute_stage!(storage, stage, backward, ::AsyncChunks)
    @sync for chunk in stage
        @async execute_chunk!(storage, chunk, backward)
    end
    return nothing
end

@kernel function _invert_spectrum!(storage, eigenvalues)
    i, j, k = @index(Global, NTuple)
    @inbounds begin
        λ = eigenvalues[1][i, 1, 1] + eigenvalues[2][1, j, 1] + eigenvalues[3][1, 1, k]
        nonzero = (i != 1) | (j != 1) | (k != 1)
        denominator = ifelse(nonzero, λ, one(λ))
        storage[i, j, k] = ifelse(nonzero, -storage[i, j, k] / denominator, zero(eltype(storage)))
    end
end

function solve!(pressure, solver::ChunkedFFTBasedPoissonSolver)
    native = solver.native
    storage = native.storage
    CUDA.synchronize()
    for stage in solver.stages
        execute_stage!(storage, stage, false, solver.execution)
    end
    launch!(architecture(solver), native.grid, :xyz, _invert_spectrum!, storage, native.eigenvalues)
    CUDA.synchronize()
    for stage in reverse(solver.stages)
        execute_stage!(storage, stage, true, solver.execution)
    end
    launch!(architecture(solver), native.grid, :xyz, copy_real_component!, pressure, storage, indices(pressure))
    return pressure
end

function compute_source_term!(solver::ChunkedFFTBasedPoissonSolver, ::Nothing, velocities, timestep)
    compute_source_term!(solver.native, nothing, velocities, timestep)
    return nothing
end

function make_solver(grid, ::Val{:serial_chunks}, configuration)
    return ChunkedFFTBasedPoissonSolver(grid; execution=SerialChunks(),
                                       chunks=get(configuration, "chunks_per_stage", 4))
end

function make_solver(grid, ::Val{:dagger_chunks}, configuration)
    return ChunkedFFTBasedPoissonSolver(grid; execution=DaggerChunks(),
                                       chunks=get(configuration, "chunks_per_stage", 4))
end

function make_solver(grid, ::Val{:async_chunks}, configuration)
    return ChunkedFFTBasedPoissonSolver(grid; execution=AsyncChunks(),
                                       chunks=get(configuration, "chunks_per_stage", 4))
end

solver_storage(solver::ChunkedFFTBasedPoissonSolver) = solver.native.storage

function backend_metadata(solver::ChunkedFFTBasedPoissonSolver)
    return (; dagger_version=string(pkgversion(Dagger)), chunks_per_stage=length(first(solver.stages)),
            synchronization="complete each stage before dependent transforms",
            scope="owning process, computation thread 1, explicit CUDA streams")
end

end
