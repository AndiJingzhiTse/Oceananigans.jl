#!/usr/bin/env bash
#SBATCH --nodes=1
#SBATCH --ntasks=3
#SBATCH --ntasks-per-node=3
#SBATCH --cpus-per-task=1
#SBATCH --mem=12G
#SBATCH --time=00:20:00
set -e
source /home/anditse/Oceananigans-DRAC/env/nibi.sh
export JULIA_NUM_THREADS=1
export JULIA_NUM_GC_THREADS=1
export OPENBLAS_NUM_THREADS=1
export JULIA_PKG_PRECOMPILE_AUTO=0
export CPU_CASE_DIR="$1"
srun --kill-on-bad-exit=1 --distribution=block:block --cpu-bind=cores julia --project=/home/anditse/Oceananigans.jl/benchmarking/results/nibi/environment /home/anditse/Oceananigans.jl/benchmarking/results/nibi/run_cpu_core_benchmark.jl
