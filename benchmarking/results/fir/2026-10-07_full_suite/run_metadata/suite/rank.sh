#!/usr/bin/env bash
# One rank per CPU core or GPU; called by either srun or mpiexec.
set -euo pipefail
case_dir=$1
project=$2
worker=$3
trace_dir=$4
julia_bin=$5
rank=${SLURM_PROCID:-${OMPI_COMM_WORLD_RANK:-${PMI_RANK:-0}}}
rank_dir="$case_dir/rank_$rank"
mkdir -p "$rank_dir"
export JULIA_NUM_THREADS=1 JULIA_NUM_GC_THREADS=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
export JULIA_PKG_PRECOMPILE_AUTO=0
profile=$(python3 -c 'import json,sys; print(int(json.load(open(sys.argv[1]))["profile"]))' "$case_dir/configuration.json")
if [[ "$profile" == 0 ]]; then
    exec "$julia_bin" --threads=1 --project="$project" "$worker" "$case_dir"
fi
export NSYS_MPI_STORE_TEAMS_PER_RANK=1
trace_rank="$trace_dir/rank_$rank"
mkdir -p "$trace_rank"
nsys profile --trace=cuda,nvtx,mpi --mpi-impl=openmpi --sample=none --cpuctxsw=none \
    --capture-range=cudaProfilerApi --capture-range-end=stop --force-overwrite=true \
    --output="$trace_rank/profile" \
    "$julia_bin" --threads=1 --project="$project" "$worker" "$case_dir" > "$rank_dir/profile.out" 2>&1
printf '%s\n' "$trace_rank/profile.nsys-rep" > "$rank_dir/trace_path.txt"
stat -c '%s' "$trace_rank/profile.nsys-rep" > "$rank_dir/trace_bytes.txt"
sha256sum "$trace_rank/profile.nsys-rep" > "$rank_dir/trace_sha256.txt"
nsys stats --report cuda_gpu_kern_sum --format csv --force-export=true --force-overwrite=true \
    --output="$rank_dir/summary" "$trace_rank/profile.nsys-rep" > "$rank_dir/stats.out" 2>&1
for report in cuda_api_sum cuda_gpu_mem_time_sum mpi_event_sum nvtx_sum; do
    status=0
    nsys stats --report "$report" --format csv --force-overwrite=true \
        --output="$rank_dir/summary" "$trace_rank/profile.nsys-rep" > "$rank_dir/$report.out" 2>&1 || status=$?
    printf '%s\n' "$status" > "$rank_dir/${report}_exit_code.txt"
done
printf '0\n' > "$rank_dir/exit_code.txt"
