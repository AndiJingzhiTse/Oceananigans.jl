#!/usr/bin/env bash
set -eo pipefail
export JULIA_NUM_THREADS=1 JULIA_NUM_GC_THREADS=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
export JULIA_PKG_PRECOMPILE_AUTO=0 JULIA_CUDA_MEMORY_POOL=none
export BENCHMARK_MPI_INIT=/home/anditse/Oceananigans.jl/benchmarking/results/nibi/2026-10-05_gpu_scaling/run_metadata/drac_mpi.jl
module load python/3.11 scipy-stack/2025a
python3 /home/anditse/Oceananigans.jl/benchmarking/results/rorqual/2026-10-07_full_suite/run_metadata/benchmark_suite.py --output /home/anditse/Oceananigans.jl/benchmarking/results/rorqual/2026-10-07_full_suite --refresh --commit
