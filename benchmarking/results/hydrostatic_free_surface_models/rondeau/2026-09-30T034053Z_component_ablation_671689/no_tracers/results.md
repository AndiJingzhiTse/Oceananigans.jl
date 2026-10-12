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
| `EarthOcean_tripolar_360x180x50_F32_WENOVectorInvariantDefault_WENO7_CATKE_0tr` | false | Float32 | 360×180×50 | 16.57 | +47.3% | 60.37 | 1.96e+08 | — | — | 2026-09-30T04:12:22.293 |
