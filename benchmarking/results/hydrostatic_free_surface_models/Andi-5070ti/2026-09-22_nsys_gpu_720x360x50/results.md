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
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | false | Float64 | 720×360×50 | 1200.08 | +0.0% | 0.83 | 1.08e+07 | — | — | 2026-09-22T14:31:19.184 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | false | Float64 | 720×360×50 | 1170.18 | +0.0% | 0.85 | 1.11e+07 | — | — | 2026-09-22T14:34:45.889 |
