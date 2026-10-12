# Oceananigans Benchmark Results

## System Information

| Property | Value |
|----------|-------|
| Julia | 1.10.10 |
| Oceananigans | 0.113.0 |
| Architecture | Distributed{CPU, false, Partition{Sizes{NTuple{6, Int64}}, Sizes{NTuple{4, Int64}}, Int64}, Tuple{Int64, Int64, Int64}, Int64, Tuple{Int64, Int64, Int64}, Oceananigans.DistributedComputations.NeighboringRanks{Int64, Int64, Int64, Int64, Int64, Int64, Int64, Int64}, MPI.Comm, Vector{MPI.Request}, Base.RefValue{Int64}, Nothing} |
| CPU | Intel(R) Xeon(R) 6972P (icelake-client) |
| Threads | 1 |
| Hostname | c492.nibi.sharcnet |
| Adapt | 4.7.1 |
| CUDA | 6.1.0 |
| GPUArrays | 11.5.15 |
| GPUCompiler | 1.17.1 |
| KernelAbstractions | 0.9.43 |
| LLVM | 9.13.2 |

## Results

| Benchmark | Distributed | Float | Grid | Time/unit (ms) | Spread | Units/s | Points/s | Size | Chunks | Timestamp |
|-----------|-------------|-------|------|----------------|--------|---------|----------|------|--------|-----------|
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 240×180×200 | 45458.67 | +2.4% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:52.117 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 240×180×200 | 45447.33 | +2.4% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:52.173 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 240×180×200 | 45455.54 | +2.3% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:52.327 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 240×180×200 | 45469.41 | +2.2% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:52.358 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 4 | Float64 | 240×180×200 | 45466.39 | +2.4% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:52.090 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 5 | Float64 | 240×180×200 | 45466.09 | +2.3% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:52.174 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 6 | Float64 | 240×180×200 | 45433.24 | +2.3% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:52.225 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 7 | Float64 | 240×180×200 | 45432.01 | +2.3% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:52.120 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 8 | Float64 | 240×180×200 | 45421.64 | +2.4% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:51.779 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 9 | Float64 | 240×180×200 | 45429.74 | +2.4% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:51.817 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 10 | Float64 | 240×180×200 | 45422.52 | +2.4% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:52.110 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 11 | Float64 | 240×180×200 | 45419.13 | +2.4% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:52.009 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 12 | Float64 | 240×180×200 | 45397.24 | +2.4% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:51.779 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 13 | Float64 | 240×180×200 | 45394.89 | +2.4% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:51.779 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 14 | Float64 | 240×180×200 | 45416.77 | +2.4% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:52.112 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 15 | Float64 | 240×180×200 | 45432.00 | +2.3% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:52.089 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 16 | Float64 | 240×180×200 | 45422.51 | +2.3% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:51.976 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 17 | Float64 | 240×180×200 | 45426.62 | +2.3% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:52.042 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 18 | Float64 | 240×180×200 | 45492.94 | +2.2% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:52.426 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 19 | Float64 | 240×180×200 | 45482.75 | +2.2% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:52.233 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 20 | Float64 | 240×180×200 | 45444.62 | +2.4% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:52.177 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 21 | Float64 | 240×180×200 | 45446.75 | +2.4% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:52.265 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 22 | Float64 | 240×180×200 | 45459.81 | +2.3% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:52.370 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 23 | Float64 | 240×180×200 | 45468.22 | +2.3% | 0.02 | 1.90e+05 | — | — | 2026-10-06T18:10:52.358 |

# Benchmark configuration

Global resolution: 1440 × 720 × 200. Grid type: LatitudeLongitudeGrid.
Partition: 6 × 4 × 1.
24 cores; 1 nodes; 24 MPI ranks; 1 pinned Julia threads per rank.
Local resolution: x 240–240, y 180–180, z 200. Remainder cells are distributed evenly; the global grid is preserved.
Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=60 s; two warmup steps, five ten-step windows.
SplitExplicitFreeSurface(substeps=30, extend_halos=false): exchange halos at every substep.
