# Nsight collects the timed region, after initialization and two untimed steps.
using OceananigansBenchmarks, Oceananigans, CUDA, NCDatasets, MPI, JSON
include(joinpath(ENV["OCEANANIGANS_DRAC_ROOT"], "src", "drac_mpi.jl"))
drac_mpi_init()
include(joinpath(@__DIR__, "..", "..", "run_benchmarks.jl"))
using Oceananigans.Fields: interior

case_dir = ENV["NSIGHT_CASE_DIR"]
configuration = JSON.parse(read(joinpath(case_dir, "configuration.json"), String))
comm = MPI.COMM_WORLD
rank = MPI.Comm_rank(comm)
ranks = MPI.Comm_size(comm)
ranks == configuration["gpus"] || error("Unexpected MPI rank count")
layout = Dict("rank" => rank, "hostname" => gethostname(), "gpu_uuid" => string(CUDA.uuid(CUDA.device())),
              "gpu_name" => CUDA.name(CUDA.device()), "threads" => Threads.nthreads())
layouts = MPI.gather(layout, comm; root=0)
distinct = MPI.bcast(rank == 0 ? length(unique(l["gpu_uuid"] for l in layouts)) == ranks : false, comm; root=0)
distinct || error("MPI ranks share GPUs")
if rank == 0
    open(joinpath(case_dir, "gpu_layout.json"), "w") do io
        JSON.json(io, layouts; pretty=true)
    end
end
send_buffer = CUDA.fill(Float64(rank), 1024)
receive_buffer = CUDA.zeros(Float64, 1024)
source = mod(rank - 1, ranks)
MPI.Sendrecv!(send_buffer, receive_buffer, comm; dest=mod(rank + 1, ranks), source)
MPI.Allreduce(all(Array(receive_buffer) .== source) ? 1 : 0, MPI.MIN, comm) == 1 || error("CUDA-aware MPI ring failed")
rank == 0 && println("PASS: $ranks distinct GPUs and CUDA-aware MPI")

arch = Distributed(GPU(); partition=Partition(configuration["partition"]...))
Nx, Ny, Nz = Int.(configuration["global_resolution"])
model = earth_ocean(arch; Nx, Ny, Nz, float_type=Float64, grid_type="lat_lon",
                    momentum_advection=make_momentum_advection("WENOVectorInvariantDefault", Float64),
                    tracer_advection=make_tracer_advection("WENO7", Float64), closure=make_closure("CATKE", Float64),
                    timestepper=:SplitRungeKutta3, tracers=(:T, :S), extend_free_surface_halos=true)
size(model.grid) == Tuple(configuration["local_resolution"]) || error("Unexpected local grid")
# Compile both stepping and the timing/result helper outside the capture.
# One warmup step plus one untimed preflight window = two untimed steps.
benchmark_time_stepping(model; Δt=60, warmup_steps=1, time_steps=1, samples=1, verbose=false)
CUDA.synchronize()
MPI.Barrier(comm)
rank == 0 && println("Starting Nsight capture: ", JSON.json(configuration))
CUDA.CUDACore.cuProfilerStart()
result = try
    benchmark_time_stepping(model; Δt=60, warmup_steps=0, time_steps=10, samples=5,
                            name="EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr",
                            verbose=false)
finally
    CUDA.synchronize()
    CUDA.CUDACore.cuProfilerStop()
end
finite_state = all(all(isfinite, interior(tracer)) for tracer in values(model.tracers)) &&
               all(isfinite, interior(model.free_surface.displacement))
MPI.Allreduce(finite_state ? 1 : 0, MPI.MIN, comm) == 1 || error("Nonfinite model state")
entry = JSON.parse(JSON.json(result))
entry["rank"] = rank
entry["configuration"] = configuration
entry["finite_state"] = finite_state
entries = MPI.gather(entry, comm; root=0)
if rank == 0
    open(joinpath(case_dir, "results.json"), "w") do io
        JSON.json(io, entries; pretty=true)
    end
    generate_markdown_report(joinpath(case_dir, "results.md"), entries)
    open(joinpath(case_dir, "results.md"), "a") do io
        println(io)
        print(io, read(joinpath(case_dir, "configuration.md"), String))
    end
    println("Completed profiled benchmark and finite-state validation")
end
MPI.Barrier(comm)
