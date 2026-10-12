# Oceananigans Benchmark Results

## System Information

| Property | Value |
|----------|-------|
| Julia | 1.10.10 |
| Oceananigans | 0.113.0 |
| Architecture | Distributed{CPU, false, Partition{Int64, Int64, Int64}, Tuple{Int64, Int64, Int64}, Int64, Tuple{Int64, Int64, Int64}, Oceananigans.DistributedComputations.NeighboringRanks{Int64, Int64, Int64, Int64, Int64, Int64, Int64, Int64}, MPI.Comm, Vector{MPI.Request}, Base.RefValue{Int64}, Nothing} |
| CPU | Intel(R) Xeon(R) 6972P (icelake-client) |
| Threads | 192 |
| Hostname | c462.nibi.sharcnet |
| Adapt | 4.7.1 |
| CUDA | 6.1.0 |
| GPUArrays | 11.5.15 |
| GPUCompiler | 1.17.1 |
| KernelAbstractions | 0.9.43 |
| LLVM | 9.13.2 |

## Results

| Benchmark | Distributed | Float | Grid | Time/unit (ms) | Spread | Units/s | Points/s | Size | Chunks | Timestamp |
|-----------|-------------|-------|------|----------------|--------|---------|----------|------|--------|-----------|
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 720×360×200 | 55448.35 | +3.5% | 0.02 | 9.35e+05 | — | — | 2026-10-06T09:46:08.621 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 720×360×200 | 55354.77 | +3.9% | 0.02 | 9.37e+05 | — | — | 2026-10-06T09:46:07.585 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 720×360×200 | 55417.08 | +3.9% | 0.02 | 9.35e+05 | — | — | 2026-10-06T09:46:07.969 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 720×360×200 | 55278.07 | +4.0% | 0.02 | 9.38e+05 | — | — | 2026-10-06T09:46:07.374 |
