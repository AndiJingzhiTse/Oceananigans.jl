# Oceananigans Benchmark Results

## System Information

| Property | Value |
|----------|-------|
| Julia | 1.12.7 |
| Oceananigans | 0.113.0 |
| Architecture | CPU |
| CPU | AMD Ryzen 9 9955HX 16-Core Processor            (znver5) |
| Threads | 1 |
| Hostname | Andi-5070ti |
| Adapt | 4.7.1 |
| CUDA | 6.1.0 |
| GPUArrays | 11.5.14 |
| GPUCompiler | 1.17.1 |
| KernelAbstractions | 0.9.42 |
| LLVM | 9.13.1 |

## Results

| Benchmark | Distributed | Float | Grid | Time/unit (ms) | Spread | Units/s | Points/s | Size | Chunks | Timestamp |
|-----------|-------------|-------|------|----------------|--------|---------|----------|------|--------|-----------|
| `EarthOcean_lat_lon_180x90x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | false | Float64 | 180×90×50 | 1361.65 | +3.1% | 0.73 | 5.95e+05 | — | — | 2026-09-17T14:27:31.368 |
| `EarthOcean_lat_lon_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | false | Float64 | 360×180×50 | 5560.21 | +1.2% | 0.18 | 5.83e+05 | — | — | 2026-09-17T14:34:10.352 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | false | Float64 | 720×360×50 | 46225.24 | +14.0% | 0.02 | 2.80e+05 | — | — | 2026-09-17T19:10:31.259 |
| `EarthOcean_lat_lon_180x90x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | false | Float64 | 180×90×50 | 101.87 | +0.5% | 9.82 | 7.95e+06 | — | — | 2026-09-17T14:52:19.553 |
| `EarthOcean_lat_lon_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | false | Float64 | 360×180×50 | 375.16 | +0.6% | 2.67 | 8.64e+06 | — | — | 2026-09-17T14:54:12.711 |
| `EarthOcean_lat_lon_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | false | Float64 | 720×360×50 | 1438.83 | +0.5% | 0.70 | 9.01e+06 | — | — | 2026-09-17T14:57:00.519 |

