# Shared model, validation and timing path for all standard benchmark series.
using OceananigansBenchmarks, Oceananigans, CUDA, NCDatasets, MPI, JSON
using Oceananigans.DistributedComputations: Distributed, Partition, Sizes
using Oceananigans.Fields: interior
using Oceananigans.Architectures: architecture
using Oceananigans.TurbulenceClosures: ThreeDimensionalFormulation
using Oceananigans.Solvers: ConjugateGradientPoissonSolver, ConjugateGradientSolver,
                            DiagonallyDominantPreconditioner, ColumnwiseTridiagonalPreconditioner,
                            BatchedTridiagonalSolver, ColumnwiseTridiagonalLowerDiagonal,
                            ColumnwiseTridiagonalUpperDiagonal, Ac,
                            FourierTridiagonalPoissonSolver, InhomogeneousFormulation,
                            compute_preconditioner_rhs!, compute_symmetric_laplacian!, FFTW
using Oceananigans.DistributedComputations: child_architecture
using Oceananigans.Architectures: on_architecture
using Oceananigans.Grids: ZDirection
using Oceananigans.BoundaryConditions: fill_halo_regions!
import Oceananigans.Solvers: get_coefficient, precondition!, solve!
import Oceananigans.Models.NonhydrostaticModels: solve_for_pressure!
using Random: seed!
using LinearAlgebra: dot
using Statistics: median
using Sockets: gethostname

# Exact vertical blocks of the full Poisson matrix: retain its horizontal
# diagonal instead of imposing the columnwise solver's fixed 1% vertical shift.
struct VerticalLineDiagonal end
@inline get_coefficient(i, j, k, grid, ::VerticalLineDiagonal, p, ::ZDirection, args...) = Ac(i, j, k, grid)
struct VerticalLinePreconditioner{S}
    solver::S
end
function VerticalLinePreconditioner(grid)
    solver = BatchedTridiagonalSolver(grid;
        lower_diagonal=ColumnwiseTridiagonalLowerDiagonal(), diagonal=VerticalLineDiagonal(),
        upper_diagonal=ColumnwiseTridiagonalUpperDiagonal(), tridiagonal_direction=ZDirection())
    return VerticalLinePreconditioner{typeof(solver)}(solver)
end
function precondition!(p, preconditioner::VerticalLinePreconditioner, r, args...)
    fill_halo_regions!(r)
    solve!(p, preconditioner.solver, r)
    return p
end

# A symmetric local approximate inverse. Only the preconditioner uses a
# Cartesian metric; CG still solves the original latitude-longitude operator.
struct LocalFFTPreconditioner{S, D}
    solver::S
    details::D
end
function LocalFFTPreconditioner(grid, config, arch)
    nx, ny, nz = size(grid)
    iy = arch.local_index[2]
    Nx, Ny, Nz = config["global_resolution"]
    latitude = -80 + 165 * (sum(Int[x for x in config["y_sizes"][1:iy-1]]) + ny / 2) / Ny
    Lx = grid.radius * deg2rad(360) * cosd(latitude) * nx / Nx
    Ly = grid.radius * deg2rad(165) * ny / Ny
    aux = RectilinearGrid(child_architecture(arch), Float64;
        size=(nx, ny, nz), halo=(7, 7, 7),
        topology=(config["partition"][1] == 1 ? Periodic : Bounded, Bounded, Bounded),
        x=(0, Lx), y=(0, Ly), z=ExponentialDiscretization(Nz, -5000, 0; scale=1250))
    screening = (config["partition"][1] > 1 ? 1 / Lx^2 : 0) +
                (config["partition"][2] > 1 ? 1 / Ly^2 : 0)
    screened = screening > 0
    # The inhomogeneous formulation retains the local constant mode, which a
    # screened block needs to communicate pressure differences between ranks.
    formulation = screened ? InhomogeneousFormulation(ZDirection()) : nothing
    Oceananigans.Solvers.FFTW_NUM_THREADS[] = 1
    solver = FourierTridiagonalPoissonSolver(aux, FFTW.ESTIMATE; tridiagonal_formulation=formulation)
    if screened
        dz = on_architecture(child_architecture(arch), diff(Array(znodes(aux, Face()))))
        solver.batched_tridiagonal_solver.b .-= reshape(dz, 1, 1, nz) .* screening
    end
    details = Dict("auxiliary_grid_type" => "RectilinearGrid", "local_resolution" => [nx, ny, nz],
        "extent_m" => [Lx, Ly, 5000], "latitude_degrees" => latitude,
        "screening_inverse_m2" => screening,
        "x_topology" => config["partition"][1] == 1 ? "Periodic" : "Bounded",
        "fftw_threads" => 1, "planner" => "ESTIMATE")
    return LocalFFTPreconditioner{typeof(solver), typeof(details)}(solver, details)
