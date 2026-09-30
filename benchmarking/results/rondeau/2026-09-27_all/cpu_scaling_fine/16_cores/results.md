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
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 180×90×50 | 10962.78 | +1.1% | 0.09 | 7.39e+04 | — | — | 2026-09-27T09:19:16.376 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 180×90×50 | 10962.71 | +1.2% | 0.09 | 7.39e+04 | — | — | 2026-09-27T09:19:16.492 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 180×90×50 | 10962.89 | +1.1% | 0.09 | 7.39e+04 | — | — | 2026-09-27T09:19:16.415 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 180×90×50 | 10962.75 | +1.1% | 0.09 | 7.39e+04 | — | — | 2026-09-27T09:19:16.225 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 4 | Float64 | 180×90×50 | 10962.65 | +1.2% | 0.09 | 7.39e+04 | — | — | 2026-09-27T09:19:16.377 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 5 | Float64 | 180×90×50 | 10962.56 | +1.2% | 0.09 | 7.39e+04 | — | — | 2026-09-27T09:19:16.537 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 6 | Float64 | 180×90×50 | 10962.57 | +1.1% | 0.09 | 7.39e+04 | — | — | 2026-09-27T09:19:16.511 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 7 | Float64 | 180×90×50 | 10962.77 | +1.1% | 0.09 | 7.39e+04 | — | — | 2026-09-27T09:19:16.285 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 8 | Float64 | 180×90×50 | 10962.81 | +1.1% | 0.09 | 7.39e+04 | — | — | 2026-09-27T09:19:16.376 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 9 | Float64 | 180×90×50 | 10962.34 | +1.2% | 0.09 | 7.39e+04 | — | — | 2026-09-27T09:19:16.487 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 10 | Float64 | 180×90×50 | 10962.51 | +1.2% | 0.09 | 7.39e+04 | — | — | 2026-09-27T09:19:16.445 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 11 | Float64 | 180×90×50 | 10962.82 | +1.1% | 0.09 | 7.39e+04 | — | — | 2026-09-27T09:19:16.225 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 12 | Float64 | 180×90×50 | 10964.63 | +1.2% | 0.09 | 7.39e+04 | — | — | 2026-09-27T09:19:15.789 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 13 | Float64 | 180×90×50 | 10962.69 | +1.2% | 0.09 | 7.39e+04 | — | — | 2026-09-27T09:19:15.961 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 14 | Float64 | 180×90×50 | 10962.76 | +1.1% | 0.09 | 7.39e+04 | — | — | 2026-09-27T09:19:15.841 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 15 | Float64 | 180×90×50 | 10963.08 | +1.1% | 0.09 | 7.39e+04 | — | — | 2026-09-27T09:19:15.794 |
