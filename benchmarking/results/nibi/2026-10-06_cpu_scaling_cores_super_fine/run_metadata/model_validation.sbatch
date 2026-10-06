#!/usr/bin/env bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=12G
#SBATCH --time=00:15:00
set -e
source /home/anditse/Oceananigans-DRAC/env/nibi.sh
export JULIA_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
julia --project=/home/anditse/Oceananigans.jl/benchmarking/results/nibi/environment /home/anditse/Oceananigans.jl/benchmarking/results/nibi/test_cpu_core_model.jl