end
function precondition!(p, preconditioner::LocalFFTPreconditioner, r, args...)
    return precondition!(p, preconditioner.solver, r, args...)
end

function validate_local_fft!(native, case_dir, rank)
    cg = native.conjugate_gradient_solver
    a, b, Ma, Mb = cg.residual, cg.search_direction, cg.linear_operator_product, cg.preconditioner_product
    set!(a, (λ, φ, z) -> sinpi(λ / 180) * cosd(φ) * (1 + z / 5000))
    set!(b, (λ, φ, z) -> sinpi(λ / 180) * cosd(φ) * (1 + z / 5000) +
                           cospi(λ / 180) * sind(φ) * (2 + z / 5000))
    precondition!(Ma, cg.preconditioner, a)
    precondition!(Mb, cg.preconditioner, b)
    aMb, bMa, energy = dot(a, Mb), dot(b, Ma), dot(a, Ma)
    relative_error = abs(aMb - bMa) / max(abs(aMb), abs(bMa), abs(energy), eps(Float64))
    # Near-orthogonal probes need an absolute scale from the quadratic form.
    symmetric = abs(aMb - bMa) <= 1e-8 * max(abs(aMb), abs(bMa), abs(energy))
    valid = all(isfinite, (aMb, bMa, energy)) && symmetric && energy < 0
    record = Dict("passed" => valid, "aMb" => aMb, "bMa" => bMa,
                  "quadratic_form" => energy, "symmetry_relative_error" => relative_error)
    rank == 0 && open(joinpath(case_dir, "preconditioner_validation.json"), "w") do io
        JSON.json(io, record; pretty=true)
    end
    valid || error("Local FFT preconditioner failed symmetry/definiteness checks")
    return record
end

# Track norm evaluations already performed by CG, without extra MPI reductions.
mutable struct BenchmarkResidualNorm{N, F}
    native::N
    scratch::F
    calls::Int
    initial::Float64
    last::Float64
    started::UInt64
    diagnostics::Bool
    rank::Int
end

function (metric::BenchmarkResidualNorm)(residual)
    value = if isnothing(metric.scratch)
        metric.native(residual)
    else
        # VolumeInverseNorm scales its input in place and scales it back.
        # A copy prevents those roundoff changes from entering the CG recurrence.
        copyto!(parent(metric.scratch), parent(residual))
        metric.native(metric.scratch)
    end
    metric.calls += 1
    isfinite(value) || error("Nonfinite pressure residual after $(max(0, metric.calls - 2)) iterations")
    metric.calls == 1 && (metric.initial = value)
    metric.last = value
    iteration = max(0, metric.calls - 2)
    if metric.diagnostics && metric.rank == 0 && (metric.calls == 1 || iteration > 0 && iteration % 200 == 0)
        println("PRESSURE_PROGRESS iteration=$iteration residual=$value elapsed_seconds=$((time_ns() - metric.started) / 1e9)")
        flush(stdout)
    end
    return value
end

mutable struct CheckedPressureSolver{S, N}
    native::S
    metric::N
    records::Vector{Dict{String, Any}}
end

function checked_pressure_solver(native, config, rank)
    cg = native.conjugate_gradient_solver
    scratch = get(config, "pressure_preserve_residual", false) ? similar(native.right_hand_side) : nothing
    metric = BenchmarkResidualNorm(cg.residual_norm, scratch, 0, 0.0, 0.0, time_ns(),
                                   get(config, "pressure_diagnostics", false), rank)
    tracked = ConjugateGradientSolver(cg.architecture, cg.grid, cg.linear_operation!,
        cg.reltol, cg.abstol, cg.maxiter, cg.iteration, cg.ρⁱ⁻¹,
        cg.linear_operator_product, cg.search_direction, cg.residual, cg.preconditioner,
        cg.preconditioner_product, cg.enforce_gauge_condition!, metric)
    native = ConjugateGradientPoissonSolver(native.grid, native.right_hand_side, tracked)
    return CheckedPressureSolver(native, metric, Dict{String, Any}[])
