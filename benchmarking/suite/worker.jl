# Shared model, validation and timing path for all standard benchmark series.
using OceananigansBenchmarks, Oceananigans, CUDA, NCDatasets, MPI, JSON
using Oceananigans.DistributedComputations: Distributed, Partition, Sizes
using Oceananigans.Fields: interior
using Oceananigans.Architectures: architecture
using Statistics: median
using Sockets: gethostname

# Load packages first, then repair OPAL_PREFIX if the server provides a hook.
# Other MPI installations can leave BENCHMARK_MPI_INIT unset.
mpi_hook = get(ENV, "BENCHMARK_MPI_INIT", "")
if !isempty(mpi_hook)
    include(mpi_hook)
    drac_mpi_init()
else
    MPI.Initialized() || MPI.Init()
end
case_dir = only(ARGS)
config = JSON.parsefile(joinpath(case_dir, "configuration.json"))
comm = MPI.COMM_WORLD
rank = MPI.Comm_rank(comm)
ranks = MPI.Comm_size(comm)
ranks == config["ranks"] || error("Unexpected MPI rank count")
Threads.nthreads() == 1 || error("Expected one Julia thread per rank")
is_gpu = config["device"] == "GPU"

function affinity()
    if Sys.islinux()
        return match(r"(?m)^Cpus_allowed_list:\s*(.+)$", read("/proc/self/status", String)).captures[1]
    end
    return "unavailable"
end

allowed = affinity()
if !is_gpu && Sys.islinux()
    # An allocation may expose both SMT siblings of one physical core.
    # Pin the computation thread to the first assigned logical CPU.
    first_cpu = parse(Int, first(split(first(split(allowed, ',')), '-')))
    mask = zeros(UInt8, max(128, cld(first_cpu + 1, 8)))
    mask[first_cpu ÷ 8 + 1] = UInt8(1) << (first_cpu % 8)
    ccall(:sched_setaffinity, Cint, (Cint, Csize_t, Ptr{UInt8}), 0, length(mask), mask) == 0 || error("Cannot pin computation thread")
    allowed = affinity()
end
physical_core = nothing
if !is_gpu
    occursin(r"^\d+$", allowed) || error("CPU computation thread must be pinned to one physical core")
    topology = "/sys/devices/system/cpu/cpu$allowed/topology"
    physical_core = strip(read(joinpath(topology, "physical_package_id"), String)) * ":" * strip(read(joinpath(topology, "core_id"), String))
end
# All local ranks may see a common GPU list, or Slurm may expose one GPU/task.
if is_gpu
    shared = MPI.Comm_split_type(comm, MPI.COMM_TYPE_SHARED, rank)
    local_rank = MPI.Comm_rank(shared)
    devices = collect(CUDA.devices())
    isempty(devices) && error("No assigned CUDA device")
    CUDA.device!(length(devices) == 1 ? devices[1] : devices[local_rank + 1])
    MPI.free(shared)
end
layout = Dict("rank" => rank, "hostname" => gethostname(), "affinity" => allowed,
              "threads" => 1, "physical_core" => physical_core, "gpu_uuid" => is_gpu ? string(CUDA.uuid(CUDA.device())) : nothing,
              "gpu_name" => is_gpu ? CUDA.name(CUDA.device()) : nothing)
layouts = MPI.gather(layout, comm; root=0)
valid_layout = rank == 0 ? length(unique((l["hostname"], is_gpu ? l["gpu_uuid"] : l["physical_core"]) for l in layouts)) == ranks : false
MPI.bcast(valid_layout, comm; root=0) || error("Ranks share a GPU or CPU computation core")
if rank == 0
    open(joinpath(case_dir, "layout.json"), "w") do io
        JSON.json(io, layouts; pretty=true)
    end
end
send_buffer = is_gpu ? CUDA.fill(Float64(rank), 1024) : fill(Float64(rank), 1024)
receive_buffer = is_gpu ? CUDA.zeros(Float64, 1024) : zeros(Float64, 1024)
source = mod(rank - 1, ranks)
MPI.Sendrecv!(send_buffer, receive_buffer, comm; dest=mod(rank + 1, ranks), source)
MPI.Allreduce(all(Array(receive_buffer) .== source) ? 1 : 0, MPI.MIN, comm) == 1 || error("MPI ring validation failed")
arch = Distributed(is_gpu ? GPU() : CPU();
                   partition=Partition(Sizes(config["x_sizes"]...), Sizes(config["y_sizes"]...), 1))
Nx, Ny, Nz = Int.(config["global_resolution"])
model = earth_ocean(arch; Nx, Ny, Nz, float_type=Float64, grid_type="lat_lon",
                    momentum_advection=WENOVectorInvariant(Float64), tracer_advection=WENO(Float64; order=7),
                    timestepper=:SplitRungeKutta3, tracers=(:T, :S),
                    extend_free_surface_halos=config["extend_free_surface_halos"])
expected = (config["x_sizes"][arch.local_index[1]], config["y_sizes"][arch.local_index[2]], Nz)
size(model.grid) == expected || error("Unexpected local resolution")
retained_substeps = length(model.free_surface.substepping.averaging_weights)

function synchronize_model(arch, comm, is_gpu)
    is_gpu && CUDA.synchronize()
    MPI.Barrier(comm)
    return nothing
end

function timing_windows!(model, config, comm, is_gpu)
    # Compile this helper before profiling; the preflight supplies one untimed step.
    durations = Float64[]
    for sample in 1:config["samples"]
        synchronize_model(architecture(model.grid), comm, is_gpu)
        start = time_ns()
        OceananigansBenchmarks.many_time_steps!(model, config["dt"], config["time_steps"])
        synchronize_model(architecture(model.grid), comm, is_gpu)
        push!(durations, (time_ns() - start) / 1e9)
    end
    return durations
end

# One warmup + one unprofiled helper window = two untimed steps.
OceananigansBenchmarks.many_time_steps!(model, config["dt"], config["warmup_steps"] - 1)
preflight = copy(config)
preflight["samples"], preflight["time_steps"] = 1, 1
timing_windows!(model, preflight, comm, is_gpu)
synchronize_model(arch, comm, is_gpu)
config["profile"] && CUDA.CUDACore.cuProfilerStart()
windows = try
    timing_windows!(model, config, comm, is_gpu)
finally
    is_gpu && CUDA.synchronize()
    config["profile"] && CUDA.CUDACore.cuProfilerStop()
end
finite_state = all(all(isfinite, interior(t)) for t in values(model.tracers)) &&
               all(isfinite, interior(model.free_surface.displacement))
MPI.Allreduce(finite_state ? 1 : 0, MPI.MIN, comm) == 1 || error("Nonfinite model fields")
metadata = JSON.parse(JSON.json(OceananigansBenchmarks.BenchmarkMetadata(arch)))
steps = config["time_steps"]
entry = Dict("rank" => rank, "grid_size" => collect(size(model.grid)), "float_type" => "Float64",
             "configuration" => config, "metadata" => metadata, "finite_state" => finite_state,
             "retained_free_surface_substeps" => retained_substeps,
             "window_seconds" => windows, "time_per_step_seconds" => minimum(windows) / steps,
             "time_per_step_median_seconds" => median(windows) / steps,
             "time_per_step_max_seconds" => maximum(windows) / steps)
entries = MPI.gather(entry, comm; root=0)
if rank == 0
    open(joinpath(case_dir, "results.json"), "w") do io
        JSON.json(io, entries; pretty=true)
    end
    println("PASS: MPI ring, distinct resources, finite fields and all $ranks rank results")
end
MPI.Barrier(comm)
