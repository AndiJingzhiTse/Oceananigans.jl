#!/usr/bin/env bash
#SBATCH --cpus-per-task=1
#SBATCH --time=03:00:00
set -e
RUN_DIR=$1
PARTITION=$2
SCRIPT_DIR=$3
mkdir -p "$RUN_DIR"
date -u +%FT%TZ > "$RUN_DIR/started.txt"
source "${DRAC_ROOT:-$HOME/Oceananigans-DRAC}/env/nibi.sh"
set -eo pipefail
export JULIA_NUM_THREADS="$SLURM_CPUS_PER_TASK"
export JULIA_NUM_GC_THREADS=1
export OPENBLAS_NUM_THREADS=1
export JULIA_PKG_PRECOMPILE_AUTO=0
export CPU_CASE_DIR="$RUN_DIR"
cd "$SCRIPT_DIR/../.."
git rev-parse HEAD > "$RUN_DIR/revision.txt"
module -t list > "$RUN_DIR/modules.txt" 2>&1
scontrol show job "$SLURM_JOB_ID" > "$RUN_DIR/slurm_job.txt"
srun --ntasks="$SLURM_JOB_NUM_NODES" --ntasks-per-node=1 --cpus-per-task=1 bash -c 'hostname; lscpu' > "$RUN_DIR/cpu_info.txt"
status=0
srun --kill-on-bad-exit=1 --distribution=block:block --cpu-bind=cores julia --project="$SCRIPT_DIR/environment" "$SCRIPT_DIR/run_cpu_core_benchmark.jl" || status=$?
printf '%s\n' "$status" > "$RUN_DIR/exit_code.txt"
date -u +%FT%TZ > "$RUN_DIR/finished.txt"
exit "$status"
