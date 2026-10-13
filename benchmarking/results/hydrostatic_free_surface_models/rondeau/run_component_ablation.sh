#!/usr/bin/env bash
# Historical compatibility launcher. New studies use benchmarking/benchmark_suite.py.
set -euo pipefail
script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
_benchmark_dir="$script_dir"
while [[ ! -d "$_benchmark_dir/legacy" ]]; do _benchmark_dir=$(dirname "$_benchmark_dir"); done
BENCHMARK_SCRIPT_DIR="$script_dir" bash "$_benchmark_dir/legacy/rondeau/run_component_ablation.sh" "$@"
