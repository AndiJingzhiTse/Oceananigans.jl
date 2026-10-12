#!/usr/bin/env bash
# Submit with an afterany dependency on every requested GPU job.
#SBATCH --job-name=nibi_scaling_finalize
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:05:00
set -e
module load StdEnv/2023 python/3.11 scipy-stack/2025a
set -eo pipefail
export OPENBLAS_NUM_THREADS=1
python3 "$2/refresh_scaling.py" "$1" --watch --poll-seconds=30 --commit
