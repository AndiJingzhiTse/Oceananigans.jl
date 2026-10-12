#!/usr/bin/env bash
set -eo pipefail
CASE_DIR=$1
TRACE_DIR=$2
SCRIPT_DIR=$3
rank=$SLURM_PROCID
rank_dir="$CASE_DIR/rank_$rank"
trace_rank_dir="$TRACE_DIR/rank_$rank"
mkdir -p "$rank_dir" "$trace_rank_dir"
export NSIGHT_CASE_DIR="$CASE_DIR"
export NSYS_MPI_STORE_TEAMS_PER_RANK=1
nsys profile --trace=cuda,nvtx,mpi --mpi-impl=openmpi --sample=none --cpuctxsw=none \
    --capture-range=cudaProfilerApi --capture-range-end=stop --force-overwrite=true \
    --output="$trace_rank_dir/profile" \
    julia --project="$SCRIPT_DIR/environment" "$SCRIPT_DIR/run_gpu_nsight.jl" > "$rank_dir/profile.out" 2>&1
printf '%s\n' "$trace_rank_dir/profile.nsys-rep" > "$rank_dir/trace_path.txt"
stat -c '%s' "$trace_rank_dir/profile.nsys-rep" > "$rank_dir/trace_bytes.txt"
sha256sum "$trace_rank_dir/profile.nsys-rep" > "$rank_dir/trace_sha256.txt"
# A kernel summary is required. Other reports can be empty (e.g. one rank
# does not perform distributed halo transfers inside the capture).
nsys stats --report cuda_gpu_kern_sum --format csv --force-export=true \
    --output="$rank_dir/summary" "$trace_rank_dir/profile.nsys-rep" > "$rank_dir/stats.out" 2>&1
for report in cuda_api_sum cuda_gpu_mem_time_sum mpi_event_sum nvtx_sum; do
    status=0
    nsys stats --report "$report" --format csv --force-export=true \
        --output="$rank_dir/summary" "$trace_rank_dir/profile.nsys-rep" > "$rank_dir/${report}.out" 2>&1 || status=$?
    printf '%s\n' "$status" > "$rank_dir/${report}_exit_code.txt"
done
printf '0\n' > "$rank_dir/exit_code.txt"
