# Oceananigans Benchmark Results

## System Information

| Property | Value |
|----------|-------|
| Julia | 1.12.7 |
| Oceananigans | 0.113.0 |
| Architecture | GPU{CUDABackend} |
| CPU | AMD EPYC 7713 64-Core Processor (znver3) |
| Threads | 1 |
| GPU | NVIDIA A100-SXM4-40GB |
| CUDA | 12.3.0 |
| Hostname | rondeau |
| Adapt | 4.7.1 |
| CUDA | 6.1.0 |
| GPUArrays | 11.5.14 |
| GPUCompiler | 1.17.1 |
| KernelAbstractions | 0.9.42 |
| LLVM | 9.13.2 |

## Results

| Benchmark | Distributed | Float | Grid | Time/unit (ms) | Spread | Units/s | Points/s | Size | Chunks | Timestamp |
|-----------|-------------|-------|------|----------------|--------|---------|----------|------|--------|-----------|
| `EarthOcean_lat_lon_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | false | Float64 | 720×360×50 | 125.82 | +0.2% | 7.95 | 1.03e+08 | — | — | 2026-09-27T04:55:28.391 |
