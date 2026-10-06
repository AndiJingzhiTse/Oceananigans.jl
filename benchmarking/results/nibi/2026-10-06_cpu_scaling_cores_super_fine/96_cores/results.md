# Oceananigans Benchmark Results

## System Information

| Property | Value |
|----------|-------|
| Julia | 1.10.10 |
| Oceananigans | 0.113.0 |
| Architecture | Distributed{CPU, false, Partition{Sizes{NTuple{12, Int64}}, Sizes{NTuple{8, Int64}}, Int64}, Tuple{Int64, Int64, Int64}, Int64, Tuple{Int64, Int64, Int64}, Oceananigans.DistributedComputations.NeighboringRanks{Int64, Int64, Int64, Int64, Int64, Int64, Int64, Int64}, MPI.Comm, Vector{MPI.Request}, Base.RefValue{Int64}, Nothing} |
| CPU | Intel(R) Xeon(R) 6972P (icelake-client) |
| Threads | 1 |
| Hostname | c334.nibi.sharcnet |
| Adapt | 4.7.1 |
| CUDA | 6.1.0 |
| GPUArrays | 11.5.15 |
| GPUCompiler | 1.17.1 |
| KernelAbstractions | 0.9.43 |
| LLVM | 9.13.2 |

## Results

| Benchmark | Distributed | Float | Grid | Time/unit (ms) | Spread | Units/s | Points/s | Size | Chunks | Timestamp |
|-----------|-------------|-------|------|----------------|--------|---------|----------|------|--------|-----------|
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 120×90×200 | 10052.53 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.356 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 120×90×200 | 10052.93 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.406 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 120×90×200 | 10053.08 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.279 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 120×90×200 | 10053.42 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 4 | Float64 | 120×90×200 | 10053.01 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 5 | Float64 | 120×90×200 | 10054.02 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.290 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 6 | Float64 | 120×90×200 | 10051.84 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.393 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 7 | Float64 | 120×90×200 | 10052.45 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.357 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 8 | Float64 | 120×90×200 | 10051.85 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.354 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 9 | Float64 | 120×90×200 | 10052.57 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.403 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 10 | Float64 | 120×90×200 | 10051.77 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.261 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 11 | Float64 | 120×90×200 | 10053.52 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 12 | Float64 | 120×90×200 | 10052.80 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 13 | Float64 | 120×90×200 | 10052.77 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.291 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 14 | Float64 | 120×90×200 | 10051.75 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.401 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 15 | Float64 | 120×90×200 | 10052.31 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.356 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 16 | Float64 | 120×90×200 | 10051.57 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.353 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 17 | Float64 | 120×90×200 | 10051.42 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.390 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 18 | Float64 | 120×90×200 | 10052.09 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.265 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 19 | Float64 | 120×90×200 | 10053.00 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 20 | Float64 | 120×90×200 | 10052.75 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 21 | Float64 | 120×90×200 | 10051.52 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.286 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 22 | Float64 | 120×90×200 | 10053.95 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.417 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 23 | Float64 | 120×90×200 | 10053.30 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.368 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 24 | Float64 | 120×90×200 | 10051.59 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.359 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 25 | Float64 | 120×90×200 | 10051.42 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.394 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 26 | Float64 | 120×90×200 | 10053.22 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.272 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 27 | Float64 | 120×90×200 | 10052.63 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 28 | Float64 | 120×90×200 | 10053.83 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 29 | Float64 | 120×90×200 | 10051.56 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.287 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 30 | Float64 | 120×90×200 | 10051.93 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.405 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 31 | Float64 | 120×90×200 | 10051.45 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.356 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 32 | Float64 | 120×90×200 | 10051.46 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.356 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 33 | Float64 | 120×90×200 | 10051.60 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.398 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 34 | Float64 | 120×90×200 | 10051.87 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.271 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 35 | Float64 | 120×90×200 | 10052.21 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 36 | Float64 | 120×90×200 | 10053.38 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 37 | Float64 | 120×90×200 | 10052.61 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.295 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 38 | Float64 | 120×90×200 | 10053.25 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.415 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 39 | Float64 | 120×90×200 | 10052.55 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.367 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 40 | Float64 | 120×90×200 | 10052.55 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.363 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 41 | Float64 | 120×90×200 | 10052.70 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.411 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 42 | Float64 | 120×90×200 | 10052.94 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.278 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 43 | Float64 | 120×90×200 | 10053.34 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 44 | Float64 | 120×90×200 | 10053.06 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 45 | Float64 | 120×90×200 | 10053.39 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.294 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 46 | Float64 | 120×90×200 | 10050.49 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.405 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 47 | Float64 | 120×90×200 | 10051.65 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.365 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 48 | Float64 | 120×90×200 | 10051.69 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.363 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 49 | Float64 | 120×90×200 | 10051.72 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.394 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 50 | Float64 | 120×90×200 | 10052.58 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.288 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 51 | Float64 | 120×90×200 | 10053.56 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 52 | Float64 | 120×90×200 | 10052.29 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 53 | Float64 | 120×90×200 | 10052.14 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.289 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 54 | Float64 | 120×90×200 | 10052.26 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.407 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 55 | Float64 | 120×90×200 | 10051.48 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.368 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 56 | Float64 | 120×90×200 | 10052.21 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.363 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 57 | Float64 | 120×90×200 | 10053.30 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.409 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 58 | Float64 | 120×90×200 | 10052.17 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.281 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 59 | Float64 | 120×90×200 | 10054.08 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 60 | Float64 | 120×90×200 | 10053.44 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 61 | Float64 | 120×90×200 | 10052.58 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.290 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 62 | Float64 | 120×90×200 | 10052.86 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.416 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 63 | Float64 | 120×90×200 | 10051.74 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.366 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 64 | Float64 | 120×90×200 | 10051.66 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.356 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 65 | Float64 | 120×90×200 | 10051.34 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.409 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 66 | Float64 | 120×90×200 | 10049.82 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.264 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 67 | Float64 | 120×90×200 | 10053.40 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 68 | Float64 | 120×90×200 | 10053.32 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 69 | Float64 | 120×90×200 | 10051.84 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.287 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 70 | Float64 | 120×90×200 | 10051.84 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.404 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 71 | Float64 | 120×90×200 | 10050.87 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.357 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 72 | Float64 | 120×90×200 | 10051.60 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.353 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 73 | Float64 | 120×90×200 | 10050.88 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.403 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 74 | Float64 | 120×90×200 | 10052.31 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.277 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 75 | Float64 | 120×90×200 | 10054.70 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 76 | Float64 | 120×90×200 | 10053.68 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 77 | Float64 | 120×90×200 | 10050.46 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.281 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 78 | Float64 | 120×90×200 | 10052.36 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.396 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 79 | Float64 | 120×90×200 | 10051.41 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.360 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 80 | Float64 | 120×90×200 | 10051.23 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.363 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 81 | Float64 | 120×90×200 | 10052.65 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.408 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 82 | Float64 | 120×90×200 | 10050.52 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.261 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 83 | Float64 | 120×90×200 | 10052.75 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 84 | Float64 | 120×90×200 | 10052.27 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 85 | Float64 | 120×90×200 | 10053.13 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.295 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 86 | Float64 | 120×90×200 | 10052.95 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.402 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 87 | Float64 | 120×90×200 | 10051.76 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.353 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 88 | Float64 | 120×90×200 | 10051.61 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.363 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 89 | Float64 | 120×90×200 | 10051.49 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.398 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 90 | Float64 | 120×90×200 | 10051.06 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.265 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 91 | Float64 | 120×90×200 | 10052.95 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 92 | Float64 | 120×90×200 | 10052.75 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.160 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 93 | Float64 | 120×90×200 | 10052.97 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.259 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 94 | Float64 | 120×90×200 | 10052.20 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.376 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 95 | Float64 | 120×90×200 | 10051.94 | +1.7% | 0.10 | 2.15e+05 | — | — | 2026-10-06T17:32:00.327 |

# Benchmark configuration

Global resolution: 1440 × 720 × 200. Grid type: LatitudeLongitudeGrid.
Partition: 12 × 8 × 1.
96 cores; 1 nodes; 96 MPI ranks; 1 pinned Julia threads per rank.
Local resolution: x 120–120, y 90–90, z 200. Remainder cells are distributed evenly; the global grid is preserved.
Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=60 s; two warmup steps, five ten-step windows.
SplitExplicitFreeSurface(substeps=30, extend_halos=false): exchange halos at every substep.
