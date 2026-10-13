#!/usr/bin/env bash
# Prepare an isolated Julia environment on Fir, Nibi or Rorqual before Slurm jobs.
set -eo pipefail
script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
machine=${1:?Usage: setup.sh fir|nibi|rorqual}
case "$machine" in fir|nibi|rorqual) ;; *) echo "Choose fir, nibi or rorqual" >&2; exit 2 ;; esac
source "$script_dir/modules.sh"
environment="${SCRATCH:-/scratch/$USER}/oceananigans_benchmark_environments/$machine"
export JULIA_DEPOT_PATH="${JULIA_DEPOT_PATH:-${SCRATCH:-/scratch/$USER}/julia_depot:}"
export JULIA_NUM_PRECOMPILE_TASKS="${JULIA_NUM_PRECOMPILE_TASKS:-4}"
julia "$script_dir/setup_environment.jl" "$environment"
julia --project="$environment" -e 'using Pkg; Pkg.precompile()'
# Load NetCDF/CUDA before selecting the system OpenMPI runtime.
julia --project="$environment" -e 'using OceananigansBenchmarks, CUDA, NCDatasets; include(ARGS[1]); drac_mpi_init(); println("PASS: benchmark environment")' "$script_dir/drac_mpi.jl"
