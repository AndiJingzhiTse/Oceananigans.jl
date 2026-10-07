#!/usr/bin/env bash
set -eo pipefail
export JULIA_NUM_THREADS=1 JULIA_NUM_GC_THREADS=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
export JULIA_PKG_PRECOMPILE_AUTO=0 JULIA_CUDA_MEMORY_POOL=none
export BENCHMARK_MPI_INIT=/home/anditse/Oceananigans.jl/benchmarking/results/nibi/2026-10-05_gpu_scaling/run_metadata/drac_mpi.jl
failed=0
if type module >/dev/null 2>&1; then module -t list > /home/anditse/Oceananigans.jl/benchmarking/results/rorqual/2026-10-07_full_suite/gpu_scaling_super_fine/2_ranks/modules.txt 2>&1; fi
/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v3/Core/julia/1.12.5/bin/julia --version > /home/anditse/Oceananigans.jl/benchmarking/results/rorqual/2026-10-07_full_suite/gpu_scaling_super_fine/2_ranks/julia_version.txt
if command -v nsys >/dev/null; then nsys --version > /home/anditse/Oceananigans.jl/benchmarking/results/rorqual/2026-10-07_full_suite/gpu_scaling_super_fine/2_ranks/nsight_version.txt; fi
srun --ntasks=1 --ntasks-per-node=1 --cpus-per-task=1 bash -c 'hostname; lscpu; if command -v nvidia-smi >/dev/null; then nvidia-smi --query-gpu=name,uuid,driver_version,memory.total --format=csv; nvidia-smi topo -m; fi' > /home/anditse/Oceananigans.jl/benchmarking/results/rorqual/2026-10-07_full_suite/gpu_scaling_super_fine/2_ranks/compute_hardware.txt
scontrol show job "$SLURM_JOB_ID" > /home/anditse/Oceananigans.jl/benchmarking/results/rorqual/2026-10-07_full_suite/gpu_scaling_super_fine/2_ranks/slurm_job.txt
date -u +%FT%TZ > /home/anditse/Oceananigans.jl/benchmarking/results/rorqual/2026-10-07_full_suite/gpu_scaling_super_fine/2_ranks/started.txt
status=0
srun --kill-on-bad-exit=1 --distribution=block:block --cpu-bind=none bash /home/anditse/Oceananigans.jl/benchmarking/results/rorqual/2026-10-07_full_suite/run_metadata/suite/rank.sh /home/anditse/Oceananigans.jl/benchmarking/results/rorqual/2026-10-07_full_suite/gpu_scaling_super_fine/2_ranks /scratch/anditse/rorqual_benchmark_environment /home/anditse/Oceananigans.jl/benchmarking/results/rorqual/2026-10-07_full_suite/run_metadata/suite/worker.jl /scratch/anditse/benchmark_traces/2026-10-07_full_suite/gpu_scaling_super_fine/2_ranks /cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v3/Core/julia/1.12.5/bin/julia > /home/anditse/Oceananigans.jl/benchmarking/results/rorqual/2026-10-07_full_suite/gpu_scaling_super_fine/2_ranks/job.out 2>&1 || status=$?
printf "%s\n" "$status" > /home/anditse/Oceananigans.jl/benchmarking/results/rorqual/2026-10-07_full_suite/gpu_scaling_super_fine/2_ranks/exit_code.txt
date -u +%FT%TZ > /home/anditse/Oceananigans.jl/benchmarking/results/rorqual/2026-10-07_full_suite/gpu_scaling_super_fine/2_ranks/finished.txt
if [[ "$status" != 0 ]]; then failed=1; fi
exit "$failed"
