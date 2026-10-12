# Oceananigans Benchmark Results

## System Information

| Property | Value |
|----------|-------|
| Julia | 1.10.10 |
| Oceananigans | 0.113.0 |
| Architecture | Distributed{CPU, false, Partition{Sizes{NTuple{4, Int64}}, Sizes{Tuple{Int64, Int64, Int64}}, Int64}, Tuple{Int64, Int64, Int64}, Int64, Tuple{Int64, Int64, Int64}, Oceananigans.DistributedComputations.NeighboringRanks{Int64, Int64, Int64, Int64, Int64, Int64, Int64, Int64}, MPI.Comm, Vector{MPI.Request}, Base.RefValue{Int64}, Nothing} |
| CPU | Intel(R) Xeon(R) 6972P (icelake-client) |
| Threads | 1 |
| Hostname | c495.nibi.sharcnet |
| Adapt | 4.7.1 |
| CUDA | 6.1.0 |
| GPUArrays | 11.5.15 |
| GPUCompiler | 1.17.1 |
| KernelAbstractions | 0.9.43 |
| LLVM | 9.13.2 |

## Results

| Benchmark | Distributed | Float | Grid | Time/unit (ms) | Spread | Units/s | Points/s | Size | Chunks | Timestamp |
|-----------|-------------|-------|------|----------------|--------|---------|----------|------|--------|-----------|
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 360×240×200 | 82774.06 | +2.4% | 0.01 | 2.09e+05 | — | — | 2026-10-06T18:39:41.850 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 360×240×200 | 82774.99 | +2.4% | 0.01 | 2.09e+05 | — | — | 2026-10-06T18:39:41.917 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 360×240×200 | 82747.12 | +2.3% | 0.01 | 2.09e+05 | — | — | 2026-10-06T18:39:41.787 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 360×240×200 | 82773.30 | +2.4% | 0.01 | 2.09e+05 | — | — | 2026-10-06T18:39:41.787 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 4 | Float64 | 360×240×200 | 82770.33 | +2.4% | 0.01 | 2.09e+05 | — | — | 2026-10-06T18:39:42.593 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 5 | Float64 | 360×240×200 | 82779.92 | +2.2% | 0.01 | 2.09e+05 | — | — | 2026-10-06T18:39:42.299 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 6 | Float64 | 360×240×200 | 82770.12 | +2.4% | 0.01 | 2.09e+05 | — | — | 2026-10-06T18:39:41.787 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 7 | Float64 | 360×240×200 | 82812.05 | +2.3% | 0.01 | 2.09e+05 | — | — | 2026-10-06T18:39:42.425 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 8 | Float64 | 360×240×200 | 82813.30 | +2.2% | 0.01 | 2.09e+05 | — | — | 2026-10-06T18:39:42.295 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 9 | Float64 | 360×240×200 | 82770.84 | +2.4% | 0.01 | 2.09e+05 | — | — | 2026-10-06T18:39:41.787 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 10 | Float64 | 360×240×200 | 82768.87 | +2.4% | 0.01 | 2.09e+05 | — | — | 2026-10-06T18:39:42.466 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 11 | Float64 | 360×240×200 | 82802.88 | +2.2% | 0.01 | 2.09e+05 | — | — | 2026-10-06T18:39:42.313 |

# Benchmark configuration

Global resolution: 1440 × 720 × 200. Grid type: LatitudeLongitudeGrid.
Partition: 4 × 3 × 1.
12 cores; 1 nodes; 12 MPI ranks; 1 pinned Julia threads per rank.
Local resolution: x 360–360, y 240–240, z 200. Remainder cells are distributed evenly; the global grid is preserved.
Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=60 s; two warmup steps, five ten-step windows.
SplitExplicitFreeSurface(substeps=30, extend_halos=false): exchange halos at every substep.
