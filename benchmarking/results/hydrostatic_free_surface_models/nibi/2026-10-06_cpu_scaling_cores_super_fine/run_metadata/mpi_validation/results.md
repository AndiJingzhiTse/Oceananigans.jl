# Oceananigans Benchmark Results

## System Information

| Property | Value |
|----------|-------|
| Julia | 1.10.10 |
| Oceananigans | 0.113.0 |
| Architecture | Distributed{CPU, false, Partition{Sizes{Tuple{Int64, Int64, Int64}}, Sizes{Int64}, Int64}, Tuple{Int64, Int64, Int64}, Int64, Tuple{Int64, Int64, Int64}, Oceananigans.DistributedComputations.NeighboringRanks{Int64, Int64, Nothing, Nothing, Nothing, Nothing, Nothing, Nothing}, MPI.Comm, Vector{MPI.Request}, Base.RefValue{Int64}, Nothing} |
| CPU | Intel(R) Xeon(R) 6972P (icelake-client) |
| Threads | 1 |
| Hostname | c648.nibi.sharcnet |
| Adapt | 4.7.1 |
| CUDA | 6.1.0 |
| GPUArrays | 11.5.15 |
| GPUCompiler | 1.17.1 |
| KernelAbstractions | 0.9.43 |
| LLVM | 9.13.2 |

## Results

| Benchmark | Distributed | Float | Grid | Time/unit (ms) | Spread | Units/s | Points/s | Size | Chunks | Timestamp |
|-----------|-------------|-------|------|----------------|--------|---------|----------|------|--------|-----------|
| `EarthOcean_lat_lon_72x36x8_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 24×36×8 | 35.97 | +2.1% | 27.80 | 1.92e+05 | — | — | 2026-10-06T17:28:50.957 |
| `EarthOcean_lat_lon_72x36x8_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 24×36×8 | 35.97 | +3.0% | 27.80 | 1.92e+05 | — | — | 2026-10-06T17:28:50.957 |
| `EarthOcean_lat_lon_72x36x8_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 24×36×8 | 35.96 | +3.1% | 27.81 | 1.92e+05 | — | — | 2026-10-06T17:28:50.957 |

# MPI wrapper validation

Resolution: 72 × 36 × 8. Grid type: LatitudeLongitudeGrid.
Partition: 3 × 1 × 1; local resolution: 24 × 36 × 8.
Three cores, three MPI ranks, one pinned thread per rank.
Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=1 s; one warmup step and two one-step windows.
Free-surface substeps=30, extend_halos=false.
These small-grid validation timings are excluded from the production scaling plot.
