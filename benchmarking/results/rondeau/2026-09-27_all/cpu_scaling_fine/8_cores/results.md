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
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 360×90×50 | 18388.78 | +0.3% | 0.05 | 8.81e+04 | — | — | 2026-09-27T08:53:26.823 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 360×90×50 | 18389.40 | +0.3% | 0.05 | 8.81e+04 | — | — | 2026-09-27T08:53:27.001 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 360×90×50 | 18389.26 | +0.3% | 0.05 | 8.81e+04 | — | — | 2026-09-27T08:53:26.899 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 360×90×50 | 18389.98 | +0.3% | 0.05 | 8.81e+04 | — | — | 2026-09-27T08:53:26.149 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 4 | Float64 | 360×90×50 | 18389.29 | +0.3% | 0.05 | 8.81e+04 | — | — | 2026-09-27T08:53:26.813 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 5 | Float64 | 360×90×50 | 18389.61 | +0.3% | 0.05 | 8.81e+04 | — | — | 2026-09-27T08:53:26.955 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 6 | Float64 | 360×90×50 | 18389.14 | +0.3% | 0.05 | 8.81e+04 | — | — | 2026-09-27T08:53:26.804 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 7 | Float64 | 360×90×50 | 18389.63 | +0.3% | 0.05 | 8.81e+04 | — | — | 2026-09-27T08:53:26.128 |
