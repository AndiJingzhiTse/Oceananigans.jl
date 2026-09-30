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
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 45×22×50 | 1181.27 | +19.2% | 0.85 | 4.19e+04 | — | — | 2026-09-30T04:15:03.875 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 45×22×50 | 1181.51 | +19.1% | 0.85 | 4.19e+04 | — | — | 2026-09-30T04:15:03.927 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 45×22×50 | 1181.25 | +19.1% | 0.85 | 4.19e+04 | — | — | 2026-09-30T04:15:03.923 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 45×22×50 | 1193.21 | +16.9% | 0.84 | 4.15e+04 | — | — | 2026-09-30T04:15:03.920 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 4 | Float64 | 45×22×50 | 1196.54 | +16.3% | 0.84 | 4.14e+04 | — | — | 2026-09-30T04:15:03.904 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 5 | Float64 | 45×22×50 | 1197.09 | +16.2% | 0.84 | 4.14e+04 | — | — | 2026-09-30T04:15:03.843 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 6 | Float64 | 45×22×50 | 1222.56 | +9.6% | 0.82 | 4.05e+04 | — | — | 2026-09-30T04:15:03.798 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 7 | Float64 | 45×26×50 | 1221.53 | +9.5% | 0.82 | 4.79e+04 | — | — | 2026-09-30T04:15:03.798 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 8 | Float64 | 45×22×50 | 1181.29 | +19.1% | 0.85 | 4.19e+04 | — | — | 2026-09-30T04:15:03.881 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 9 | Float64 | 45×22×50 | 1181.44 | +19.1% | 0.85 | 4.19e+04 | — | — | 2026-09-30T04:15:03.936 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 10 | Float64 | 45×22×50 | 1181.49 | +19.0% | 0.85 | 4.19e+04 | — | — | 2026-09-30T04:15:03.892 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 11 | Float64 | 45×22×50 | 1197.38 | +16.1% | 0.84 | 4.13e+04 | — | — | 2026-09-30T04:15:03.908 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 12 | Float64 | 45×22×50 | 1200.23 | +15.9% | 0.83 | 4.12e+04 | — | — | 2026-09-30T04:15:03.930 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 13 | Float64 | 45×22×50 | 1200.94 | +15.7% | 0.83 | 4.12e+04 | — | — | 2026-09-30T04:15:03.920 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 14 | Float64 | 45×22×50 | 1222.47 | +10.3% | 0.82 | 4.05e+04 | — | — | 2026-09-30T04:15:03.873 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 15 | Float64 | 45×26×50 | 1222.57 | +9.8% | 0.82 | 4.78e+04 | — | — | 2026-09-30T04:15:03.849 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 16 | Float64 | 45×22×50 | 1197.84 | +17.4% | 0.83 | 4.13e+04 | — | — | 2026-09-30T04:15:03.895 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 17 | Float64 | 45×22×50 | 1197.63 | +17.4% | 0.83 | 4.13e+04 | — | — | 2026-09-30T04:15:03.937 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 18 | Float64 | 45×22×50 | 1197.65 | +17.4% | 0.83 | 4.13e+04 | — | — | 2026-09-30T04:15:03.934 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 19 | Float64 | 45×22×50 | 1197.54 | +16.1% | 0.84 | 4.13e+04 | — | — | 2026-09-30T04:15:03.934 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 20 | Float64 | 45×22×50 | 1200.24 | +15.8% | 0.83 | 4.12e+04 | — | — | 2026-09-30T04:15:03.938 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 21 | Float64 | 45×22×50 | 1199.04 | +16.1% | 0.83 | 4.13e+04 | — | — | 2026-09-30T04:15:03.938 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 22 | Float64 | 45×22×50 | 1222.33 | +10.3% | 0.82 | 4.05e+04 | — | — | 2026-09-30T04:15:03.919 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 23 | Float64 | 45×26×50 | 1222.56 | +10.6% | 0.82 | 4.79e+04 | — | — | 2026-09-30T04:15:03.860 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 24 | Float64 | 45×22×50 | 1213.47 | +14.6% | 0.82 | 4.08e+04 | — | — | 2026-09-30T04:15:03.894 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 25 | Float64 | 45×22×50 | 1213.40 | +14.6% | 0.82 | 4.08e+04 | — | — | 2026-09-30T04:15:03.941 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 26 | Float64 | 45×22×50 | 1213.50 | +14.6% | 0.82 | 4.08e+04 | — | — | 2026-09-30T04:15:03.941 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 27 | Float64 | 45×22×50 | 1197.47 | +16.1% | 0.84 | 4.13e+04 | — | — | 2026-09-30T04:15:03.958 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 28 | Float64 | 45×22×50 | 1200.16 | +15.8% | 0.83 | 4.12e+04 | — | — | 2026-09-30T04:15:03.941 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 29 | Float64 | 45×22×50 | 1200.33 | +15.8% | 0.83 | 4.12e+04 | — | — | 2026-09-30T04:15:03.926 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 30 | Float64 | 45×22×50 | 1222.28 | +10.3% | 0.82 | 4.05e+04 | — | — | 2026-09-30T04:15:03.898 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 31 | Float64 | 45×26×50 | 1222.58 | +10.6% | 0.82 | 4.78e+04 | — | — | 2026-09-30T04:15:03.840 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 32 | Float64 | 45×22×50 | 1213.39 | +14.6% | 0.82 | 4.08e+04 | — | — | 2026-09-30T04:15:03.888 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 33 | Float64 | 45×22×50 | 1213.52 | +14.6% | 0.82 | 4.08e+04 | — | — | 2026-09-30T04:15:03.922 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 34 | Float64 | 45×22×50 | 1213.52 | +14.6% | 0.82 | 4.08e+04 | — | — | 2026-09-30T04:15:03.923 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 35 | Float64 | 45×22×50 | 1196.98 | +16.2% | 0.84 | 4.14e+04 | — | — | 2026-09-30T04:15:03.914 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 36 | Float64 | 45×22×50 | 1197.02 | +16.2% | 0.84 | 4.14e+04 | — | — | 2026-09-30T04:15:03.908 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 37 | Float64 | 45×22×50 | 1196.79 | +16.2% | 0.84 | 4.14e+04 | — | — | 2026-09-30T04:15:03.888 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 38 | Float64 | 45×22×50 | 1222.77 | +10.2% | 0.82 | 4.05e+04 | — | — | 2026-09-30T04:15:03.857 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 39 | Float64 | 45×26×50 | 1222.39 | +10.6% | 0.82 | 4.79e+04 | — | — | 2026-09-30T04:15:03.794 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 40 | Float64 | 45×22×50 | 1197.28 | +16.2% | 0.84 | 4.13e+04 | — | — | 2026-09-30T04:15:03.884 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 41 | Float64 | 45×22×50 | 1197.44 | +16.1% | 0.84 | 4.13e+04 | — | — | 2026-09-30T04:15:03.922 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 42 | Float64 | 45×22×50 | 1197.25 | +16.2% | 0.84 | 4.13e+04 | — | — | 2026-09-30T04:15:03.897 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 43 | Float64 | 45×22×50 | 1197.41 | +16.1% | 0.84 | 4.13e+04 | — | — | 2026-09-30T04:15:03.872 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 44 | Float64 | 45×22×50 | 1197.90 | +15.9% | 0.83 | 4.13e+04 | — | — | 2026-09-30T04:15:03.922 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 45 | Float64 | 45×22×50 | 1197.93 | +15.9% | 0.83 | 4.13e+04 | — | — | 2026-09-30T04:15:03.941 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 46 | Float64 | 45×22×50 | 1222.75 | +10.2% | 0.82 | 4.05e+04 | — | — | 2026-09-30T04:15:03.894 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 47 | Float64 | 45×26×50 | 1222.68 | +10.0% | 0.82 | 4.78e+04 | — | — | 2026-09-30T04:15:03.809 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 48 | Float64 | 45×22×50 | 1197.30 | +16.2% | 0.84 | 4.13e+04 | — | — | 2026-09-30T04:15:03.886 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 49 | Float64 | 45×22×50 | 1194.20 | +16.7% | 0.84 | 4.15e+04 | — | — | 2026-09-30T04:15:03.941 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 50 | Float64 | 45×22×50 | 1194.23 | +16.7% | 0.84 | 4.14e+04 | — | — | 2026-09-30T04:15:03.922 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 51 | Float64 | 45×22×50 | 1191.55 | +17.2% | 0.84 | 4.15e+04 | — | — | 2026-09-30T04:15:03.881 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 52 | Float64 | 45×22×50 | 1197.87 | +15.9% | 0.83 | 4.13e+04 | — | — | 2026-09-30T04:15:03.874 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 53 | Float64 | 45×22×50 | 1197.91 | +15.9% | 0.83 | 4.13e+04 | — | — | 2026-09-30T04:15:03.909 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 54 | Float64 | 45×22×50 | 1222.75 | +10.0% | 0.82 | 4.05e+04 | — | — | 2026-09-30T04:15:03.876 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 55 | Float64 | 45×26×50 | 1222.63 | +9.5% | 0.82 | 4.78e+04 | — | — | 2026-09-30T04:15:03.819 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 56 | Float64 | 45×22×50 | 1197.29 | +16.2% | 0.84 | 4.13e+04 | — | — | 2026-09-30T04:15:03.886 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 57 | Float64 | 45×22×50 | 1194.08 | +16.7% | 0.84 | 4.15e+04 | — | — | 2026-09-30T04:15:03.936 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 58 | Float64 | 45×22×50 | 1194.16 | +16.7% | 0.84 | 4.15e+04 | — | — | 2026-09-30T04:15:03.913 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 59 | Float64 | 45×22×50 | 1193.44 | +16.8% | 0.84 | 4.15e+04 | — | — | 2026-09-30T04:15:03.897 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 60 | Float64 | 45×22×50 | 1196.49 | +16.3% | 0.84 | 4.14e+04 | — | — | 2026-09-30T04:15:03.903 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 61 | Float64 | 45×22×50 | 1197.17 | +16.2% | 0.84 | 4.13e+04 | — | — | 2026-09-30T04:15:03.812 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 62 | Float64 | 45×22×50 | 1221.50 | +9.6% | 0.82 | 4.05e+04 | — | — | 2026-09-30T04:15:03.795 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 63 | Float64 | 45×26×50 | 1221.48 | +9.6% | 0.82 | 4.79e+04 | — | — | 2026-09-30T04:15:03.780 |
