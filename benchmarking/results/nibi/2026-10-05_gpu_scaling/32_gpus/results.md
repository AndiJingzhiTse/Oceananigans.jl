# Oceananigans Benchmark Results

## System Information

| Property | Value |
|----------|-------|
| Julia | 1.10.10 |
| Oceananigans | 0.113.0 |
| Architecture | Distributed{GPU{CUDABackend}, false, Partition{Int64, Int64, Int64}, Tuple{Int64, Int64, Int64}, Int64, Tuple{Int64, Int64, Int64}, Oceananigans.DistributedComputations.NeighboringRanks{Int64, Int64, Int64, Int64, Int64, Int64, Int64, Int64}, MPI.Comm, Vector{MPI.Request}, Base.RefValue{Int64}, Nothing} |
| CPU | INTEL(R) XEON(R) PLATINUM 8570 (icelake-client) |
| Threads | 1 |
| Hostname | g18.nibi.sharcnet |
| Adapt | 4.7.1 |
| CUDA | 6.1.0 |
| GPUArrays | 11.5.15 |
| GPUCompiler | 1.17.1 |
| KernelAbstractions | 0.9.43 |
| LLVM | 9.13.2 |

## Results

| Benchmark | Distributed | Float | Grid | Time/unit (ms) | Spread | Units/s | Points/s | Size | Chunks | Timestamp |
|-----------|-------------|-------|------|----------------|--------|---------|----------|------|--------|-----------|
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 180×180×200 | 98.32 | +289.9% | 10.17 | 6.59e+07 | — | — | 2026-10-05T04:49:01.478 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 180×180×200 | 98.17 | +292.9% | 10.19 | 6.60e+07 | — | — | 2026-10-05T04:49:01.478 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 180×180×200 | 98.02 | +290.5% | 10.20 | 6.61e+07 | — | — | 2026-10-05T04:49:01.478 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 180×180×200 | 98.16 | +289.9% | 10.19 | 6.60e+07 | — | — | 2026-10-05T04:49:01.478 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 4 | Float64 | 180×180×200 | 98.14 | +290.0% | 10.19 | 6.60e+07 | — | — | 2026-10-05T04:49:01.478 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 5 | Float64 | 180×180×200 | 98.09 | +294.3% | 10.19 | 6.61e+07 | — | — | 2026-10-05T04:49:01.478 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 6 | Float64 | 180×180×200 | 98.10 | +290.5% | 10.19 | 6.61e+07 | — | — | 2026-10-05T04:49:01.478 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 7 | Float64 | 180×180×200 | 97.99 | +290.6% | 10.21 | 6.61e+07 | — | — | 2026-10-05T04:49:01.478 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 8 | Float64 | 180×180×200 | 98.11 | +256.7% | 10.19 | 6.60e+07 | — | — | 2026-10-05T04:49:01.467 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 9 | Float64 | 180×180×200 | 98.00 | +262.1% | 10.20 | 6.61e+07 | — | — | 2026-10-05T04:49:01.467 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 10 | Float64 | 180×180×200 | 97.70 | +263.2% | 10.24 | 6.63e+07 | — | — | 2026-10-05T04:49:01.467 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 11 | Float64 | 180×180×200 | 97.57 | +264.0% | 10.25 | 6.64e+07 | — | — | 2026-10-05T04:49:01.467 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 12 | Float64 | 180×180×200 | 98.33 | +255.9% | 10.17 | 6.59e+07 | — | — | 2026-10-05T04:49:01.467 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 13 | Float64 | 180×180×200 | 97.72 | +261.9% | 10.23 | 6.63e+07 | — | — | 2026-10-05T04:49:01.467 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 14 | Float64 | 180×180×200 | 97.67 | +263.0% | 10.24 | 6.63e+07 | — | — | 2026-10-05T04:49:01.467 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 15 | Float64 | 180×180×200 | 97.52 | +263.6% | 10.25 | 6.64e+07 | — | — | 2026-10-05T04:49:01.467 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 16 | Float64 | 180×180×200 | 98.17 | +252.9% | 10.19 | 6.60e+07 | — | — | 2026-10-05T04:49:01.475 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 17 | Float64 | 180×180×200 | 97.58 | +254.6% | 10.25 | 6.64e+07 | — | — | 2026-10-05T04:49:01.475 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 18 | Float64 | 180×180×200 | 97.59 | +261.7% | 10.25 | 6.64e+07 | — | — | 2026-10-05T04:49:01.475 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 19 | Float64 | 180×180×200 | 97.53 | +255.5% | 10.25 | 6.64e+07 | — | — | 2026-10-05T04:49:01.475 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 20 | Float64 | 180×180×200 | 98.27 | +257.3% | 10.18 | 6.59e+07 | — | — | 2026-10-05T04:49:01.475 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 21 | Float64 | 180×180×200 | 97.97 | +259.6% | 10.21 | 6.61e+07 | — | — | 2026-10-05T04:49:01.475 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 22 | Float64 | 180×180×200 | 97.65 | +255.4% | 10.24 | 6.64e+07 | — | — | 2026-10-05T04:49:01.475 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 23 | Float64 | 180×180×200 | 97.61 | +254.7% | 10.24 | 6.64e+07 | — | — | 2026-10-05T04:49:01.475 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 24 | Float64 | 180×180×200 | 98.12 | +259.2% | 10.19 | 6.60e+07 | — | — | 2026-10-05T04:49:01.477 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 25 | Float64 | 180×180×200 | 97.72 | +259.8% | 10.23 | 6.63e+07 | — | — | 2026-10-05T04:49:01.477 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 26 | Float64 | 180×180×200 | 97.66 | +259.9% | 10.24 | 6.64e+07 | — | — | 2026-10-05T04:49:01.477 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 27 | Float64 | 180×180×200 | 97.69 | +255.3% | 10.24 | 6.63e+07 | — | — | 2026-10-05T04:49:01.477 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 28 | Float64 | 180×180×200 | 98.31 | +289.4% | 10.17 | 6.59e+07 | — | — | 2026-10-05T04:49:01.477 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 29 | Float64 | 180×180×200 | 98.03 | +290.7% | 10.20 | 6.61e+07 | — | — | 2026-10-05T04:49:01.477 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 30 | Float64 | 180×180×200 | 98.13 | +287.0% | 10.19 | 6.60e+07 | — | — | 2026-10-05T04:49:01.477 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 31 | Float64 | 180×180×200 | 98.17 | +284.2% | 10.19 | 6.60e+07 | — | — | 2026-10-05T04:49:01.477 |
