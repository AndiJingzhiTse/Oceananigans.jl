module PressureSolverBenchmark

using CUDA: CUDA
using Dates: now, UTC
using FFTW: FFTW
using JSON: JSON
using KernelAbstractions: @kernel, @index
using MPI: MPI
using Statistics: median
using TOML: TOML
using Oceananigans
using Oceananigans.Architectures: architecture
using Oceananigans.DistributedComputations: Distributed, Partition
using Oceananigans.Fields: interior, fill_halo_regions!
using Oceananigans.Models.NonhydrostaticModels: nonhydrostatic_pressure_solver
using Oceananigans.Operators: ∇²ᶜᶜᶜ, divᶜᶜᶜ
using Oceananigans.Solvers: solve!, FFTBasedPoissonSolver
using Oceananigans.Utils: launch!

export run_case, validate_configuration, make_solver, solve_rhs!

function validate_configuration(configuration)
    resolution = configuration["resolution"]
    partition = configuration["partition"]
    length(resolution) == length(partition) == 3 || error("Resolution and partition must have three entries")
    all(resolution .>= 8) || error("Each dimension must contain at least eight cells")
    all(partition .> 0) || error("Partition entries must be positive")
    all(resolution .% partition .== 0) || error("Resolution must be divisible by partition")
    partition[3] == 1 || error("FFT solver requires the vertical dimension to remain local")
    configuration["float_type"] in ("Float32", "Float64") || error("Unsupported precision")
    for key in ("warmup_steps", "windows", "steps_per_window")
        configuration[key] > 0 || error("$key must be positive")
    end
    configuration["timestep"] > 0 || error("Timestep must be positive")
    configuration["viscosity"] >= 0 || error("Viscosity must be nonnegative")
    return nothing
end

function make_solver(grid, ::Val{:native})
    return nonhydrostatic_pressure_solver(grid, nothing)
end

solver_storage(solver::FFTBasedPoissonSolver) = solver.storage
solver_storage(solver) = parent(solver.storage.zfield)

function solve_rhs!(pressure, solver, right_hand_side)
    copyto!(solver_storage(solver), right_hand_side)
    solve!(pressure.data, solver)
    return nothing
end

@kernel function _laplacian!(result, grid, pressure)
    i, j, k = @index(Global, NTuple)
    @inbounds result[i, j, k] = ∇²ᶜᶜᶜ(i, j, k, grid, pressure)
end

@kernel function _divergence!(result, grid, u, v, w)
    i, j, k = @index(Global, NTuple)
    @inbounds result[i, j, k] = divᶜᶜᶜ(i, j, k, grid, u, v, w)
end

function validate_pressure!(pressure, right_hand_side, exact_pressure, comm)
    grid = pressure.grid
    laplacian = CenterField(grid)
    fill_halo_regions!(pressure)
    launch!(architecture(grid), grid, :xyz, _laplacian!, laplacian, grid, pressure)
    residual = interior(laplacian) .- interior(right_hand_side)
    relative_residual = sqrt(MPI.Allreduce(sum(abs2, residual), +, comm) /
                             MPI.Allreduce(sum(abs2, interior(right_hand_side)), +, comm))
    difference = interior(pressure) .- interior(exact_pressure)
    relative_error = sqrt(MPI.Allreduce(sum(abs2, difference), +, comm) /
                          MPI.Allreduce(sum(abs2, interior(exact_pressure)), +, comm))
    tolerance = 100 * eps(eltype(grid)) * maximum(size(grid))^2
    passed = isfinite(relative_residual) && isfinite(relative_error) &&
             relative_residual <= tolerance && relative_error <= tolerance
    passed || error("Pressure validation failed: residual=$relative_residual error=$relative_error tolerance=$tolerance")
    return (; relative_residual, relative_error, tolerance, passed)
end

function measure_windows!(operation, configuration, comm)
    for _ in 1:configuration["warmup_steps"]
        operation()
    end
    CUDA.synchronize()
    local_seconds = Float64[]
    for _ in 1:configuration["windows"]
        MPI.Barrier(comm)
        CUDA.synchronize()
        started = time_ns()
        for _ in 1:configuration["steps_per_window"]
            operation()
        end
        CUDA.synchronize()
        push!(local_seconds, (time_ns() - started) / 1e9)
    end
    maximum_rank_seconds = [MPI.Allreduce(seconds, max, comm) for seconds in local_seconds]
    steps = configuration["steps_per_window"]
    return (; local_seconds, maximum_rank_seconds,
            fastest_seconds_per_operation=minimum(maximum_rank_seconds) / steps,
            median_seconds_per_operation=median(maximum_rank_seconds) / steps)
end

