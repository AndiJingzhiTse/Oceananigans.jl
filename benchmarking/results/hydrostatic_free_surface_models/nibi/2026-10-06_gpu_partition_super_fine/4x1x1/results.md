# Oceananigans Benchmark Results

## System Information

| Property | Value |
|----------|-------|
| Julia | 1.10.10 |
| Oceananigans | 0.113.0 |
| Architecture | Distributed{GPU{CUDABackend}, false, Partition{Int64, Int64, Int64}, Tuple{Int64, Int64, Int64}, Int64, Tuple{Int64, Int64, Int64}, Oceananigans.DistributedComputations.NeighboringRanks{Int64, Int64, Nothing, Nothing, Nothing, Nothing, Nothing, Nothing}, MPI.Comm, Vector{MPI.Request}, Base.RefValue{Int64}, Nothing} |
| CPU | INTEL(R) XEON(R) PLATINUM 8570 (icelake-client) |
| Threads | 1 |
| Hostname | g13.nibi.sharcnet |
| Adapt | 4.7.1 |
| CUDA | 6.1.0 |
| GPUArrays | 11.5.15 |
| GPUCompiler | 1.17.1 |
| KernelAbstractions | 0.9.43 |
| LLVM | 9.13.2 |

## Results

| Benchmark | Distributed | Float | Grid | Time/unit (ms) | Spread | Units/s | Points/s | Size | Chunks | Timestamp |
|-----------|-------------|-------|------|----------------|--------|---------|----------|------|--------|-----------|
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 360×720×200 | 261.24 | +3.0% | 3.83 | 1.98e+08 | — | — | 2026-10-07T16:19:39.117 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 360×720×200 | 261.24 | +3.0% | 3.83 | 1.98e+08 | — | — | 2026-10-07T16:19:39.117 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 360×720×200 | 261.25 | +3.0% | 3.83 | 1.98e+08 | — | — | 2026-10-07T16:19:39.117 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 360×720×200 | 261.25 | +3.0% | 3.83 | 1.98e+08 | — | — | 2026-10-07T16:19:39.117 |
