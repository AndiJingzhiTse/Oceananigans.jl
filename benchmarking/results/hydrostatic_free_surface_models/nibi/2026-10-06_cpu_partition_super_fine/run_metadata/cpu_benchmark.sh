#!/usr/bin/env bash
set -e
RUN_DIR=$1
PARTITION=$2
SCRIPT_DIR=$3
source "${DRAC_ROOT:-$HOME/Oceananigans-DRAC}/env/nibi.sh"
set -eo pipefail
export JULIA_NUM_THREADS=192
export OPENBLAS_NUM_THREADS=1
export JULIA_PKG_PRECOMPILE_AUTO=0
export CPU_CASE_DIR="$RUN_DIR"
mkdir -p "$RUN_DIR"
cd "$SCRIPT_DIR/../.."
git rev-parse HEAD > "$RUN_DIR/revision.txt"
module -t list > "$RUN_DIR/modules.txt" 2>&1
scontrol show job "$SLURM_JOB_ID" > "$RUN_DIR/slurm_job.txt"
srun --ntasks-per-node=1 --cpu-bind=cores bash -c 'hostname; lscpu; cat /proc/self/status | sed -n "/Cpus_allowed_list/p"' > "$RUN_DIR/cpu_info.txt"
srun --kill-on-bad-exit=1 --ntasks-per-node=1 --cpu-bind=cores julia --project="$SCRIPT_DIR/environment" "$SCRIPT_DIR/run_cpu_benchmark.jl" \
    --mode=benchmark --case=earth_ocean --device=CPU --distributed \
    --partition="$PARTITION" --size=1440x720x200 --grid_type=lat_lon \
    --float_type=Float64 --momentum_advection=WENOVectorInvariantDefault \
    --tracer_advection=WENO7 --closure=CATKE --tracers=T,S \
    --timestepper=SplitRungeKutta3 --dt=60 --warmup_steps=2 --time_steps=10 --samples=5 \
    --output="$RUN_DIR/results.json" --clear