function validate_model!(model, comm)
    velocity = model.velocities
    divergence = CenterField(model.grid)
    foreach(fill_halo_regions!, values(velocity))
    launch!(architecture(model.grid), model.grid, :xyz, _divergence!, divergence,
            model.grid, velocity.u, velocity.v, velocity.w)
    maximum_divergence = MPI.Allreduce(maximum(abs, interior(divergence)), max, comm)
    finite = MPI.Allreduce(all(all(isfinite, interior(field)) for field in values(velocity)), &, comm)
    tolerance = 100 * eps(eltype(model.grid)) * maximum(size(model.grid))^2
    finite && maximum_divergence <= tolerance || error("Model validation failed: divergence=$maximum_divergence")
    return (; finite, maximum_divergence, tolerance, passed=true)
end

function run_case(configuration_path, output_directory; backend=:native)
    configuration = TOML.parsefile(configuration_path)
    validate_configuration(configuration)
    MPI.Initialized() || MPI.Init()
    comm = MPI.COMM_WORLD
    rank, ranks = MPI.Comm_rank(comm), MPI.Comm_size(comm)
    prod(configuration["partition"]) == ranks || error("MPI rank count does not match partition")
    CUDA.functional() || error("This study requires a CUDA GPU; CPU studies remain cancelled on Rondeau")
    length(CUDA.devices()) >= ranks || error("Expose at least one distinct GPU per rank")
    arch = ranks == 1 ? GPU() : Distributed(GPU(); partition=Partition(configuration["partition"]...))
    float_type = configuration["float_type"] == "Float64" ? Float64 : Float32
    resolution = Tuple(configuration["resolution"])
    grid = RectilinearGrid(arch, float_type; size=resolution, extent=(2π, 2π, 2π),
                           topology=(Periodic, Periodic, Periodic), halo=(4, 4, 4))
    started = time_ns()
    solver = make_solver(grid, Val(backend))
    CUDA.synchronize()
    construction_seconds = (time_ns() - started) / 1e9
    pressure, exact_pressure, right_hand_side = CenterField(grid), CenterField(grid), CenterField(grid)
    set!(exact_pressure, (x, y, z) -> cos(x) * cos(2y) * cos(3z))
    fill_halo_regions!(exact_pressure)
    launch!(arch, grid, :xyz, _laplacian!, right_hand_side, grid, exact_pressure)
    source = copy(interior(right_hand_side))
    pressure_timing = measure_windows!(() -> solve_rhs!(pressure, solver, source), configuration, comm)
    pressure_validation = validate_pressure!(pressure, right_hand_side, exact_pressure, comm)

    model = NonhydrostaticModel(grid; pressure_solver=solver, timestepper=:RungeKutta3,
                               advection=Centered(order=2), buoyancy=nothing, coriolis=nothing,
                               closure=ScalarDiffusivity(ν=configuration["viscosity"]), tracers=())
    set!(model, u=(x, y, z) -> sin(x) * cos(y) * cos(z),
                v=(x, y, z) -> -cos(x) * sin(y) * cos(z), w=0)
    timestep = float_type(configuration["timestep"])
    timestep_timing = measure_windows!(() -> time_step!(model, timestep), configuration, comm)
    model_validation = validate_model!(model, comm)
    mkpath(output_directory)
    result = (; status="COMPLETED", backend, configuration, grid_type="RectilinearGrid",
              topology=["Periodic", "Periodic", "Periodic"], local_resolution=size(grid), rank, ranks,
              device=string(CUDA.device()), gpu_uuid=string(CUDA.uuid(CUDA.device())),
              julia_version=string(VERSION), oceananigans_version=string(pkgversion(Oceananigans)),
              cuda_version=string(pkgversion(CUDA)), mpi_library=MPI.Get_library_version(),
              cuda_runtime=string(CUDA.runtime_version()), cuda_driver=string(CUDA.driver_version()),
              fftw_version=string(pkgversion(FFTW)), cpu=Sys.CPU_NAME,
              cpu_affinity=Sys.islinux() ? match(r"Cpus_allowed_list:\s*([^\n]+)", read("/proc/self/status", String))[1] : "unavailable",
              visible_devices=get(ENV, "CUDA_VISIBLE_DEVICES", ""),
              environment=Base.active_project(), solver_type=string(typeof(solver)),
              julia_threads=Threads.nthreads(), source_path=pathof(Oceananigans),
              source_revision=readchomp(`git -C $(joinpath(@__DIR__, "../..")) rev-parse HEAD`),
              source_dirty=!isempty(readchomp(`git -C $(joinpath(@__DIR__, "../..")) status --porcelain`)),
              timestamp=string(now(UTC)), construction_seconds, pressure_timing, pressure_validation,
              timestep_timing, model_validation,
              temporary_directory=realpath(tempdir()), command=Base.PROGRAM_FILE * " " * join(ARGS, " "))
    open(joinpath(output_directory, "rank_$rank.json"), "w") do io
        JSON.json(io, result; pretty=true)
    end
    println("PASS rank=$rank backend=$backend pressure=$(pressure_timing.median_seconds_per_operation) timestep=$(timestep_timing.median_seconds_per_operation)")
    return result
end

end
