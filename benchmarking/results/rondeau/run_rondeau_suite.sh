#!/usr/bin/env bash
set -euo pipefail

# Run inside an allocation or on the GPUs and cores assigned to you.
suite=${1:-all}
script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
repo_root=$(cd "$script_dir/../../.." && pwd)
cd "$repo_root"
dry_run=${DRY_RUN:-0}
julia_bin=${JULIA_BIN:-julia}
mpi_bin=${MPIEXEC:-mpiexec}
nsys_bin=${NSYS_BIN:-nsys}
cpu_counts=${CPU_COUNTS:-"1 2 4 8 16 32 64 128"}
gpu_counts=${GPU_COUNTS:-"1 2 4"}
profile_cpu_threads=${PROFILE_CPU_THREADS:-1}
output_root=${OUTPUT_ROOT:-"$script_dir"}
run_root="$output_root/$(date -u +%Y-%m-%dT%H%M%SZ)_${suite}_$$"
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1

case "$suite" in
    all|cpu_resolution|gpu_resolution|cpu_scaling_default|cpu_scaling_fine|cpu_scaling|gpu_scaling_fine|gpu_scaling_super_fine|gpu_scaling|nsys_gpu|nsys_cpu) ;;
    *) printf 'Unknown suite: %s\n' "$suite" >&2; exit 2 ;;
esac

run_command() {
    printf '%q ' "$@"
    printf '\n'
    if [[ "$dry_run" != 1 ]]; then
        "$@"
    fi
}

benchmark() {
    local folder=$1
    shift
    local destination="$run_root/$folder"
    if [[ "$dry_run" != 1 ]]; then
        mkdir -p "$destination"
        run_command "$@" --output="$destination/results.json" 2>&1 | tee "$destination/run.log"
    else
        run_command "$@" --output="$destination/results.json"
    fi
}

partition_for() {
    # Keep x evenly partitioned across the tripolar fold on the 360 grid.
    if [[ "$1" == 128 && "${2:-}" == 360x180x50 ]]; then
        printf '8x16x1'
        return
    fi
    case "$1" in
        1) printf '1x1x1' ;;
        2) printf '1x2x1' ;;
        4) printf '2x2x1' ;;
        8) printf '2x4x1' ;;
        16) printf '4x4x1' ;;
        32) printf '8x4x1' ;;
        64) printf '8x8x1' ;;
        128) printf '16x8x1' ;;
        *) printf 'Supported rank counts: 1 2 4 8 16 32 64 128; got %s\n' "$1" >&2; return 2 ;;
    esac
}

if [[ "$dry_run" != 1 ]]; then
    required_tools=("$julia_bin")
    if [[ "$suite" == all || "$suite" == cpu_scaling* || "$suite" == gpu_scaling* ]]; then
        required_tools+=("$mpi_bin")
    fi
    if [[ "$suite" == all || "$suite" == nsys_gpu || "$suite" == nsys_cpu ]]; then
        required_tools+=("$nsys_bin")
    fi
    for tool in "${required_tools[@]}"; do
        if ! command -v "$tool" >/dev/null; then
            printf 'Required tool not found: %s. Load the benchmark environment first.\n' "$tool" >&2
            exit 1
        fi
    done
    mkdir -p "$run_root"
    git rev-parse HEAD > "$run_root/revision.txt"
    git status --short > "$run_root/working_tree.txt"
    "$julia_bin" --version > "$run_root/julia_version.txt"
    hostname > "$run_root/hostname.txt"
    lscpu > "$run_root/cpu_info.txt"
    if command -v nvidia-smi >/dev/null; then
        nvidia-smi > "$run_root/gpu_info.txt"
        nvidia-smi topo -m > "$run_root/gpu_topology.txt"
    fi
    if [[ -f benchmarking/Manifest.toml ]]; then
        cp benchmarking/Manifest.toml "$run_root/Manifest.toml"
    fi
fi

common=(--project=benchmarking benchmarking/run_benchmarks.jl --float_type=Float64
        --momentum_advection=WENOVectorInvariantDefault --tracer_advection=WENO7
        --closure=CATKE --timestepper=SplitRungeKutta3 --tracers=T,S --dt=60
        --warmup_steps=2)
timing=(--time_steps=10 --samples=5)
profiling=(--time_steps=2 --samples=1)

if [[ "$suite" == all || "$suite" == cpu_resolution ]]; then
    for size in 180x90x50 360x180x50 720x360x50; do
        grid=lat_lon
        [[ "$size" == 720x360x50 ]] && grid=tripolar
        benchmark "cpu_resolution/$size" "$julia_bin" --threads=1 "${common[@]}" "${timing[@]}" \
            --device=CPU --size="$size" --grid_type="$grid"
    done
