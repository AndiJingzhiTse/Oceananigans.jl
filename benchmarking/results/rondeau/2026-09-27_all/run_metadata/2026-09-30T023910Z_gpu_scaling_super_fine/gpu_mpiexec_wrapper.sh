#!/usr/bin/env bash
set -euo pipefail
args=()
while (($#)); do
    case "$1" in
        --map-by|--bind-to) shift 2 ;;
        *) args+=("$1"); shift ;;
    esac
done
exec /opt/uw/openmpi/4.1.7-with-cuda/bin/mpiexec --rankfile /tmp/rondeau_gpu_rankfile "${args[@]}"
