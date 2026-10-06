# Oceananigans Benchmark Results

## System Information

| Property | Value |
|----------|-------|
| Julia | 1.10.10 |
| Oceananigans | 0.113.0 |
| Architecture | Distributed{CPU, false, Partition{Sizes{Tuple{Int64, Int64, Int64}}, Sizes{Int64}, Int64}, Tuple{Int64, Int64, Int64}, Int64, Tuple{Int64, Int64, Int64}, Oceananigans.DistributedComputations.NeighboringRanks{Int64, Int64, Nothing, Nothing, Nothing, Nothing, Nothing, Nothing}, MPI.Comm, Vector{MPI.Request}, Base.RefValue{Int64}, Nothing} |
| CPU | Intel(R) Xeon(R) 6972P (icelake-client) |
| Threads | 1 |
| Hostname | m8.nibi.sharcnet |
| Adapt | 4.7.1 |
| CUDA | 6.1.0 |
| GPUArrays | 11.5.15 |
| GPUCompiler | 1.17.1 |
| KernelAbstractions | 0.9.43 |
| LLVM | 9.13.2 |

## Results

| Benchmark | Distributed | Float | Grid | Time/unit (ms) | Spread | Units/s | Points/s | Size | Chunks | Timestamp |
|-----------|-------------|-------|------|----------------|--------|---------|----------|------|--------|-----------|
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 480×720×200 | 274286.95 | +3.0% | 0.00 | 2.52e+05 | — | — | 2026-10-06T21:20:49.192 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 480×720×200 | 274286.86 | +3.0% | 0.00 | 2.52e+05 | — | — | 2026-10-06T21:20:49.192 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 480×720×200 | 274287.07 | +3.0% | 0.00 | 2.52e+05 | — | — | 2026-10-06T21:20:49.192 |

# Benchmark configuration

Global resolution: 1440 × 720 × 200. Grid type: LatitudeLongitudeGrid.
Partition: 3 × 1 × 1.
3 cores; 1 nodes; 3 MPI ranks; 1 pinned Julia threads per rank.
Local resolution: x 480–480, y 720–720, z 200. Remainder cells are distributed evenly; the global grid is preserved.
Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=60 s; two warmup steps, five ten-step windows.
SplitExplicitFreeSurface(substeps=30, extend_halos=false): exchange halos at every substep.
