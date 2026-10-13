#!/usr/bin/env bash
#SBATCH --nodes=1
#SBATCH --gpus-per-task=h100:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --time=01:00:00
set -e
GROUP_DIR=$1
TRACE_GROUP_DIR=$2
SCRIPT_DIR=$3
shift 3
source "${DRAC_ROOT:-$HOME/Oceananigans-DRAC}/env/nibi.sh"
set -eo pipefail
export JULIA_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export JULIA_PKG_PRECOMPILE_AUTO=0
nsys --version > "$GROUP_DIR/nsight_version.txt"
module -t list > "$GROUP_DIR/modules.txt" 2>&1
scontrol show job "$SLURM_JOB_ID" > "$GROUP_DIR/slurm_job.txt"
srun --ntasks=1 --ntasks-per-node=1 bash -c 'hostname; nvidia-smi --query-gpu=name,uuid,driver_version,memory.total --format=csv; nvidia-smi topo -m' > "$GROUP_DIR/gpu_info.txt"
failed=0
for partition in "$@"; do
    case_dir="$GROUP_DIR/$partition"
    trace_dir="$TRACE_GROUP_DIR/$partition"
    mkdir -p "$case_dir" "$trace_dir"
    date -u +%FT%TZ > "$case_dir/started.txt"
    git -C "$SCRIPT_DIR" rev-parse HEAD > "$case_dir/revision.txt"
    status=0
    srun --kill-on-bad-exit=1 --cpu-bind=none bash "$SCRIPT_DIR/nsight_rank.sh" "$case_dir" "$trace_dir" "$SCRIPT_DIR" > "$case_dir/job.out" 2>&1 || status=$?
    printf '%s\n' "$status" > "$case_dir/exit_code.txt"
    date -u +%FT%TZ > "$case_dir/finished.txt"
    printf 'Partition %s: exit code %s\n' "$partition" "$status"
    if [[ "$status" != 0 ]]; then failed=1; fi
done
exit "$failed"