end

function solve_for_pressure!(pressure, solver::CheckedPressureSolver, free_surface, velocities, Δt)
    metric = solver.metric
    metric.calls = 0
    metric.started = time_ns()
    solve_for_pressure!(pressure, solver.native, free_surface, velocities, Δt)
    cg = solver.native.conjugate_gradient_solver
    # The iteration cap short-circuits CG's final norm evaluation.
    residual = cg.iteration >= cg.maxiter ? metric.native(cg.residual) : metric.last
    tolerance = max(cg.reltol * metric.initial, cg.abstol)
    converged = isfinite(residual) && residual <= tolerance
    record = Dict{String, Any}("solve" => length(solver.records) + 1, "iterations" => cg.iteration,
        "initial_residual" => metric.initial, "final_residual" => residual,
        "tolerance" => tolerance, "converged" => converged,
        "projection_dt" => Float64(Δt),
        "seconds" => (time_ns() - metric.started) / 1e9)
    push!(solver.records, record)
    if metric.diagnostics && metric.rank == 0
        println("PRESSURE_SOLVE ", JSON.json(record))
        flush(stdout)
    end
    if !converged
        open(joinpath(case_dir, "rank_$(metric.rank)", "pressure_failure.json"), "w") do io
            JSON.json(io, record; pretty=true)
        end
        error("Pressure solve failed convergence after $(cg.iteration) iterations: residual=$residual, tolerance=$tolerance")
    end
    return pressure
end

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
execution_mode = get(config, "execution_mode", "baseline")
execution_mode in ("baseline", "dagger") || error("Unknown execution mode: $execution_mode")

function synchronized_window!(model, Δt, steps, is_gpu, device)
    # CUDA device and stream state are task-local. Both variants bind the
    # assigned device and complete the current stream inside the same helper.
    is_gpu && CUDA.device!(device)
    OceananigansBenchmarks.many_time_steps!(model, Δt, steps)
    is_gpu && CUDA.synchronize()
    return nothing
end

# MPI communicators and mutable models must stay on this process. Each rank
# has exactly one Julia computation thread; no Distributed workers are added.
# Define this only for Dagger runs so baseline does not load its scheduler.
if execution_mode == "dagger"
    @eval using Dagger
    @eval function execute_window!(model, Δt, steps, is_gpu, device, ::Val{:dagger})
        task = Dagger.@spawn scope=Dagger.scope(worker=1, thread=1) synchronized_window!(model, Δt, steps, is_gpu, device)
        fetch(task)
        return nothing
    end
end

function execute_window!(model, Δt, steps, is_gpu, device, ::Val{:baseline})
    synchronized_window!(model, Δt, steps, is_gpu, device)
    return nothing
end

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
model_type = get(config, "model_type", "HydrostaticFreeSurfaceModel")
is_hydrostatic = model_type == "HydrostaticFreeSurfaceModel"
preconditioner_validation = nothing
if rank == 0
    println("MODEL_BUILD_START mode=$execution_mode resolution=$(config["global_resolution"]) partition=$(config["partition"])")
    flush(stdout)
end
model = if is_hydrostatic
    earth_ocean(arch; Nx, Ny, Nz, float_type=Float64, grid_type="lat_lon",
                    momentum_advection=WENOVectorInvariant(Float64), tracer_advection=WENO(Float64; order=7),
                    timestepper=:SplitRungeKutta3, tracers=(:T, :S),
                    extend_free_surface_halos=config["extend_free_surface_halos"])
