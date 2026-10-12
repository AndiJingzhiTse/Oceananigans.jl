#!/usr/bin/env bash
# Three independent Julia/MPI launches on the same four-GPU allocation.
#SBATCH --job-name=nibi_partitions_4
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --ntasks-per-node=4
#SBATCH --gpus-per-task=h100:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=00:30:00
set -euo pipefail
SERIES_DIR=$1
SCRIPT_DIR=$2
mkdir -p "$SERIES_DIR"
failed=0
for partition in 4x1x1 2x2x1 1x4x1; do
    case_dir="$SERIES_DIR/$partition"
    mkdir -p "$case_dir"
    date -u +%FT%TZ > "$case_dir/started.txt"
    if bash "$SCRIPT_DIR/benchmark.sbatch" "$case_dir" "$partition" "$SCRIPT_DIR" > "$case_dir/job.out" 2>&1; then
        status=0
    else
        status=$?
        failed=1
    fi
    printf '%s\n' "$status" > "$case_dir/exit_code.txt"
    date -u +%FT%TZ > "$case_dir/finished.txt"
    printf 'Partition %s: exit code %s\n' "$partition" "$status"
done
exit "$failed"
