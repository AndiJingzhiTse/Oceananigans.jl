#!/usr/bin/env bash
set -eo pipefail
repository=$(git rev-parse --show-toplevel)
export TMPDIR="$repository/.runtime/tmp" TMP="$repository/.runtime/tmp" TEMP="$repository/.runtime/tmp"
export OMPI_MCA_orte_tmpdir_base="$TMPDIR"
export JULIA_DEPOT_PATH=/scratch/anditse/julia_depot
mkdir -p "$TMPDIR" "$repository/.runtime/nibi_dagger"
source "$repository/benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/modules.sh"
export JULIA_NUM_PRECOMPILE_TASKS=2
julia "$repository/benchmarking/scripts/env/setup_environment.jl" "$repository/.runtime/nibi_dagger/environment"
julia --project="$repository/.runtime/nibi_dagger/environment" -e 'using Pkg; Pkg.add(PackageSpec(name="Dagger", version="0.22.7")); Pkg.precompile()'
julia --project="$repository/.runtime/nibi_dagger/environment" -e 'using OceananigansBenchmarks, CUDA, NCDatasets, MPI, Dagger; println("PASS: benchmark and Dagger package load")'
python3 - <<'PY'
from pathlib import Path
import shutil
repo = Path.cwd()
environment = repo / '.runtime/nibi_dagger/environment'
for family in ('hydrostatic_free_surface_models', 'non_hydrostatic_models'):
    for metadata in (repo / 'benchmarking/results' / family / 'nibi/dagger').glob('*/*/*/run_metadata'):
        for name in ('Project.toml', 'Manifest.toml', 'LocalPreferences.toml'):
            shutil.copy2(environment / name, metadata / name)
PY
