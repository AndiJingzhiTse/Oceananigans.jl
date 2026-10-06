#!/usr/bin/env bash
#SBATCH --job-name=nibi_nsight_finalize
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:15:00
set -e
module load StdEnv/2023 python/3.11 scipy-stack/2025a
export OPENBLAS_NUM_THREADS=1
python3 "$2/nsight_series.py" "$1" --watch --commit
