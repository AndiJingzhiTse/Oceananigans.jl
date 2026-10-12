# Oceananigans Benchmark Results

## System Information

| Property | Value |
|----------|-------|
| Julia | 1.10.10 |
| Oceananigans | 0.113.0 |
| Architecture | Distributed{CPU, false, Partition{Sizes{NTuple{16, Int64}}, Sizes{NTuple{12, Int64}}, Int64}, Tuple{Int64, Int64, Int64}, Int64, Tuple{Int64, Int64, Int64}, Oceananigans.DistributedComputations.NeighboringRanks{Int64, Int64, Int64, Int64, Int64, Int64, Int64, Int64}, MPI.Comm, Vector{MPI.Request}, Base.RefValue{Int64}, Nothing} |
| CPU | Intel(R) Xeon(R) 6972P (icelake-client) |
| Threads | 1 |
| Hostname | c80.nibi.sharcnet |
| Adapt | 4.7.1 |
| CUDA | 6.1.0 |
| GPUArrays | 11.5.15 |
| GPUCompiler | 1.17.1 |
| KernelAbstractions | 0.9.43 |
| LLVM | 9.13.2 |

## Results

| Benchmark | Distributed | Float | Grid | Time/unit (ms) | Spread | Units/s | Points/s | Size | Chunks | Timestamp |
|-----------|-------------|-------|------|----------------|--------|---------|----------|------|--------|-----------|
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 90×60×200 | 5260.64 | +3.1% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 90×60×200 | 5260.84 | +3.1% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.649 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 90×60×200 | 5261.14 | +3.1% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 90×60×200 | 5261.08 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 4 | Float64 | 90×60×200 | 5260.81 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 5 | Float64 | 90×60×200 | 5260.57 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 6 | Float64 | 90×60×200 | 5260.66 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 7 | Float64 | 90×60×200 | 5260.81 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 8 | Float64 | 90×60×200 | 5261.03 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 9 | Float64 | 90×60×200 | 5261.70 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 10 | Float64 | 90×60×200 | 5261.16 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 11 | Float64 | 90×60×200 | 5261.14 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 12 | Float64 | 90×60×200 | 5260.61 | +3.1% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 13 | Float64 | 90×60×200 | 5260.60 | +3.1% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.646 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 14 | Float64 | 90×60×200 | 5261.09 | +3.1% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 15 | Float64 | 90×60×200 | 5261.09 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 16 | Float64 | 90×60×200 | 5260.80 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 17 | Float64 | 90×60×200 | 5260.97 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 18 | Float64 | 90×60×200 | 5260.75 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 19 | Float64 | 90×60×200 | 5260.86 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 20 | Float64 | 90×60×200 | 5261.14 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 21 | Float64 | 90×60×200 | 5259.34 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 22 | Float64 | 90×60×200 | 5261.18 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 23 | Float64 | 90×60×200 | 5261.20 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 24 | Float64 | 90×60×200 | 5260.83 | +3.1% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 25 | Float64 | 90×60×200 | 5260.97 | +3.0% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.648 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 26 | Float64 | 90×60×200 | 5260.46 | +3.1% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 27 | Float64 | 90×60×200 | 5260.83 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 28 | Float64 | 90×60×200 | 5261.00 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 29 | Float64 | 90×60×200 | 5261.16 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 30 | Float64 | 90×60×200 | 5260.95 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 31 | Float64 | 90×60×200 | 5260.85 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 32 | Float64 | 90×60×200 | 5261.14 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 33 | Float64 | 90×60×200 | 5261.31 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 34 | Float64 | 90×60×200 | 5260.55 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 35 | Float64 | 90×60×200 | 5260.06 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 36 | Float64 | 90×60×200 | 5260.90 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 37 | Float64 | 90×60×200 | 5260.66 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.646 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 38 | Float64 | 90×60×200 | 5261.26 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 39 | Float64 | 90×60×200 | 5261.09 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 40 | Float64 | 90×60×200 | 5260.94 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 41 | Float64 | 90×60×200 | 5261.27 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 42 | Float64 | 90×60×200 | 5261.17 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 43 | Float64 | 90×60×200 | 5260.71 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 44 | Float64 | 90×60×200 | 5261.41 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 45 | Float64 | 90×60×200 | 5263.06 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 46 | Float64 | 90×60×200 | 5260.50 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 47 | Float64 | 90×60×200 | 5260.63 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 48 | Float64 | 90×60×200 | 5260.76 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 49 | Float64 | 90×60×200 | 5261.05 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.646 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 50 | Float64 | 90×60×200 | 5261.30 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 51 | Float64 | 90×60×200 | 5260.86 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 52 | Float64 | 90×60×200 | 5261.29 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 53 | Float64 | 90×60×200 | 5261.60 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 54 | Float64 | 90×60×200 | 5262.26 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 55 | Float64 | 90×60×200 | 5260.58 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 56 | Float64 | 90×60×200 | 5260.60 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 57 | Float64 | 90×60×200 | 5264.86 | +2.8% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 58 | Float64 | 90×60×200 | 5259.86 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 59 | Float64 | 90×60×200 | 5260.17 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 60 | Float64 | 90×60×200 | 5260.57 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 61 | Float64 | 90×60×200 | 5260.58 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 62 | Float64 | 90×60×200 | 5261.08 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 63 | Float64 | 90×60×200 | 5260.77 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 64 | Float64 | 90×60×200 | 5261.62 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 65 | Float64 | 90×60×200 | 5261.37 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 66 | Float64 | 90×60×200 | 5262.36 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 67 | Float64 | 90×60×200 | 5261.34 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 68 | Float64 | 90×60×200 | 5260.19 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 69 | Float64 | 90×60×200 | 5261.04 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 70 | Float64 | 90×60×200 | 5260.65 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 71 | Float64 | 90×60×200 | 5260.44 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 72 | Float64 | 90×60×200 | 5261.24 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 73 | Float64 | 90×60×200 | 5260.95 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 74 | Float64 | 90×60×200 | 5261.13 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 75 | Float64 | 90×60×200 | 5260.59 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 76 | Float64 | 90×60×200 | 5261.38 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 77 | Float64 | 90×60×200 | 5261.63 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 78 | Float64 | 90×60×200 | 5261.88 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 79 | Float64 | 90×60×200 | 5260.59 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 80 | Float64 | 90×60×200 | 5260.29 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 81 | Float64 | 90×60×200 | 5261.37 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 82 | Float64 | 90×60×200 | 5260.62 | +2.3% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 83 | Float64 | 90×60×200 | 5260.52 | +2.3% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 84 | Float64 | 90×60×200 | 5260.97 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 85 | Float64 | 90×60×200 | 5261.09 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.644 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 86 | Float64 | 90×60×200 | 5261.22 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 87 | Float64 | 90×60×200 | 5260.25 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 88 | Float64 | 90×60×200 | 5260.52 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 89 | Float64 | 90×60×200 | 5260.82 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 90 | Float64 | 90×60×200 | 5261.35 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 91 | Float64 | 90×60×200 | 5260.46 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 92 | Float64 | 90×60×200 | 5260.64 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 93 | Float64 | 90×60×200 | 5260.93 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 94 | Float64 | 90×60×200 | 5260.92 | +2.3% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 95 | Float64 | 90×60×200 | 5261.14 | +2.3% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 96 | Float64 | 90×60×200 | 5261.17 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 97 | Float64 | 90×60×200 | 5261.13 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 98 | Float64 | 90×60×200 | 5260.87 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 99 | Float64 | 90×60×200 | 5260.84 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 100 | Float64 | 90×60×200 | 5260.54 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 101 | Float64 | 90×60×200 | 5260.85 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 102 | Float64 | 90×60×200 | 5260.85 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 103 | Float64 | 90×60×200 | 5260.83 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 104 | Float64 | 90×60×200 | 5260.70 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 105 | Float64 | 90×60×200 | 5260.61 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 106 | Float64 | 90×60×200 | 5260.55 | +2.3% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 107 | Float64 | 90×60×200 | 5260.70 | +2.3% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 108 | Float64 | 90×60×200 | 5260.80 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 109 | Float64 | 90×60×200 | 5260.86 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 110 | Float64 | 90×60×200 | 5261.01 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 111 | Float64 | 90×60×200 | 5260.92 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 112 | Float64 | 90×60×200 | 5261.20 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 113 | Float64 | 90×60×200 | 5261.70 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 114 | Float64 | 90×60×200 | 5262.05 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 115 | Float64 | 90×60×200 | 5261.52 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 116 | Float64 | 90×60×200 | 5261.10 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 117 | Float64 | 90×60×200 | 5261.22 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 118 | Float64 | 90×60×200 | 5260.81 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 119 | Float64 | 90×60×200 | 5261.19 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 120 | Float64 | 90×60×200 | 5260.81 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 121 | Float64 | 90×60×200 | 5260.12 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 122 | Float64 | 90×60×200 | 5260.85 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 123 | Float64 | 90×60×200 | 5260.85 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 124 | Float64 | 90×60×200 | 5261.10 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 125 | Float64 | 90×60×200 | 5261.29 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 126 | Float64 | 90×60×200 | 5261.41 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 127 | Float64 | 90×60×200 | 5261.65 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 128 | Float64 | 90×60×200 | 5261.03 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 129 | Float64 | 90×60×200 | 5260.88 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 130 | Float64 | 90×60×200 | 5261.17 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 131 | Float64 | 90×60×200 | 5261.26 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 132 | Float64 | 90×60×200 | 5260.54 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 133 | Float64 | 90×60×200 | 5260.34 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 134 | Float64 | 90×60×200 | 5260.55 | +3.0% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 135 | Float64 | 90×60×200 | 5260.76 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 136 | Float64 | 90×60×200 | 5260.95 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 137 | Float64 | 90×60×200 | 5261.06 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 138 | Float64 | 90×60×200 | 5260.93 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 139 | Float64 | 90×60×200 | 5261.03 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 140 | Float64 | 90×60×200 | 5260.85 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 141 | Float64 | 90×60×200 | 5260.89 | +3.0% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 142 | Float64 | 90×60×200 | 5263.87 | +2.8% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 143 | Float64 | 90×60×200 | 5264.13 | +2.8% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 144 | Float64 | 90×60×200 | 5260.71 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 145 | Float64 | 90×60×200 | 5260.35 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 146 | Float64 | 90×60×200 | 5260.49 | +3.0% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 147 | Float64 | 90×60×200 | 5260.79 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 148 | Float64 | 90×60×200 | 5260.96 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 149 | Float64 | 90×60×200 | 5260.70 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 150 | Float64 | 90×60×200 | 5259.93 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 151 | Float64 | 90×60×200 | 5260.80 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 152 | Float64 | 90×60×200 | 5260.73 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 153 | Float64 | 90×60×200 | 5260.83 | +3.0% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 154 | Float64 | 90×60×200 | 5264.26 | +2.8% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 155 | Float64 | 90×60×200 | 5264.85 | +2.8% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 156 | Float64 | 90×60×200 | 5260.90 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 157 | Float64 | 90×60×200 | 5260.24 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 158 | Float64 | 90×60×200 | 5260.38 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 159 | Float64 | 90×60×200 | 5260.78 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 160 | Float64 | 90×60×200 | 5261.01 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 161 | Float64 | 90×60×200 | 5260.76 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 162 | Float64 | 90×60×200 | 5260.69 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 163 | Float64 | 90×60×200 | 5260.63 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 164 | Float64 | 90×60×200 | 5260.67 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 165 | Float64 | 90×60×200 | 5260.89 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 166 | Float64 | 90×60×200 | 5263.88 | +2.8% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 167 | Float64 | 90×60×200 | 5264.11 | +2.8% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 168 | Float64 | 90×60×200 | 5260.70 | +3.0% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 169 | Float64 | 90×60×200 | 5261.02 | +3.0% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 170 | Float64 | 90×60×200 | 5260.51 | +3.0% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 171 | Float64 | 90×60×200 | 5260.65 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 172 | Float64 | 90×60×200 | 5260.48 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 173 | Float64 | 90×60×200 | 5260.06 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 174 | Float64 | 90×60×200 | 5260.59 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.641 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 175 | Float64 | 90×60×200 | 5260.48 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 176 | Float64 | 90×60×200 | 5260.69 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 177 | Float64 | 90×60×200 | 5260.69 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 178 | Float64 | 90×60×200 | 5261.15 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 179 | Float64 | 90×60×200 | 5260.73 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 180 | Float64 | 90×60×200 | 5260.82 | +3.1% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 181 | Float64 | 90×60×200 | 5261.23 | +3.0% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 182 | Float64 | 90×60×200 | 5261.35 | +3.1% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 183 | Float64 | 90×60×200 | 5260.56 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 184 | Float64 | 90×60×200 | 5260.90 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 185 | Float64 | 90×60×200 | 5260.56 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 186 | Float64 | 90×60×200 | 5260.75 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 187 | Float64 | 90×60×200 | 5261.08 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 188 | Float64 | 90×60×200 | 5260.92 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 189 | Float64 | 90×60×200 | 5262.15 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 190 | Float64 | 90×60×200 | 5260.87 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 191 | Float64 | 90×60×200 | 5260.98 | +2.9% | 0.19 | 2.05e+05 | — | — | 2026-10-06T18:09:33.642 |

# Benchmark configuration

Global resolution: 1440 × 720 × 200. Grid type: LatitudeLongitudeGrid.
Partition: 16 × 12 × 1.
192 cores; 1 nodes; 192 MPI ranks; 1 pinned Julia threads per rank.
Local resolution: x 90–90, y 60–60, z 200. Remainder cells are distributed evenly; the global grid is preserved.
Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=60 s; two warmup steps, five ten-step windows.
SplitExplicitFreeSurface(substeps=30, extend_halos=false): exchange halos at every substep.
