#!/usr/bin/env bash
# Historical compatibility launcher. New studies use benchmarking/benchmark_suite.py.
set -euo pipefail
script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
BENCHMARK_SCRIPT_DIR="$script_dir" bash "$script_dir/../../legacy/rondeau/run_rondeau_suite.sh" "$@"