elseif model_type == "NonhydrostaticModel"
    grid = LatitudeLongitudeGrid(arch, Float64; size=(Nx, Ny, Nz), halo=(7, 7, 7),
                                 longitude=(0, 360), latitude=(-80, 85),
                                 z=ExponentialDiscretization(Nz, -5000, 0; scale=1250))
    closure = ScalarDiffusivity(ExplicitTimeDiscretization(), ThreeDimensionalFormulation(), Float64;
                               ν=config["viscosity"], κ=config["diffusivity"])
    # Every rank needs the same stopping bound, including uneven Sizes partitions.
    preconditioner_name = get(config, "pressure_preconditioner", "DiagonallyDominantPreconditioner")
    preconditioner = if preconditioner_name == "ColumnwiseTridiagonalPreconditioner"
        ColumnwiseTridiagonalPreconditioner(grid)
    elseif preconditioner_name == "VerticalLinePreconditioner"
        VerticalLinePreconditioner(grid)
    elseif preconditioner_name == "LocalFFTPreconditioner"
        LocalFFTPreconditioner(grid, config, arch)
    elseif preconditioner_name == "DiagonallyDominantPreconditioner"
        DiagonallyDominantPreconditioner()
    else
        error("Unknown pressure preconditioner: $preconditioner_name")
    end
    native_solver = ConjugateGradientPoissonSolver(grid; preconditioner,
        maxiter=get(config, "pressure_max_iterations", 5000),
        reltol=get(config, "pressure_reltol", sqrt(eps(Float64))),
        abstol=get(config, "pressure_abstol", sqrt(eps(Float64))))
    if preconditioner isa LocalFFTPreconditioner
        preconditioner_validation = validate_local_fft!(native_solver, case_dir, rank)
    end
    pressure_solver = checked_pressure_solver(native_solver, config, rank)
    nonhydrostatic = NonhydrostaticModel(grid;
        momentum_advection=WENO(Float64; order=7), tracer_advection=WENO(Float64; order=7),
        coriolis=HydrostaticSphericalCoriolis(Float64),
        buoyancy=SeawaterBuoyancy(equation_of_state=OceananigansBenchmarks.TEOS10EquationOfState()),
        closure, pressure_solver, tracers=(:T, :S), timestepper=:RungeKutta3)
    initial_seed = get(config, "initial_condition_seed", nothing)
    if !isnothing(initial_seed)
        seed!(initial_seed + rank)
        is_gpu && CUDA.seed!(initial_seed + rank)
    end
    Tᵢ(λ, φ, z) = 30 * (1 - tanh((abs(φ) - 45) / 8)) / 2 + rand()
    Sᵢ(λ, φ, z) = 28 - 5e-3 * z + rand()
    set!(nonhydrostatic; T=Tᵢ, S=Sᵢ)
    nonhydrostatic
else
    error("Unknown model type: $model_type")
end
expected = (config["x_sizes"][arch.local_index[1]], config["y_sizes"][arch.local_index[2]], Nz)
size(model.grid) == expected || error("Unexpected local resolution")
retained_substeps = is_hydrostatic ? length(model.free_surface.substepping.averaging_weights) : nothing
if rank == 0
    println("MODEL_BUILD_FINISHED mode=$execution_mode")
    flush(stdout)
end

function synchronize_model(arch, comm, is_gpu)
    is_gpu && CUDA.synchronize()
    MPI.Barrier(comm)
    return nothing
end

function timing_windows!(model, config, comm, is_gpu)
    # Compile this helper before profiling; the preflight supplies one untimed step.
    durations = Float64[]
    mode = Val(Symbol(get(config, "execution_mode", "baseline")))
    device = is_gpu ? CUDA.device() : nothing
    for sample in 1:config["samples"]
        synchronize_model(architecture(model.grid), comm, is_gpu)
        start = time_ns()
        execute_window!(model, config["dt"], config["time_steps"], is_gpu, device, mode)
        synchronize_model(architecture(model.grid), comm, is_gpu)
        push!(durations, (time_ns() - start) / 1e9)
        if rank == 0
            println("TIMING_WINDOW mode=$(get(config, "execution_mode", "baseline")) sample=$sample seconds=$(last(durations))")
            flush(stdout)
        end
    end
    return durations
end

# One warmup + one unprofiled helper window = two untimed steps.
rank == 0 && println("WARMUP_START mode=$execution_mode")
OceananigansBenchmarks.many_time_steps!(model, config["dt"], config["warmup_steps"] - 1)
preflight = copy(config)
preflight["samples"], preflight["time_steps"] = 1, 1
timing_windows!(model, preflight, comm, is_gpu)
synchronize_model(arch, comm, is_gpu)
rank == 0 && println("WARMUP_FINISHED mode=$execution_mode")
config["profile"] && CUDA.CUDACore.cuProfilerStart()
windows = try
    timing_windows!(model, config, comm, is_gpu)
