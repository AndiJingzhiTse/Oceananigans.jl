#!/usr/bin/env bash
# Resource counts and output paths are supplied by scaling.py.
#SBATCH --gpus-per-task=h100:1
#SBATCH --cpus-per-task=8
#SBATCH --time=00:45:00
set -e
SCRIPT_DIR=$3  # Slurm runs a spool copy, so BASH_SOURCE is not the source path.
DRAC_ROOT=${DRAC_ROOT:-$HOME/Oceananigans-DRAC}
source "$DRAC_ROOT/env/nibi.sh"
set -eo pipefail
export JULIA_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export JULIA_PKG_PRECOMPILE_AUTO=0
RUN_DIR=$1
PARTITION=$2
mkdir -p "$RUN_DIR"
cd "$SCRIPT_DIR/../.."
git rev-parse HEAD > "$RUN_DIR/revision.txt"
module -t list > "$RUN_DIR/modules.txt" 2>&1
scontrol show job "$SLURM_JOB_ID" > "$RUN_DIR/slurm_job.txt"
srun --ntasks="$SLURM_JOB_NUM_NODES" --ntasks-per-node=1 bash -c 'hostname; nvidia-smi --query-gpu=name,uuid,driver_version,memory.total --format=csv; nvidia-smi topo -m' > "$RUN_DIR/gpu_info.txt"
srun --cpu-bind=none julia --project="$SCRIPT_DIR/environment" "$SCRIPT_DIR/run_benchmark.jl" \
    --mode=benchmark --case=earth_ocean --device=GPU --distributed \
    --partition="$PARTITION" --size=1440x720x200 --grid_type=lat_lon \
    --float_type=Float64 --momentum_advection=WENOVectorInvariantDefault \
    --tracer_advection=WENO7 --closure=CATKE --tracers=T,S \
    --timestepper=SplitRungeKutta3 --dt=60 --warmup_steps=2 --time_steps=10 --samples=5 \
    --output="$RUN_DIR/results.json" --clear
