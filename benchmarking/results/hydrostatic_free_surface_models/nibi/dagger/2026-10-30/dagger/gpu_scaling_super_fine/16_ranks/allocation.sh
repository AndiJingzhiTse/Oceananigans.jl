#!/usr/bin/env bash
set -eo pipefail
mkdir -p /home/anditse/Oceananigans.jl/.runtime/tmp
export JULIA_DEPOT_PATH=/scratch/anditse/julia_depot
export TMPDIR=/home/anditse/Oceananigans.jl/.runtime/tmp
export TMP=/home/anditse/Oceananigans.jl/.runtime/tmp
export TEMP=/home/anditse/Oceananigans.jl/.runtime/tmp
export OMPI_MCA_orte_tmpdir_base=/home/anditse/Oceananigans.jl/.runtime/tmp
source /home/anditse/Oceananigans.jl/benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/modules.sh
export JULIA_NUM_THREADS=1 JULIA_NUM_GC_THREADS=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
export JULIA_PKG_PRECOMPILE_AUTO=0 JULIA_CUDA_MEMORY_POOL=none
export BENCHMARK_MPI_INIT=/home/anditse/Oceananigans.jl/benchmarking/scripts/env/drac_mpi.jl
failed=0
if type module >/dev/null 2>&1; then module -t list > /home/anditse/Oceananigans.jl/benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/2026-10-30/dagger/gpu_scaling_super_fine/16_ranks/modules.txt 2>&1; fi
julia --version > /home/anditse/Oceananigans.jl/benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/2026-10-30/dagger/gpu_scaling_super_fine/16_ranks/julia_version.txt
if command -v nsys >/dev/null; then nsys --version > /home/anditse/Oceananigans.jl/benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/2026-10-30/dagger/gpu_scaling_super_fine/16_ranks/nsight_version.txt; fi
srun --ntasks=2 --ntasks-per-node=1 --cpus-per-task=1 bash -c 'hostname; lscpu; nvidia-smi --query-gpu=name,uuid,driver_version,memory.total --format=csv; nvidia-smi topo -m' > /home/anditse/Oceananigans.jl/benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/2026-10-30/dagger/gpu_scaling_super_fine/16_ranks/compute_hardware.txt
scontrol show job "$SLURM_JOB_ID" > /home/anditse/Oceananigans.jl/benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/2026-10-30/dagger/gpu_scaling_super_fine/16_ranks/slurm_job.txt
date -u +%FT%TZ > /home/anditse/Oceananigans.jl/benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/2026-10-30/dagger/gpu_scaling_super_fine/16_ranks/started.txt
status=0
srun --kill-on-bad-exit=1 --distribution=block:block --cpu-bind=none bash /home/anditse/Oceananigans.jl/benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/2026-10-30/dagger/gpu_scaling_super_fine/run_metadata/src/suite/rank.sh /home/anditse/Oceananigans.jl/benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/2026-10-30/dagger/gpu_scaling_super_fine/16_ranks /home/anditse/Oceananigans.jl/.runtime/nibi_dagger/environment /home/anditse/Oceananigans.jl/benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/2026-10-30/dagger/gpu_scaling_super_fine/run_metadata/src/suite/worker.jl /home/anditse/Oceananigans.jl/benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/2026-10-30/dagger/raw_profiles/hydrostatic_free_surface_models/nibi/dc0fc4e207fcfff2/gpu_scaling_super_fine/gpu_scaling_super_fine/16_ranks julia > /home/anditse/Oceananigans.jl/benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/2026-10-30/dagger/gpu_scaling_super_fine/16_ranks/job.out 2>&1 || status=$?
printf "%s\n" "$status" > /home/anditse/Oceananigans.jl/benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/2026-10-30/dagger/gpu_scaling_super_fine/16_ranks/exit_code.txt
date -u +%FT%TZ > /home/anditse/Oceananigans.jl/benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/2026-10-30/dagger/gpu_scaling_super_fine/16_ranks/finished.txt
if [[ "$status" != 0 ]]; then failed=1; fi
exit "$failed"
