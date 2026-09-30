# Oceananigans Benchmark Results

## System Information

| Property | Value |
|----------|-------|
| Julia | 1.12.7 |
| Oceananigans | 0.113.0 |
| Architecture | Distributed{CPU, false, Partition{Int64, Int64, Int64}, Tuple{Int64, Int64, Int64}, Int64, Tuple{Int64, Int64, Int64}, Oceananigans.DistributedComputations.NeighboringRanks{Int64, Int64, Int64, Int64, Int64, Int64, Int64, Int64}, MPI.Comm, Vector{MPI.Request}, Base.RefValue{Int64}, Nothing} |
| CPU | AMD EPYC 7713 64-Core Processor (znver3) |
| Threads | 1 |
| Hostname | rondeau |
| Adapt | 4.7.1 |
| CUDA | 6.1.0 |
| GPUArrays | 11.5.14 |
| GPUCompiler | 1.17.1 |
| KernelAbstractions | 0.9.42 |
| LLVM | 9.13.2 |

## Results

| Benchmark | Distributed | Float | Grid | Time/unit (ms) | Spread | Units/s | Points/s | Size | Chunks | Timestamp |
|-----------|-------------|-------|------|----------------|--------|---------|----------|------|--------|-----------|
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 90×90×50 | 5834.52 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.434 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 90×90×50 | 5834.63 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.500 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 90×90×50 | 5834.63 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.406 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 90×90×50 | 5834.73 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.171 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 4 | Float64 | 90×90×50 | 5834.95 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.557 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 5 | Float64 | 90×90×50 | 5834.70 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.612 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 6 | Float64 | 90×90×50 | 5834.81 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.629 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 7 | Float64 | 90×90×50 | 5834.73 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.521 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 8 | Float64 | 90×90×50 | 5833.61 | +1.6% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.616 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 9 | Float64 | 90×90×50 | 5834.82 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.712 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 10 | Float64 | 90×90×50 | 5834.91 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.726 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 11 | Float64 | 90×90×50 | 5834.74 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.593 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 12 | Float64 | 90×90×50 | 5833.74 | +1.6% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.626 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 13 | Float64 | 90×90×50 | 5834.40 | +1.6% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.726 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 14 | Float64 | 90×90×50 | 5834.82 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.687 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 15 | Float64 | 90×90×50 | 5835.52 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.531 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 16 | Float64 | 90×90×50 | 5833.86 | +1.6% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.588 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 17 | Float64 | 90×90×50 | 5833.88 | +1.6% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.645 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 18 | Float64 | 90×90×50 | 5833.66 | +1.6% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.619 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 19 | Float64 | 90×90×50 | 5834.06 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.432 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 20 | Float64 | 90×90×50 | 5830.13 | +1.6% | 0.17 | 6.95e+04 | — | — | 2026-09-27T20:25:07.269 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 21 | Float64 | 90×90×50 | 5834.93 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.494 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 22 | Float64 | 90×90×50 | 5834.93 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.542 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 23 | Float64 | 90×90×50 | 5834.85 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.431 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 24 | Float64 | 90×90×50 | 5834.93 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.197 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 25 | Float64 | 90×90×50 | 5834.88 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.481 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 26 | Float64 | 90×90×50 | 5834.90 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.440 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 27 | Float64 | 90×90×50 | 5834.86 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.426 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 28 | Float64 | 90×90×50 | 5834.70 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.435 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 29 | Float64 | 90×90×50 | 5834.53 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.480 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 30 | Float64 | 90×90×50 | 5834.55 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:07.403 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 31 | Float64 | 90×90×50 | 5835.60 | +1.5% | 0.17 | 6.94e+04 | — | — | 2026-09-27T20:25:06.706 |
