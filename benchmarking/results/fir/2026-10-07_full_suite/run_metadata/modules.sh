#!/usr/bin/env bash
# Fir software environment; benchmark execution stays in benchmark_suite.py.
module load StdEnv/2023 gcc/12.3 openmpi/4.1.5 julia/1.12.5 cuda/12.6 python/3.11 scipy-stack/2025a
export JULIA_PKG_PRECOMPILE_AUTO=0
