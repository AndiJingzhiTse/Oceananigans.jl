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
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 180×45×50 | 4970.49 | +1.0% | 0.20 | 8.15e+04 | — | — | 2026-09-30T03:16:15.138 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 180×45×50 | 4970.66 | +1.0% | 0.20 | 8.15e+04 | — | — | 2026-09-30T03:16:15.260 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 180×45×50 | 4970.61 | +1.0% | 0.20 | 8.15e+04 | — | — | 2026-09-30T03:16:15.205 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 180×45×50 | 4969.89 | +1.1% | 0.20 | 8.15e+04 | — | — | 2026-09-30T03:16:14.977 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 4 | Float64 | 180×45×50 | 4970.55 | +1.0% | 0.20 | 8.15e+04 | — | — | 2026-09-30T03:16:15.131 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 5 | Float64 | 180×45×50 | 4970.43 | +1.0% | 0.20 | 8.15e+04 | — | — | 2026-09-30T03:16:15.224 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 6 | Float64 | 180×45×50 | 4970.62 | +1.0% | 0.20 | 8.15e+04 | — | — | 2026-09-30T03:16:15.155 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 7 | Float64 | 180×45×50 | 4969.77 | +1.1% | 0.20 | 8.15e+04 | — | — | 2026-09-30T03:16:14.972 |
