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
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 45×45×50 | 1634.77 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.375 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 45×45×50 | 1634.63 | +6.5% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.414 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 45×45×50 | 1634.69 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.355 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 45×45×50 | 1635.11 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.266 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 4 | Float64 | 45×45×50 | 1634.76 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.373 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 5 | Float64 | 45×45×50 | 1635.05 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.393 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 6 | Float64 | 45×45×50 | 1634.90 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.393 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 7 | Float64 | 45×45×50 | 1634.85 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.355 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 8 | Float64 | 45×45×50 | 1635.01 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.378 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 9 | Float64 | 45×45×50 | 1634.75 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.419 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 10 | Float64 | 45×45×50 | 1634.80 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.434 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 11 | Float64 | 45×45×50 | 1634.84 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.390 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 12 | Float64 | 45×45×50 | 1635.00 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.379 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 13 | Float64 | 45×45×50 | 1634.87 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.429 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 14 | Float64 | 45×45×50 | 1634.88 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.420 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 15 | Float64 | 45×45×50 | 1634.89 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.363 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 16 | Float64 | 45×45×50 | 1634.97 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.375 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 17 | Float64 | 45×45×50 | 1635.01 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.391 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 18 | Float64 | 45×45×50 | 1635.00 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.374 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 19 | Float64 | 45×45×50 | 1635.17 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.317 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 20 | Float64 | 45×45×50 | 1635.05 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.317 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 21 | Float64 | 45×45×50 | 1635.09 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.369 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 22 | Float64 | 45×45×50 | 1635.12 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.389 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 23 | Float64 | 45×45×50 | 1635.12 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.349 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 24 | Float64 | 45×45×50 | 1635.10 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.303 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 25 | Float64 | 45×45×50 | 1635.13 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.375 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 26 | Float64 | 45×45×50 | 1635.10 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.347 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 27 | Float64 | 45×45×50 | 1635.12 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.346 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 28 | Float64 | 45×45×50 | 1634.73 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.393 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 29 | Float64 | 45×45×50 | 1634.73 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.392 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 30 | Float64 | 45×45×50 | 1634.72 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.356 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 31 | Float64 | 45×45×50 | 1635.22 | +6.4% | 0.61 | 6.19e+04 | — | — | 2026-09-30T03:53:23.174 |
