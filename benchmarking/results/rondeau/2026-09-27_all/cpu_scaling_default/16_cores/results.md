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
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 90×45×50 | 2949.20 | +2.6% | 0.34 | 6.87e+04 | — | — | 2026-09-30T03:34:59.037 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 90×45×50 | 2949.37 | +2.6% | 0.34 | 6.87e+04 | — | — | 2026-09-30T03:34:59.092 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 90×45×50 | 2949.34 | +2.6% | 0.34 | 6.87e+04 | — | — | 2026-09-30T03:34:59.059 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 90×45×50 | 2949.46 | +2.6% | 0.34 | 6.87e+04 | — | — | 2026-09-30T03:34:58.985 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 4 | Float64 | 90×45×50 | 2949.32 | +2.6% | 0.34 | 6.87e+04 | — | — | 2026-09-30T03:34:59.040 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 5 | Float64 | 90×45×50 | 2949.24 | +2.6% | 0.34 | 6.87e+04 | — | — | 2026-09-30T03:34:59.113 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 6 | Float64 | 90×45×50 | 2949.29 | +2.6% | 0.34 | 6.87e+04 | — | — | 2026-09-30T03:34:59.114 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 7 | Float64 | 90×45×50 | 2949.58 | +2.6% | 0.34 | 6.87e+04 | — | — | 2026-09-30T03:34:59.025 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 8 | Float64 | 90×45×50 | 2949.29 | +2.6% | 0.34 | 6.87e+04 | — | — | 2026-09-30T03:34:59.040 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 9 | Float64 | 90×45×50 | 2949.19 | +2.7% | 0.34 | 6.87e+04 | — | — | 2026-09-30T03:34:59.093 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 10 | Float64 | 90×45×50 | 2949.34 | +2.6% | 0.34 | 6.87e+04 | — | — | 2026-09-30T03:34:59.073 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 11 | Float64 | 90×45×50 | 2949.38 | +2.6% | 0.34 | 6.87e+04 | — | — | 2026-09-30T03:34:58.997 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 12 | Float64 | 90×45×50 | 2948.86 | +2.7% | 0.34 | 6.87e+04 | — | — | 2026-09-30T03:34:58.899 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 13 | Float64 | 90×45×50 | 2948.99 | +2.7% | 0.34 | 6.87e+04 | — | — | 2026-09-30T03:34:58.964 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 14 | Float64 | 90×45×50 | 2948.87 | +2.7% | 0.34 | 6.87e+04 | — | — | 2026-09-30T03:34:58.900 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 15 | Float64 | 90×45×50 | 2949.39 | +2.7% | 0.34 | 6.87e+04 | — | — | 2026-09-30T03:34:58.865 |
