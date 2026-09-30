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
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 90×45×50 | 3749.63 | +7.1% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.001 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 90×45×50 | 3749.32 | +7.1% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.090 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 90×45×50 | 3749.20 | +7.1% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.091 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 90×45×50 | 3771.09 | +5.9% | 0.27 | 5.37e+04 | — | — | 2026-09-27T20:49:12.063 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 4 | Float64 | 90×45×50 | 3775.40 | +5.8% | 0.26 | 5.36e+04 | — | — | 2026-09-27T20:49:11.978 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 5 | Float64 | 90×45×50 | 3775.21 | +5.8% | 0.26 | 5.36e+04 | — | — | 2026-09-27T20:49:11.901 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 6 | Float64 | 90×45×50 | 3775.62 | +6.6% | 0.26 | 5.36e+04 | — | — | 2026-09-27T20:49:11.661 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 7 | Float64 | 90×45×50 | 3782.62 | +6.3% | 0.26 | 5.35e+04 | — | — | 2026-09-27T20:49:11.546 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 8 | Float64 | 90×45×50 | 3749.37 | +7.1% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:11.980 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 9 | Float64 | 90×45×50 | 3749.20 | +7.2% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.083 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 10 | Float64 | 90×45×50 | 3755.24 | +6.9% | 0.27 | 5.39e+04 | — | — | 2026-09-27T20:49:12.063 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 11 | Float64 | 90×45×50 | 3751.70 | +7.3% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.082 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 12 | Float64 | 90×45×50 | 3751.73 | +7.3% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.110 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 13 | Float64 | 90×45×50 | 3750.12 | +7.3% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.045 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 14 | Float64 | 90×45×50 | 3755.08 | +7.3% | 0.27 | 5.39e+04 | — | — | 2026-09-27T20:49:11.978 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 15 | Float64 | 90×45×50 | 3754.93 | +7.3% | 0.27 | 5.39e+04 | — | — | 2026-09-27T20:49:11.797 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 16 | Float64 | 90×45×50 | 3750.67 | +7.0% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.024 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 17 | Float64 | 90×45×50 | 3750.67 | +7.1% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.116 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 18 | Float64 | 90×45×50 | 3755.41 | +7.0% | 0.27 | 5.39e+04 | — | — | 2026-09-27T20:49:12.118 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 19 | Float64 | 90×45×50 | 3751.49 | +7.3% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.131 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 20 | Float64 | 90×45×50 | 3753.98 | +7.2% | 0.27 | 5.39e+04 | — | — | 2026-09-27T20:49:12.141 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 21 | Float64 | 90×45×50 | 3750.02 | +7.4% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.132 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 22 | Float64 | 90×45×50 | 3754.98 | +7.3% | 0.27 | 5.39e+04 | — | — | 2026-09-27T20:49:12.063 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 23 | Float64 | 90×45×50 | 3754.87 | +7.3% | 0.27 | 5.39e+04 | — | — | 2026-09-27T20:49:11.796 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 24 | Float64 | 90×45×50 | 3750.58 | +7.1% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.025 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 25 | Float64 | 90×45×50 | 3750.64 | +7.1% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.121 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 26 | Float64 | 90×45×50 | 3755.30 | +6.9% | 0.27 | 5.39e+04 | — | — | 2026-09-27T20:49:12.137 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 27 | Float64 | 90×45×50 | 3751.53 | +7.6% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.137 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 28 | Float64 | 90×45×50 | 3751.46 | +7.5% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.137 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 29 | Float64 | 90×45×50 | 3750.20 | +7.6% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.088 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 30 | Float64 | 90×45×50 | 3755.12 | +7.3% | 0.27 | 5.39e+04 | — | — | 2026-09-27T20:49:12.022 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 31 | Float64 | 90×45×50 | 3754.94 | +7.3% | 0.27 | 5.39e+04 | — | — | 2026-09-27T20:49:11.782 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 32 | Float64 | 90×45×50 | 3750.70 | +7.0% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.015 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 33 | Float64 | 90×45×50 | 3750.70 | +7.0% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.088 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 34 | Float64 | 90×45×50 | 3750.75 | +7.2% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.097 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 35 | Float64 | 90×45×50 | 3756.37 | +7.2% | 0.27 | 5.39e+04 | — | — | 2026-09-27T20:49:12.178 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 36 | Float64 | 90×45×50 | 3756.30 | +7.2% | 0.27 | 5.39e+04 | — | — | 2026-09-27T20:49:12.178 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 37 | Float64 | 90×45×50 | 3755.15 | +7.3% | 0.27 | 5.39e+04 | — | — | 2026-09-27T20:49:12.135 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 38 | Float64 | 90×45×50 | 3757.64 | +7.2% | 0.27 | 5.39e+04 | — | — | 2026-09-27T20:49:11.917 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 39 | Float64 | 90×45×50 | 3758.79 | +7.2% | 0.27 | 5.39e+04 | — | — | 2026-09-27T20:49:11.673 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 40 | Float64 | 90×45×50 | 3745.38 | +7.2% | 0.27 | 5.41e+04 | — | — | 2026-09-27T20:49:12.183 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 41 | Float64 | 90×45×50 | 3745.46 | +7.2% | 0.27 | 5.41e+04 | — | — | 2026-09-27T20:49:12.260 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 42 | Float64 | 90×45×50 | 3745.18 | +7.2% | 0.27 | 5.41e+04 | — | — | 2026-09-27T20:49:12.217 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 43 | Float64 | 90×45×50 | 3744.96 | +7.7% | 0.27 | 5.41e+04 | — | — | 2026-09-27T20:49:12.159 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 44 | Float64 | 90×45×50 | 3747.86 | +7.6% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.215 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 45 | Float64 | 90×45×50 | 3748.09 | +7.5% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.219 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 46 | Float64 | 90×45×50 | 3780.94 | +6.3% | 0.26 | 5.36e+04 | — | — | 2026-09-27T20:49:11.982 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 47 | Float64 | 90×45×50 | 3782.13 | +5.9% | 0.26 | 5.35e+04 | — | — | 2026-09-27T20:49:11.684 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 48 | Float64 | 90×45×50 | 3745.51 | +7.3% | 0.27 | 5.41e+04 | — | — | 2026-09-27T20:49:12.196 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 49 | Float64 | 90×45×50 | 3745.49 | +7.3% | 0.27 | 5.41e+04 | — | — | 2026-09-27T20:49:12.291 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 50 | Float64 | 90×45×50 | 3745.51 | +7.3% | 0.27 | 5.41e+04 | — | — | 2026-09-27T20:49:12.253 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 51 | Float64 | 90×45×50 | 3745.19 | +7.3% | 0.27 | 5.41e+04 | — | — | 2026-09-27T20:49:12.176 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 52 | Float64 | 90×45×50 | 3747.87 | +7.3% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.117 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 53 | Float64 | 90×45×50 | 3747.83 | +7.3% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:12.134 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 54 | Float64 | 90×45×50 | 3780.89 | +6.3% | 0.26 | 5.36e+04 | — | — | 2026-09-27T20:49:11.960 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 55 | Float64 | 90×45×50 | 3782.13 | +5.9% | 0.26 | 5.35e+04 | — | — | 2026-09-27T20:49:11.701 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 56 | Float64 | 90×45×50 | 3745.43 | +7.3% | 0.27 | 5.41e+04 | — | — | 2026-09-27T20:49:12.213 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 57 | Float64 | 90×45×50 | 3745.44 | +7.3% | 0.27 | 5.41e+04 | — | — | 2026-09-27T20:49:12.297 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 58 | Float64 | 90×45×50 | 3745.44 | +7.3% | 0.27 | 5.41e+04 | — | — | 2026-09-27T20:49:12.244 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 59 | Float64 | 90×45×50 | 3745.11 | +7.3% | 0.27 | 5.41e+04 | — | — | 2026-09-27T20:49:12.021 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 60 | Float64 | 90×45×50 | 3750.81 | +7.0% | 0.27 | 5.40e+04 | — | — | 2026-09-27T20:49:11.956 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 61 | Float64 | 90×45×50 | 3771.27 | +5.9% | 0.27 | 5.37e+04 | — | — | 2026-09-27T20:49:11.693 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 62 | Float64 | 90×45×50 | 3783.97 | +5.8% | 0.26 | 5.35e+04 | — | — | 2026-09-27T20:49:11.580 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 63 | Float64 | 90×45×50 | 3782.56 | +5.7% | 0.26 | 5.35e+04 | — | — | 2026-09-27T20:49:11.529 |
