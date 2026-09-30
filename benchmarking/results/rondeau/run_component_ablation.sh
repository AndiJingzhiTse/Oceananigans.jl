#!/usr/bin/env bash
set -euo pipefail

# Run six Earth-ocean configurations sequentially on one visible GPU.
script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
repo_root=$(cd "$script_dir/../../.." && pwd)
cd "$repo_root"

julia_bin=${JULIA_BIN:-julia}
gpu_id=${GPU_ID:-0}
dry_run=${DRY_RUN:-0}
output_root=${OUTPUT_ROOT:-$script_dir}
run_root=${RUN_ROOT:-"$output_root/$(date -u +%Y-%m-%dT%H%M%SZ)_component_ablation_$$"}

export CUDA_VISIBLE_DEVICES="$gpu_id"
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1

if [[ "$dry_run" != 1 ]]; then
    command -v "$julia_bin" >/dev/null
    mkdir -p "$run_root"
    git rev-parse HEAD > "$run_root/revision.txt"
    git status --short > "$run_root/working_tree.txt"
    "$julia_bin" --version > "$run_root/julia_version.txt"
    hostname > "$run_root/hostname.txt"
    if command -v nvidia-smi >/dev/null; then
        nvidia-smi -i "$gpu_id" > "$run_root/gpu_info.txt"
    fi
fi

common=(--project=benchmarking benchmarking/run_benchmarks.jl
        --device=GPU --size=360x180x50 --grid_type=tripolar --float_type=Float32
        --momentum_advection=WENOVectorInvariantDefault --tracer_advection=WENO7
        --coriolis=spherical --buoyancy=seawater --closure=CATKE
        --timestepper=SplitRungeKutta3 --tracers=T,S
        --dt=60 --warmup_steps=2 --time_steps=10 --samples=5)

run_case() {
    local name=$1
    shift
    if ((${#selected_cases[@]} > 0)); then
        local selected=0
        for requested in "${selected_cases[@]}"; do
            [[ "$name" == "$requested" ]] && selected=1
        done
        [[ "$selected" == 1 ]] || return 0
    fi
    local destination="$run_root/$name"
    local cmd=("$julia_bin" --threads=1 "${common[@]}" --group="$name" --output="$destination/results.json" "$@")
    printf '%q ' "${cmd[@]}"
    printf '\n'
    if [[ "$dry_run" != 1 ]]; then
        mkdir -p "$destination"
        "${cmd[@]}" 2>&1 | tee "$destination/run.log"
    fi
}

selected_cases=("$@")

run_case baseline
run_case no_tracer_advection --tracer_advection=nothing
run_case no_coriolis --coriolis=nothing
run_case no_buoyancy --buoyancy=nothing
run_case no_closure --closure=nothing
# Seawater buoyancy requires T and S, so this case also disables buoyancy.
run_case no_tracers --tracers=nothing --buoyancy=nothing

printf 'Results: %s\n' "$run_root"
