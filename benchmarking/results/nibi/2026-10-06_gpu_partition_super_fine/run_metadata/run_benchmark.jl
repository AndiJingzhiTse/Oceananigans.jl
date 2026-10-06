# Load NetCDF/HDF5 before the DRAC helper resets OpenMPI_jll's OPAL_PREFIX.
using OceananigansBenchmarks, Oceananigans, CUDA, NCDatasets, MPI
include(joinpath(ENV["OCEANANIGANS_DRAC_ROOT"], "src", "drac_mpi.jl"))
drac_mpi_init()

comm = MPI.COMM_WORLD
rank = MPI.Comm_rank(comm)
ranks = MPI.Comm_size(comm)
gpu_uuid = string(CUDA.uuid(CUDA.device()))
println("rank $rank on $(gethostname()): $(CUDA.name(CUDA.device())), UUID $gpu_uuid")
uuids = MPI.gather(gpu_uuid, comm; root=0)
distinct = MPI.bcast(rank == 0 ? length(unique(uuids)) == ranks : false, comm; root=0)
distinct || error("MPI ranks share GPUs")

# Verify CUDA-aware MPI at every count, including inter-node transport.
send_buffer = CUDA.fill(Float64(rank), 1024)
receive_buffer = CUDA.zeros(Float64, 1024)
source = mod(rank - 1, ranks)
MPI.Sendrecv!(send_buffer, receive_buffer, comm; dest=mod(rank + 1, ranks), source)
correct = all(Array(receive_buffer) .== source)
MPI.Allreduce(correct ? 1 : 0, MPI.MIN, comm) == 1 || error("CUDA-aware MPI ring check failed")
rank == 0 && println("PASS: $ranks distinct GPUs and CUDA-aware MPI")
MPI.Barrier(comm)

include(joinpath(@__DIR__, "..", "..", "run_benchmarks.jl"))
main()  # The suite's PROGRAM_FILE guard does not run when included by this wrapper.
