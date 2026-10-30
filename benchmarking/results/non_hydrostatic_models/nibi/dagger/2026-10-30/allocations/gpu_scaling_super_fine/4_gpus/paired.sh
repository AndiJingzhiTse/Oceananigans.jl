#!/usr/bin/env bash
failed=0
bash /home/anditse/Oceananigans.jl/benchmarking/results/non_hydrostatic_models/nibi/dagger/2026-10-30/baseline/gpu_scaling_super_fine/4_ranks/allocation.sh || failed=1
bash /home/anditse/Oceananigans.jl/benchmarking/results/non_hydrostatic_models/nibi/dagger/2026-10-30/dagger/gpu_scaling_super_fine/4_ranks/allocation.sh || failed=1
exit "$failed"
