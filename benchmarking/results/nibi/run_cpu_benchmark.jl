# Load NetCDF before resetting OpenMPI_jll's OPAL_PREFIX, as on the GPU runs.
using OceananigansBenchmarks, Oceananigans, NCDatasets, MPI, JSON
include(joinpath(ENV["OCEANANIGANS_DRAC_ROOT"], "src", "drac_mpi.jl"))
drac_mpi_init()
comm = MPI.COMM_WORLD
rank = MPI.Comm_rank(comm)
ranks = MPI.Comm_size(comm)
Threads.nthreads() == 192 || error("Expected 192 Julia threads per CPU node")
status = read("/proc/self/status", String)
affinity = match(r"(?m)^Cpus_allowed_list:\s*(.+)$", status).captures[1]
layout = Dict("rank" => rank, "hostname" => gethostname(), "threads" => Threads.nthreads(),
              "cpus_per_task" => parse(Int, ENV["SLURM_CPUS_PER_TASK"]), "cpu_affinity" => affinity)
layouts = MPI.gather(layout, comm; root=0)
valid = MPI.bcast(rank == 0 ? length(unique(l["hostname"] for l in layouts)) == ranks : false, comm; root=0)
valid || error("Expected exactly one MPI rank per CPU node")
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
println("rank $rank on $(gethostname()): 192 threads; CPU affinity $affinity")
MPI.Barrier(comm)
rank == 0 && println("PASS: $ranks distinct CPU nodes and CPU MPI ring")
include(joinpath(@__DIR__, "..", "..", "run_benchmarks.jl"))
main()
