using MPI
using CUDA
using Oceananigans
using Oceananigans.DistributedComputations: Distributed, Partition

function check_mpi()
    device = ARGS[1]
    expected_ranks = parse(Int, ARGS[2])
    MPI.Init()
    communicator = MPI.COMM_WORLD
    ranks = MPI.Comm_size(communicator)
    rank = MPI.Comm_rank(communicator)
    ranks == expected_ranks || error("Expected $expected_ranks MPI ranks, found $ranks. Check the MPI launcher and MPI.jl library.")

    if rank == 0
        MPI.versioninfo()
    end

    if device == "GPU"
        local_comm = MPI.Comm_split_type(communicator, MPI.COMM_TYPE_SHARED, rank)
        local_ranks = MPI.Comm_size(local_comm)
        visible_gpus = length(collect(CUDA.devices()))
        visible_gpus >= local_ranks || error("Each rank must see all GPUs assigned to this run: $local_ranks local ranks, $visible_gpus visible GPUs.")
        MPI.has_cuda() || error("The loaded MPI library does not report CUDA support.")
        Distributed(GPU(); partition=Partition(1, ranks, 1))
        println("Rank $rank: GPU $(CUDA.device()), $(CUDA.name(CUDA.device()))")

        # Exercise communication using actual device buffers, beyond capability detection.
        buffer = CUDA.fill(Int32(rank + 1), 1)
        CUDA.synchronize()
        MPI.Allreduce!(buffer, MPI.SUM, communicator)
        CUDA.synchronize()
        expected_sum = ranks * (ranks + 1) ÷ 2
        only(Array(buffer)) == expected_sum || error("CUDA buffer MPI reduction failed.")
    else
        println("Rank $rank: CPU, Julia threads $(Threads.nthreads())")
    end

    MPI.Barrier(communicator)
    rank == 0 && println("MPI check passed for $device on $ranks ranks.")
    MPI.Finalize()
    return nothing
end

try
    check_mpi()
catch exception
    showerror(stderr, exception, catch_backtrace())
    println(stderr)
    if MPI.Initialized() && !MPI.Finalized()
        MPI.Abort(MPI.COMM_WORLD, 1)
    end
    rethrow()
end
