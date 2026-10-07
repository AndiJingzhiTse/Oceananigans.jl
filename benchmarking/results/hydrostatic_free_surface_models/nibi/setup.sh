#!/usr/bin/env bash
# Run on a login node before submitting GPU jobs.
set -e
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
DRAC_ROOT=${DRAC_ROOT:-$HOME/Oceananigans-DRAC}
export JULIA_DEPOT_PATH="${JULIA_DEPOT_PATH:-/scratch/$USER/julia_depot}"
source "$DRAC_ROOT/env/drac.sh"
set -eo pipefail
export JULIA_NUM_PRECOMPILE_TASKS=${JULIA_NUM_PRECOMPILE_TASKS:-4}
export JULIA_PKG_PRECOMPILE_AUTO=0
julia "$SCRIPT_DIR/setup_environment.jl" "$SCRIPT_DIR/environment"
julia --project="$SCRIPT_DIR/environment" -e 'using Pkg; Pkg.precompile()'
# Load all benchmark dependencies before resetting OPAL_PREFIX, as required on Nibi.
julia --project="$SCRIPT_DIR/environment" -e 'using OceananigansBenchmarks, CUDA, NCDatasets; include(joinpath(ENV["OCEANANIGANS_DRAC_ROOT"], "src", "drac_mpi.jl")); drac_mpi_init(); println("PASS: Nibi benchmark environment")'
