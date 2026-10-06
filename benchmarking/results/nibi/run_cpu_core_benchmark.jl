# Single-threaded MPI ranks, or explicitly pinned threads for a thread sweep.
using OceananigansBenchmarks, Oceananigans, NCDatasets, MPI, JSON
include(joinpath(ENV["OCEANANIGANS_DRAC_ROOT"], "src", "drac_mpi.jl"))
drac_mpi_init()
comm = MPI.COMM_WORLD
rank = MPI.Comm_rank(comm)
ranks = MPI.Comm_size(comm)
expected_threads = parse(Int, ENV["SLURM_CPUS_PER_TASK"])
Threads.nthreads() == expected_threads || error("Unexpected Julia thread count")
status = read("/proc/self/status", String)
allowed = match(r"(?m)^Cpus_allowed_list:\s*(.+)$", status).captures[1]
cpus = Int[]
for item in split(allowed, ',')
    edges = parse.(Int, split(item, '-'))
    append!(cpus, first(edges):last(edges))
end
length(cpus) == expected_threads || error("Slurm CPU affinity does not match requested cores per rank")
thread_affinities = Vector{String}(undef, expected_threads)
Threads.@threads :static for i in 1:expected_threads
    cpu = cpus[Threads.threadid()]
    mask = zeros(UInt8, max(128, cld(maximum(cpus) + 1, 8)))
    mask[cpu ÷ 8 + 1] = UInt8(1) << (cpu % 8)
    result = ccall(:sched_setaffinity, Cint, (Cint, Csize_t, Ptr{UInt8}), 0, length(mask), mask)
    result == 0 || error("Could not pin Julia thread to CPU $cpu")
    tid = ccall(:gettid, Cint, ())
    thread_status = read("/proc/self/task/$tid/status", String)
    thread_affinities[i] = match(r"(?m)^Cpus_allowed_list:\s*(.+)$", thread_status).captures[1]
end
layout = Dict("rank" => rank, "hostname" => gethostname(), "threads" => Threads.nthreads(),
              "cpus_per_task" => expected_threads, "allocated_affinity" => allowed,
              "thread_affinities" => thread_affinities)
layouts = MPI.gather(layout, comm; root=0)
if rank == 0
    open(joinpath(ENV["CPU_CASE_DIR"], "cpu_layout.json"), "w") do io
        JSON.json(io, layouts; pretty=true)
    end
end
send_buffer = fill(Float64(rank), 1024)
receive_buffer = zeros(Float64, 1024)
source = mod(rank - 1, ranks)
MPI.Sendrecv!(send_buffer, receive_buffer, comm; dest=mod(rank + 1, ranks), source)
MPI.Allreduce(all(receive_buffer .== source) ? 1 : 0, MPI.MIN, comm) == 1 || error("CPU MPI ring check failed")
println("rank $rank on $(gethostname()): $expected_threads pinned threads; allocated CPUs $allowed")
MPI.Barrier(comm)
rank == 0 && println("PASS: CPU MPI ring and explicitly pinned Julia threads")
include(joinpath(@__DIR__, "..", "..", "run_benchmarks.jl"))
using Oceananigans.DistributedComputations: Sizes
using Oceananigans.Fields: interior
configuration = JSON.parse(read(joinpath(ENV["CPU_CASE_DIR"], "configuration.json"), String))
ranks == configuration["ranks"] || error("Unexpected MPI rank count")
partition = Partition(Sizes(configuration["x_sizes"]...), Sizes(configuration["y_sizes"]...), 1)
arch = Distributed(CPU(); partition)
model = earth_ocean(arch; Nx=1440, Ny=720, Nz=200, grid_type="lat_lon", float_type=Float64,
                    momentum_advection=make_momentum_advection("WENOVectorInvariantDefault", Float64),
                    tracer_advection=make_tracer_advection("WENO7", Float64), closure=make_closure("CATKE", Float64),
                    timestepper=:SplitRungeKutta3, tracers=(:T, :S), extend_free_surface_halos=false)
local_index = arch.local_index
expected_size = (configuration["x_sizes"][local_index[1]], configuration["y_sizes"][local_index[2]], 200)
size(model.grid) == expected_size || error("Unexpected rank-local model grid")
MPI.Barrier(comm)
rank == 0 && println("CONFIGURATION: ", JSON.json(configuration))
result = benchmark_time_stepping(model; Δt=60, warmup_steps=2, time_steps=10, samples=5,
                                 name="EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr",
                                 verbose=rank == 0)
finite_state = all(all(isfinite, interior(tracer)) for tracer in values(model.tracers)) &&
               all(isfinite, interior(model.free_surface.displacement))
MPI.Allreduce(finite_state ? 1 : 0, MPI.MIN, comm) == 1 || error("Nonfinite tracer or free-surface state after benchmark")
entry = JSON.parse(JSON.json(result))
entry["rank"] = rank
entry["configuration"] = configuration
entry["finite_state"] = finite_state
entries = MPI.gather(entry, comm; root=0)
if rank == 0
    output = joinpath(ENV["CPU_CASE_DIR"], "results.json")
    open(output, "w") do io
        JSON.json(io, entries; pretty=true)
    end
    generate_markdown_report(joinpath(ENV["CPU_CASE_DIR"], "results.md"), entries)
    open(joinpath(ENV["CPU_CASE_DIR"], "results.md"), "a") do io
        println(io)
        print(io, read(joinpath(ENV["CPU_CASE_DIR"], "configuration.md"), String))
    end
    println("Completed benchmark; all $ranks rank results saved to $output")
end
MPI.Barrier(comm)
