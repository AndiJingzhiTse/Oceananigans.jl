#!/usr/bin/env bash
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=192
#SBATCH --mem=0
#SBATCH --exclusive
#SBATCH --time=01:00:00
set -e
FOLDER=$1
SCRIPT_DIR=$2
shift 2
failed=0
for partition in "$@"; do
    case_dir="$FOLDER/$partition"
    mkdir -p "$case_dir"
    date -u +%FT%TZ > "$case_dir/started.txt"
    if bash "$SCRIPT_DIR/cpu_benchmark.sh" "$case_dir" "$partition" "$SCRIPT_DIR" > "$case_dir/job.out" 2>&1; then
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