finally
    is_gpu && CUDA.synchronize()
    config["profile"] && CUDA.CUDACore.cuProfilerStop()
end
true_pressure_residual = nothing
if !is_hydrostatic && get(config, "pressure_check_true_residual", false)
    solver = model.pressure_solver
    cg = solver.native.conjugate_gradient_solver
    compute_symmetric_laplacian!(cg.linear_operator_product, model.pressures.pNHS)
    # make_pressure_correction! stores physical pressure by dividing the
    # solved pressure impulse by the RK stage duration. Restore that scale.
    parent(cg.linear_operator_product) .*= max(eps(Float64), last(solver.records)["projection_dt"])
    parent(cg.residual) .= parent(solver.native.right_hand_side) .- parent(cg.linear_operator_product)
    true_pressure_residual = solver.metric.native(cg.residual)
    tolerance = last(solver.records)["tolerance"]
    rank == 0 && println("PRESSURE_TRUE_RESIDUAL value=$true_pressure_residual tolerance=$tolerance")
    isfinite(true_pressure_residual) && true_pressure_residual <= tolerance || error("Recomputed pressure residual exceeds tolerance")
end
finite_state = all(all(isfinite, interior(t)) for t in values(model.tracers)) &&
               all(all(isfinite, interior(v)) for v in values(model.velocities)) &&
               (is_hydrostatic ? all(isfinite, interior(model.free_surface.displacement)) :
                all(isfinite, interior(model.pressures.pNHS)))
MPI.Allreduce(finite_state ? 1 : 0, MPI.MIN, comm) == 1 || error("Nonfinite model fields")
metadata = JSON.parse(JSON.json(OceananigansBenchmarks.BenchmarkMetadata(arch)))
metadata["mpi_library_version"] = MPI.Get_library_version()
metadata["execution_mode"] = execution_mode
metadata["dagger_version"] = execution_mode == "dagger" ? string(pkgversion(Dagger)) : nothing
metadata["mpi_thread_support"] = string(MPI.Query_thread())
if Sys.islinux()
    peak_rss = match(r"(?m)^VmHWM:\s*(\d+) kB", read("/proc/self/status", String))
    metadata["process_peak_rss_bytes"] = isnothing(peak_rss) ? nothing : parse(Int, peak_rss.captures[1]) * 1024
end
gpu_memory = is_gpu ? CUDA.CUDACore.MemoryInfo() : nothing
if is_gpu
    metadata["gpu_name"] = CUDA.name(CUDA.device())
    metadata["cuda_version"] = string(CUDA.runtime_version())
end
steps = config["time_steps"]
entry = Dict("rank" => rank, "grid_size" => collect(size(model.grid)), "float_type" => "Float64",
             "model_type" => model_type, "free_surface" => is_hydrostatic ? "SplitExplicitFreeSurface" : "RigidLid",
             "pressure_solver" => is_hydrostatic ? nothing : string(nameof(typeof(model.pressure_solver.native))),
             "pressure_preconditioner" => is_hydrostatic ? nothing : string(nameof(typeof(model.pressure_solver.native.conjugate_gradient_solver.preconditioner))),
             "pressure_solver_converged" => is_hydrostatic ? nothing : all(r["converged"] for r in model.pressure_solver.records),
             "pressure_solver_iterations" => is_hydrostatic ? nothing : model.pressure_solver.native.conjugate_gradient_solver.iteration,
             "pressure_solves" => is_hydrostatic ? nothing : model.pressure_solver.records,
             "pressure_final_true_residual" => true_pressure_residual,
             "pressure_preconditioner_details" => !is_hydrostatic && model.pressure_solver.native.conjugate_gradient_solver.preconditioner isa LocalFFTPreconditioner ? model.pressure_solver.native.conjugate_gradient_solver.preconditioner.details : nothing,
             "pressure_preconditioner_validation" => preconditioner_validation,
             "configuration" => config, "metadata" => metadata, "finite_state" => finite_state,
             "retained_free_surface_substeps" => retained_substeps,
             "gpu_memory_used_bytes" => is_gpu ? gpu_memory.total_bytes - gpu_memory.free_bytes : nothing,
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
