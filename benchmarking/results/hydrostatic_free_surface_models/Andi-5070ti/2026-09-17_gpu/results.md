# Oceananigans Benchmark Results

## System Information

| Property | Value |
|----------|-------|
| Julia | 1.12.7 |
| Oceananigans | 0.113.0 |
| Architecture | GPU{CUDABackend} |
| CPU | AMD Ryzen 9 9955HX 16-Core Processor            (znver5) |
| Threads | 1 |
| GPU | NVIDIA GeForce RTX 5070 Ti Laptop GPU |
| CUDA | 12.9.0 |
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
| `EarthOcean_lat_lon_180x90x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | false | Float64 | 180×90×50 | 101.87 | +0.5% | 9.82 | 7.95e+06 | — | — | 2026-09-17T14:52:19.553 |
| `EarthOcean_lat_lon_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | false | Float64 | 360×180×50 | 375.16 | +0.6% | 2.67 | 8.64e+06 | — | — | 2026-09-17T14:54:12.711 |
| `EarthOcean_lat_lon_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | false | Float64 | 720×360×50 | 1438.83 | +0.5% | 0.70 | 9.01e+06 | — | — | 2026-09-17T14:57:00.519 |
| `EarthOcean_lat_lon_1440x720x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | false | Float64 | 1440×720×50 | 8115.04 | +8.0% | 0.12 | 6.39e+06 | — | — | 2026-09-23T15:03:13.006 |
