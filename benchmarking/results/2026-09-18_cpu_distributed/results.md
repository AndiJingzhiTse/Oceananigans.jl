# Oceananigans Benchmark Results

## System Information

| Property | Value |
|----------|-------|
| Julia | 1.12.7 |
| Oceananigans | 0.113.0 |
| Architecture | Distributed{CPU, false, Partition{Int64, Int64, Int64}, Tuple{Int64, Int64, Int64}, Int64, Tuple{Int64, Int64, Int64}, Oceananigans.DistributedComputations.NeighboringRanks{Int64, Int64, Int64, Int64, Int64, Int64, Int64, Int64}, MPI.Comm, Vector{MPI.Request}, Base.RefValue{Int64}, Nothing} |
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
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 720×360×50 | 66266.96 | +9.3% | 0.02 | 1.96e+05 | — | — | 2026-09-18T20:29:33.123 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 720×180×50 | 46149.24 | +22.2% | 0.02 | 1.40e+05 | — | — | 2026-09-18T21:47:02.281 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 720×180×50 | 46150.35 | +22.1% | 0.02 | 1.40e+05 | — | — | 2026-09-18T21:47:02.284 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 360×180×50 | 31254.41 | +6.8% | 0.03 | 1.04e+05 | — | — | 2026-09-18T23:04:31.526 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 360×180×50 | 31253.69 | +6.8% | 0.03 | 1.04e+05 | — | — | 2026-09-18T23:04:31.475 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 360×180×50 | 31250.98 | +6.8% | 0.03 | 1.04e+05 | — | — | 2026-09-18T23:04:31.442 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 360×180×50 | 31253.76 | +6.8% | 0.03 | 1.04e+05 | — | — | 2026-09-18T23:04:31.344 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 360×90×50 | 15739.18 | +9.5% | 0.06 | 1.03e+05 | — | — | 2026-09-18T23:52:24.476 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 360×90×50 | 15737.59 | +9.5% | 0.06 | 1.03e+05 | — | — | 2026-09-18T23:52:24.672 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 360×90×50 | 15737.84 | +9.5% | 0.06 | 1.03e+05 | — | — | 2026-09-18T23:52:24.508 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 360×90×50 | 15736.61 | +9.6% | 0.06 | 1.03e+05 | — | — | 2026-09-18T23:52:23.468 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 4 | Float64 | 360×90×50 | 15738.43 | +9.5% | 0.06 | 1.03e+05 | — | — | 2026-09-18T23:52:24.456 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 5 | Float64 | 360×90×50 | 15739.11 | +9.5% | 0.06 | 1.03e+05 | — | — | 2026-09-18T23:52:24.562 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 6 | Float64 | 360×90×50 | 15739.47 | +9.5% | 0.06 | 1.03e+05 | — | — | 2026-09-18T23:52:24.460 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 7 | Float64 | 360×90×50 | 15738.45 | +9.5% | 0.06 | 1.03e+05 | — | — | 2026-09-18T23:52:24.375 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 180×90×50 | 9111.31 | +1.1% | 0.11 | 8.89e+04 | — | — | 2026-09-19T02:31:10.706 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 180×90×50 | 9109.55 | +1.1% | 0.11 | 8.89e+04 | — | — | 2026-09-19T02:31:10.751 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 180×90×50 | 9112.94 | +1.1% | 0.11 | 8.89e+04 | — | — | 2026-09-19T02:31:10.689 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 180×90×50 | 9111.86 | +1.1% | 0.11 | 8.89e+04 | — | — | 2026-09-19T02:31:10.616 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 4 | Float64 | 180×90×50 | 9112.35 | +1.1% | 0.11 | 8.89e+04 | — | — | 2026-09-19T02:31:10.690 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 5 | Float64 | 180×90×50 | 9112.27 | +1.1% | 0.11 | 8.89e+04 | — | — | 2026-09-19T02:31:10.764 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 6 | Float64 | 180×90×50 | 9112.78 | +1.1% | 0.11 | 8.89e+04 | — | — | 2026-09-19T02:31:10.764 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 7 | Float64 | 180×90×50 | 9112.68 | +1.1% | 0.11 | 8.89e+04 | — | — | 2026-09-19T02:31:10.533 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 8 | Float64 | 180×90×50 | 9111.77 | +1.1% | 0.11 | 8.89e+04 | — | — | 2026-09-19T02:31:10.690 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 9 | Float64 | 180×90×50 | 9112.54 | +1.1% | 0.11 | 8.89e+04 | — | — | 2026-09-19T02:31:10.749 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 10 | Float64 | 180×90×50 | 9112.02 | +1.1% | 0.11 | 8.89e+04 | — | — | 2026-09-19T02:31:10.705 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 11 | Float64 | 180×90×50 | 9112.55 | +1.1% | 0.11 | 8.89e+04 | — | — | 2026-09-19T02:31:10.634 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 12 | Float64 | 180×90×50 | 9110.04 | +1.1% | 0.11 | 8.89e+04 | — | — | 2026-09-19T02:31:10.692 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 13 | Float64 | 180×90×50 | 9110.88 | +1.1% | 0.11 | 8.89e+04 | — | — | 2026-09-19T02:31:10.749 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 14 | Float64 | 180×90×50 | 9113.13 | +1.1% | 0.11 | 8.89e+04 | — | — | 2026-09-19T02:31:10.683 |
| `EarthOcean_tripolar_720x360x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 15 | Float64 | 180×90×50 | 9111.72 | +1.1% | 0.11 | 8.89e+04 | — | — | 2026-09-19T02:31:10.533 |
