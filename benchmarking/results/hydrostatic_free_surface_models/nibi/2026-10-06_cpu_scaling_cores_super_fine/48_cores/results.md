# Oceananigans Benchmark Results

## System Information

| Property | Value |
|----------|-------|
| Julia | 1.10.10 |
| Oceananigans | 0.113.0 |
| Architecture | Distributed{CPU, false, Partition{Sizes{NTuple{8, Int64}}, Sizes{NTuple{6, Int64}}, Int64}, Tuple{Int64, Int64, Int64}, Int64, Tuple{Int64, Int64, Int64}, Oceananigans.DistributedComputations.NeighboringRanks{Int64, Int64, Int64, Int64, Int64, Int64, Int64, Int64}, MPI.Comm, Vector{MPI.Request}, Base.RefValue{Int64}, Nothing} |
| CPU | Intel(R) Xeon(R) 6972P (icelake-client) |
| Threads | 1 |
| Hostname | c203.nibi.sharcnet |
| Adapt | 4.7.1 |
| CUDA | 6.1.0 |
| GPUArrays | 11.5.15 |
| GPUCompiler | 1.17.1 |
| KernelAbstractions | 0.9.43 |
| LLVM | 9.13.2 |

## Results

| Benchmark | Distributed | Float | Grid | Time/unit (ms) | Spread | Units/s | Points/s | Size | Chunks | Timestamp |
|-----------|-------------|-------|------|----------------|--------|---------|----------|------|--------|-----------|
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 180×120×200 | 19740.81 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.832 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 180×120×200 | 19740.49 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.888 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 180×120×200 | 19739.95 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 180×120×200 | 19731.45 | +3.4% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 4 | Float64 | 180×120×200 | 19731.12 | +3.4% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.755 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 5 | Float64 | 180×120×200 | 19731.45 | +3.4% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.692 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 6 | Float64 | 180×120×200 | 19735.00 | +3.2% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.716 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 7 | Float64 | 180×120×200 | 19735.22 | +3.2% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.784 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 8 | Float64 | 180×120×200 | 19731.83 | +3.2% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 9 | Float64 | 180×120×200 | 19741.47 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 10 | Float64 | 180×120×200 | 19738.59 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.848 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 11 | Float64 | 180×120×200 | 19739.93 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.799 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 12 | Float64 | 180×120×200 | 19739.75 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.793 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 13 | Float64 | 180×120×200 | 19739.52 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.855 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 14 | Float64 | 180×120×200 | 19741.89 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 15 | Float64 | 180×120×200 | 19740.15 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 16 | Float64 | 180×120×200 | 19737.69 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.900 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 17 | Float64 | 180×120×200 | 19738.30 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.826 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 18 | Float64 | 180×120×200 | 19739.30 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.821 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 19 | Float64 | 180×120×200 | 19736.73 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.887 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 20 | Float64 | 180×120×200 | 19738.13 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 21 | Float64 | 180×120×200 | 19740.44 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.653 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 22 | Float64 | 180×120×200 | 19742.89 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.888 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 23 | Float64 | 180×120×200 | 19741.73 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.822 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 24 | Float64 | 180×120×200 | 19739.01 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.820 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 25 | Float64 | 180×120×200 | 19738.32 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.891 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 26 | Float64 | 180×120×200 | 19736.04 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 27 | Float64 | 180×120×200 | 19739.24 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 28 | Float64 | 180×120×200 | 19741.97 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.851 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 29 | Float64 | 180×120×200 | 19742.47 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.801 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 30 | Float64 | 180×120×200 | 19739.58 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.820 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 31 | Float64 | 180×120×200 | 19739.78 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.887 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 32 | Float64 | 180×120×200 | 19735.84 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 33 | Float64 | 180×120×200 | 19737.77 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 34 | Float64 | 180×120×200 | 19741.78 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.869 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 35 | Float64 | 180×120×200 | 19741.26 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.799 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 36 | Float64 | 180×120×200 | 19738.84 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.842 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 37 | Float64 | 180×120×200 | 19738.38 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.932 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 38 | Float64 | 180×120×200 | 19736.83 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 39 | Float64 | 180×120×200 | 19737.61 | +3.2% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 40 | Float64 | 180×120×200 | 19740.06 | +3.2% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.850 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 41 | Float64 | 180×120×200 | 19740.76 | +3.2% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.802 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 42 | Float64 | 180×120×200 | 19739.55 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.849 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 43 | Float64 | 180×120×200 | 19737.92 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.926 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 44 | Float64 | 180×120×200 | 19736.08 | +3.1% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 45 | Float64 | 180×120×200 | 19736.27 | +3.3% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.642 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 46 | Float64 | 180×120×200 | 19742.95 | +3.3% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.824 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 47 | Float64 | 180×120×200 | 19742.97 | +3.3% | 0.05 | 2.19e+05 | — | — | 2026-10-06T17:41:50.767 |

# Benchmark configuration

Global resolution: 1440 × 720 × 200. Grid type: LatitudeLongitudeGrid.
Partition: 8 × 6 × 1.
48 cores; 1 nodes; 48 MPI ranks; 1 pinned Julia threads per rank.
Local resolution: x 180–180, y 120–120, z 200. Remainder cells are distributed evenly; the global grid is preserved.
Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=60 s; two warmup steps, five ten-step windows.
SplitExplicitFreeSurface(substeps=30, extend_halos=false): exchange halos at every substep.