fi

if [[ "$suite" == all || "$suite" == gpu_resolution ]]; then
    for size in 180x90x50 360x180x50 720x360x50 1440x720x50; do
        benchmark "gpu_resolution/$size" "$julia_bin" --threads=1 "${common[@]}" "${timing[@]}" \
            --device=GPU --size="$size" --grid_type=lat_lon
    done
fi

if [[ "$suite" == all || "$suite" == cpu_scaling || "$suite" == cpu_scaling_default || "$suite" == cpu_scaling_fine ]]; then
    cpu_sizes=()
    [[ "$suite" == all || "$suite" == cpu_scaling || "$suite" == cpu_scaling_default ]] && cpu_sizes+=("cpu_scaling_default:360x180x50")
    [[ "$suite" == all || "$suite" == cpu_scaling || "$suite" == cpu_scaling_fine ]] && cpu_sizes+=("cpu_scaling_fine:720x360x50")
    for config in "${cpu_sizes[@]}"; do
        series=${config%%:*}
        size=${config#*:}
        for count in $cpu_counts; do
            partition=$(partition_for "$count" "$size")
            run_command "$mpi_bin" -n "$count" --map-by core --bind-to core --report-bindings \
                "$julia_bin" --threads=1 --project=benchmarking "$script_dir/check_rondeau_mpi.jl" CPU "$count"
            benchmark "$series/${count}_cores" "$mpi_bin" -n "$count" \
                --map-by core --bind-to core --report-bindings \
                "$julia_bin" --threads=1 "${common[@]}" "${timing[@]}" \
                --device=CPU --size="$size" --grid_type=tripolar --distributed --partition="$partition"
        done
    done
fi

if [[ "$suite" == all || "$suite" == gpu_scaling || "$suite" == gpu_scaling_fine || "$suite" == gpu_scaling_super_fine ]]; then
    (
    # Required by some MPI implementations that use CUDA's legacy IPC APIs.
    export JULIA_CUDA_MEMORY_POOL=none
    gpu_sizes=()
    [[ "$suite" == all || "$suite" == gpu_scaling || "$suite" == gpu_scaling_fine ]] && gpu_sizes+=("gpu_scaling_fine:720x360x50:tripolar")
    [[ "$suite" == all || "$suite" == gpu_scaling || "$suite" == gpu_scaling_super_fine ]] && gpu_sizes+=("gpu_scaling_super_fine:1440x720x50:lat_lon")
    for config in "${gpu_sizes[@]}"; do
        IFS=: read -r series size grid <<< "$config"
        for count in $gpu_counts; do
            partition=$(partition_for "$count" "$size")
            run_command "$mpi_bin" -n "$count" --map-by core --bind-to core --report-bindings \
                "$julia_bin" --threads=1 --project=benchmarking "$script_dir/check_rondeau_mpi.jl" GPU "$count"
            benchmark "$series/${count}_gpus" "$mpi_bin" -n "$count" \
                --map-by core --bind-to core --report-bindings \
                "$julia_bin" --threads=1 "${common[@]}" "${timing[@]}" \
                --device=GPU --size="$size" --grid_type="$grid" --distributed --partition="$partition"
        done
    done
    )
fi

if [[ "$suite" == all || "$suite" == nsys_gpu ]]; then
    for size in 360x180x50 720x360x50; do
        benchmark "nsys_gpu/$size" "$nsys_bin" profile --trace=cuda,nvtx --sample=none --cpuctxsw=none \
            --output="$run_root/nsys_gpu/$size/profile" \
            "$julia_bin" --threads=1 "${common[@]}" "${profiling[@]}" \
            --device=GPU --size="$size" --grid_type=tripolar
        run_command "$nsys_bin" stats --report cuda_gpu_kern_sum --format csv \
            --output="$run_root/nsys_gpu/$size/kernel_summary" "$run_root/nsys_gpu/$size/profile.nsys-rep"
    done
fi

if [[ "$suite" == all || "$suite" == nsys_cpu ]]; then
    run_command "$nsys_bin" status --environment
    benchmark "nsys_cpu/720x360x50" "$nsys_bin" profile --trace=nvtx --sample=process-tree \
        --cpuctxsw=process-tree --sampling-period=1000000 --backtrace=dwarf --resolve-symbols=true \
        --output="$run_root/nsys_cpu/720x360x50/profile" \
        "$julia_bin" --threads="$profile_cpu_threads" "${common[@]}" "${profiling[@]}" \
        --device=CPU --size=720x360x50 --grid_type=tripolar
fi

printf 'Results: %s\n' "$run_root"
