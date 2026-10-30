#!/usr/bin/env bash
set -eo pipefail
source /home/anditse/Oceananigans.jl/benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/modules.sh
python3 /home/anditse/Oceananigans.jl/benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/compare_nibi.py --date 2026-10-30 --refresh --commit
