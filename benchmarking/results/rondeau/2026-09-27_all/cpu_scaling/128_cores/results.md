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
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 45×45×50 | 2137.08 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.679 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 45×45×50 | 2137.22 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.734 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 45×45×50 | 2137.11 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.730 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 45×45×50 | 2137.28 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.725 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 4 | Float64 | 45×45×50 | 2137.15 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.711 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 5 | Float64 | 45×45×50 | 2136.96 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.561 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 6 | Float64 | 45×45×50 | 2128.80 | +15.6% | 0.47 | 4.76e+04 | — | — | 2026-09-27T21:15:27.317 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 7 | Float64 | 45×45×50 | 2136.14 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.317 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 8 | Float64 | 45×45×50 | 2137.26 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.655 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 9 | Float64 | 45×45×50 | 2137.22 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.728 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 10 | Float64 | 45×45×50 | 2137.23 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.725 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 11 | Float64 | 45×45×50 | 2137.01 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.712 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 12 | Float64 | 45×45×50 | 2137.07 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.679 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 13 | Float64 | 45×45×50 | 2136.72 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.565 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 14 | Float64 | 45×45×50 | 2133.07 | +15.1% | 0.47 | 4.75e+04 | — | — | 2026-09-27T21:15:27.377 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 15 | Float64 | 45×45×50 | 2130.78 | +15.4% | 0.47 | 4.75e+04 | — | — | 2026-09-27T21:15:27.356 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 16 | Float64 | 45×45×50 | 2137.23 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.658 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 17 | Float64 | 45×45×50 | 2137.29 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.739 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 18 | Float64 | 45×45×50 | 2137.32 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.659 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 19 | Float64 | 45×45×50 | 2137.13 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.665 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 20 | Float64 | 45×45×50 | 2137.27 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.703 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 21 | Float64 | 45×45×50 | 2137.23 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.666 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 22 | Float64 | 45×45×50 | 2137.37 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.591 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 23 | Float64 | 45×45×50 | 2136.60 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.542 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 24 | Float64 | 45×45×50 | 2137.35 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.658 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 25 | Float64 | 45×45×50 | 2137.31 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.727 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 26 | Float64 | 45×45×50 | 2137.35 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.674 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 27 | Float64 | 45×45×50 | 2137.08 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.705 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 28 | Float64 | 45×45×50 | 2136.97 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.767 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 29 | Float64 | 45×45×50 | 2137.02 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.727 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 30 | Float64 | 45×45×50 | 2137.42 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.636 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 31 | Float64 | 45×45×50 | 2136.60 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.574 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 32 | Float64 | 45×45×50 | 2137.26 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.663 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 33 | Float64 | 45×45×50 | 2137.04 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.736 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 34 | Float64 | 45×45×50 | 2136.89 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.736 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 35 | Float64 | 45×45×50 | 2136.84 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.752 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 36 | Float64 | 45×45×50 | 2136.71 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.760 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 37 | Float64 | 45×45×50 | 2137.20 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.752 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 38 | Float64 | 45×45×50 | 2137.25 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.689 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 39 | Float64 | 45×45×50 | 2137.24 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.621 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 40 | Float64 | 45×45×50 | 2137.24 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.692 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 41 | Float64 | 45×45×50 | 2137.08 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.750 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 42 | Float64 | 45×45×50 | 2136.81 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.761 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 43 | Float64 | 45×45×50 | 2136.70 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.762 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 44 | Float64 | 45×45×50 | 2136.82 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.759 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 45 | Float64 | 45×45×50 | 2137.16 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.752 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 46 | Float64 | 45×45×50 | 2137.36 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.734 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 47 | Float64 | 45×45×50 | 2137.17 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.589 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 48 | Float64 | 45×45×50 | 2137.29 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.691 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 49 | Float64 | 45×45×50 | 2137.09 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.750 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 50 | Float64 | 45×45×50 | 2136.85 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.759 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 51 | Float64 | 45×45×50 | 2136.82 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.761 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 52 | Float64 | 45×45×50 | 2136.78 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.759 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 53 | Float64 | 45×45×50 | 2137.13 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.751 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 54 | Float64 | 45×45×50 | 2137.21 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.718 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 55 | Float64 | 45×45×50 | 2137.20 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.583 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 56 | Float64 | 45×45×50 | 2139.39 | +14.4% | 0.47 | 4.73e+04 | — | — | 2026-09-27T21:15:27.766 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 57 | Float64 | 45×45×50 | 2139.54 | +14.4% | 0.47 | 4.73e+04 | — | — | 2026-09-27T21:15:27.827 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 58 | Float64 | 45×45×50 | 2139.36 | +14.4% | 0.47 | 4.73e+04 | — | — | 2026-09-27T21:15:27.848 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 59 | Float64 | 45×45×50 | 2139.53 | +14.4% | 0.47 | 4.73e+04 | — | — | 2026-09-27T21:15:27.851 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 60 | Float64 | 45×45×50 | 2136.88 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.765 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 61 | Float64 | 45×45×50 | 2137.12 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.707 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 62 | Float64 | 45×45×50 | 2137.03 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.658 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 63 | Float64 | 45×45×50 | 2137.15 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.584 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 64 | Float64 | 45×45×50 | 2139.99 | +14.4% | 0.47 | 4.73e+04 | — | — | 2026-09-27T21:15:27.767 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 65 | Float64 | 45×45×50 | 2139.61 | +14.4% | 0.47 | 4.73e+04 | — | — | 2026-09-27T21:15:27.827 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 66 | Float64 | 45×45×50 | 2139.79 | +14.4% | 0.47 | 4.73e+04 | — | — | 2026-09-27T21:15:27.823 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 67 | Float64 | 45×45×50 | 2139.62 | +14.4% | 0.47 | 4.73e+04 | — | — | 2026-09-27T21:15:27.822 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 68 | Float64 | 45×45×50 | 2137.20 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.710 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 69 | Float64 | 45×45×50 | 2137.19 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.657 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 70 | Float64 | 45×45×50 | 2137.63 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.555 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 71 | Float64 | 45×45×50 | 2137.32 | +13.9% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.355 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 72 | Float64 | 45×45×50 | 2140.00 | +14.4% | 0.47 | 4.73e+04 | — | — | 2026-09-27T21:15:27.757 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 73 | Float64 | 45×45×50 | 2139.62 | +14.4% | 0.47 | 4.73e+04 | — | — | 2026-09-27T21:15:27.816 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 74 | Float64 | 45×45×50 | 2139.49 | +14.4% | 0.47 | 4.73e+04 | — | — | 2026-09-27T21:15:27.782 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 75 | Float64 | 45×45×50 | 2139.17 | +14.5% | 0.47 | 4.73e+04 | — | — | 2026-09-27T21:15:27.766 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 76 | Float64 | 45×45×50 | 2136.46 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.686 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 77 | Float64 | 45×45×50 | 2136.57 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.673 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 78 | Float64 | 45×45×50 | 2136.46 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.628 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 79 | Float64 | 45×45×50 | 2136.52 | +13.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.396 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 80 | Float64 | 45×45×50 | 2141.80 | +14.3% | 0.47 | 4.73e+04 | — | — | 2026-09-27T21:15:27.704 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 81 | Float64 | 45×45×50 | 2141.69 | +14.3% | 0.47 | 4.73e+04 | — | — | 2026-09-27T21:15:27.767 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 82 | Float64 | 45×45×50 | 2141.77 | +14.3% | 0.47 | 4.73e+04 | — | — | 2026-09-27T21:15:27.693 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 83 | Float64 | 45×45×50 | 2136.35 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.668 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 84 | Float64 | 45×45×50 | 2136.40 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.741 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 85 | Float64 | 45×45×50 | 2136.29 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.757 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 86 | Float64 | 45×45×50 | 2136.55 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.674 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 87 | Float64 | 45×45×50 | 2136.39 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.591 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 88 | Float64 | 45×45×50 | 2141.67 | +14.3% | 0.47 | 4.73e+04 | — | — | 2026-09-27T21:15:27.737 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 89 | Float64 | 45×45×50 | 2140.62 | +14.3% | 0.47 | 4.73e+04 | — | — | 2026-09-27T21:15:27.770 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 90 | Float64 | 45×45×50 | 2140.73 | +14.3% | 0.47 | 4.73e+04 | — | — | 2026-09-27T21:15:27.760 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 91 | Float64 | 45×45×50 | 2136.25 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.745 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 92 | Float64 | 45×45×50 | 2136.10 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.771 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 93 | Float64 | 45×45×50 | 2136.17 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.773 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 94 | Float64 | 45×45×50 | 2136.58 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.708 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 95 | Float64 | 45×45×50 | 2136.28 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.613 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 96 | Float64 | 45×45×50 | 2136.34 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.708 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 97 | Float64 | 45×45×50 | 2136.16 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.755 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 98 | Float64 | 45×45×50 | 2136.11 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.757 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 99 | Float64 | 45×45×50 | 2136.11 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.770 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 100 | Float64 | 45×45×50 | 2136.34 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.701 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 101 | Float64 | 45×45×50 | 2136.23 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.740 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 102 | Float64 | 45×45×50 | 2136.49 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.675 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 103 | Float64 | 45×45×50 | 2136.34 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.635 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 104 | Float64 | 45×45×50 | 2136.45 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.693 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 105 | Float64 | 45×45×50 | 2136.20 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.758 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 106 | Float64 | 45×45×50 | 2136.42 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.714 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 107 | Float64 | 45×45×50 | 2136.89 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.670 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 108 | Float64 | 45×45×50 | 2136.51 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.622 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 109 | Float64 | 45×45×50 | 2136.69 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.504 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 110 | Float64 | 45×45×50 | 2136.61 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.541 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 111 | Float64 | 45×45×50 | 2136.61 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.544 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 112 | Float64 | 45×45×50 | 2136.56 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.696 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 113 | Float64 | 45×45×50 | 2136.40 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.754 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 114 | Float64 | 45×45×50 | 2136.43 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.696 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 115 | Float64 | 45×45×50 | 2136.94 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.646 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 116 | Float64 | 45×45×50 | 2136.88 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.617 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 117 | Float64 | 45×45×50 | 2137.04 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.566 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 118 | Float64 | 45×45×50 | 2136.86 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.390 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 119 | Float64 | 45×45×50 | 2137.02 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.354 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 120 | Float64 | 45×45×50 | 2137.02 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.664 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 121 | Float64 | 45×45×50 | 2136.92 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.732 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 122 | Float64 | 45×45×50 | 2136.94 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.731 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 123 | Float64 | 45×45×50 | 2136.96 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.713 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 124 | Float64 | 45×45×50 | 2137.24 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.696 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 125 | Float64 | 45×45×50 | 2137.01 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.572 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 126 | Float64 | 45×45×50 | 2135.99 | +14.6% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.321 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 127 | Float64 | 45×45×50 | 2137.64 | +14.5% | 0.47 | 4.74e+04 | — | — | 2026-09-27T21:15:27.300 |
