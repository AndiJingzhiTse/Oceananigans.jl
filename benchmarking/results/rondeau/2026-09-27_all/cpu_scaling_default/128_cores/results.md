# Oceananigans Benchmark Results

## System Information

| Property | Value |
|----------|-------|
| Julia | 1.12.7 |
| Oceananigans | 0.113.0 |
| Architecture | Distributed{CPU, false, Partition{Int64, Int64, Int64}, Tuple{Int64, Int64, Int64}, Int64, Tuple{Int64, Int64, Int64}, Oceananigans.DistributedComputations.NeighboringRanks{Int64, Int64, Int64, Int64, Int64, Int64, Int64, Int64}, MPI.Comm, Vector{MPI.Request}, Base.RefValue{Int64}, Nothing} |
| CPU | AMD EPYC 7713 64-Core Processor (znver3) |
| Threads | 1 |
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
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 45×11×50 | 814.30 | +32.8% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.550 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 45×11×50 | 822.45 | +31.4% | 1.22 | 3.01e+04 | — | — | 2026-09-30T04:46:21.710 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 2 | Float64 | 45×11×50 | 822.50 | +31.4% | 1.22 | 3.01e+04 | — | — | 2026-09-30T04:46:21.710 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 3 | Float64 | 45×11×50 | 815.16 | +31.3% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.739 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 4 | Float64 | 45×11×50 | 806.71 | +32.7% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.633 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 5 | Float64 | 45×11×50 | 806.70 | +32.7% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.634 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 6 | Float64 | 45×11×50 | 813.99 | +32.9% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.633 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 7 | Float64 | 45×11×50 | 801.08 | +35.0% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.480 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 8 | Float64 | 45×11×50 | 802.13 | +34.8% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.473 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 9 | Float64 | 45×11×50 | 802.07 | +34.8% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.460 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 10 | Float64 | 45×11×50 | 805.01 | +34.4% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.430 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 11 | Float64 | 45×11×50 | 803.90 | +34.5% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.403 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 12 | Float64 | 45×11×50 | 802.97 | +34.7% | 1.25 | 3.08e+04 | — | — | 2026-09-30T04:46:21.370 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 13 | Float64 | 45×11×50 | 803.33 | +34.6% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.370 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 14 | Float64 | 45×11×50 | 804.94 | +34.4% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.371 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 15 | Float64 | 45×15×50 | 811.06 | +33.3% | 1.23 | 4.16e+04 | — | — | 2026-09-30T04:46:21.352 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 16 | Float64 | 45×11×50 | 813.72 | +33.2% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.556 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 17 | Float64 | 45×11×50 | 822.15 | +31.7% | 1.22 | 3.01e+04 | — | — | 2026-09-30T04:46:21.693 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 18 | Float64 | 45×11×50 | 822.15 | +31.7% | 1.22 | 3.01e+04 | — | — | 2026-09-30T04:46:21.709 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 19 | Float64 | 45×11×50 | 822.15 | +30.2% | 1.22 | 3.01e+04 | — | — | 2026-09-30T04:46:21.710 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 20 | Float64 | 45×11×50 | 814.05 | +31.6% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.592 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 21 | Float64 | 45×11×50 | 813.99 | +31.6% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.593 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 22 | Float64 | 45×11×50 | 814.02 | +32.9% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.603 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 23 | Float64 | 45×11×50 | 801.32 | +34.9% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.479 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 24 | Float64 | 45×11×50 | 801.39 | +35.0% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.488 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 25 | Float64 | 45×11×50 | 801.58 | +34.9% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.496 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 26 | Float64 | 45×11×50 | 804.65 | +34.4% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.476 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 27 | Float64 | 45×11×50 | 804.17 | +34.5% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.461 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 28 | Float64 | 45×11×50 | 804.14 | +34.5% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.448 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 29 | Float64 | 45×11×50 | 805.27 | +34.4% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.437 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 30 | Float64 | 45×11×50 | 805.25 | +34.4% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.391 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 31 | Float64 | 45×15×50 | 812.77 | +33.0% | 1.23 | 4.15e+04 | — | — | 2026-09-30T04:46:21.389 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 32 | Float64 | 45×11×50 | 813.79 | +32.9% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.579 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 33 | Float64 | 45×11×50 | 822.10 | +31.5% | 1.22 | 3.01e+04 | — | — | 2026-09-30T04:46:21.709 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 34 | Float64 | 45×11×50 | 822.12 | +31.5% | 1.22 | 3.01e+04 | — | — | 2026-09-30T04:46:21.733 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 35 | Float64 | 45×11×50 | 822.06 | +31.6% | 1.22 | 3.01e+04 | — | — | 2026-09-30T04:46:21.734 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 36 | Float64 | 45×11×50 | 813.71 | +32.9% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.628 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 37 | Float64 | 45×11×50 | 813.72 | +33.0% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.628 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 38 | Float64 | 45×11×50 | 813.37 | +33.0% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.626 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 39 | Float64 | 45×11×50 | 800.82 | +35.0% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.505 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 40 | Float64 | 45×11×50 | 800.91 | +35.1% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.502 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 41 | Float64 | 45×11×50 | 801.23 | +35.0% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.525 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 42 | Float64 | 45×11×50 | 804.75 | +34.4% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.502 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 43 | Float64 | 45×11×50 | 803.97 | +34.6% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.499 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 44 | Float64 | 45×11×50 | 804.06 | +34.5% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.492 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 45 | Float64 | 45×11×50 | 805.26 | +34.4% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.458 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 46 | Float64 | 45×11×50 | 810.34 | +33.5% | 1.23 | 3.05e+04 | — | — | 2026-09-30T04:46:21.453 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 47 | Float64 | 45×15×50 | 820.32 | +31.8% | 1.22 | 4.11e+04 | — | — | 2026-09-30T04:46:21.483 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 48 | Float64 | 45×11×50 | 813.78 | +32.9% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.579 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 49 | Float64 | 45×11×50 | 815.22 | +32.7% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.650 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 50 | Float64 | 45×11×50 | 815.17 | +32.7% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.671 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 51 | Float64 | 45×11×50 | 815.11 | +32.7% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.677 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 52 | Float64 | 45×11×50 | 813.77 | +32.9% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.633 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 53 | Float64 | 45×11×50 | 813.75 | +32.9% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.630 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 54 | Float64 | 45×11×50 | 813.41 | +33.0% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.649 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 55 | Float64 | 45×11×50 | 800.92 | +35.0% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.509 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 56 | Float64 | 45×11×50 | 801.01 | +35.1% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.510 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 57 | Float64 | 45×11×50 | 801.24 | +35.0% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.502 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 58 | Float64 | 45×11×50 | 804.86 | +34.4% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.499 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 59 | Float64 | 45×11×50 | 804.13 | +34.5% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.484 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 60 | Float64 | 45×11×50 | 804.14 | +34.5% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.469 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 61 | Float64 | 45×11×50 | 805.28 | +35.7% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.465 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 62 | Float64 | 45×11×50 | 810.35 | +35.3% | 1.23 | 3.05e+04 | — | — | 2026-09-30T04:46:21.449 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 63 | Float64 | 45×15×50 | 820.35 | +34.2% | 1.22 | 4.11e+04 | — | — | 2026-09-30T04:46:21.446 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 64 | Float64 | 45×11×50 | 812.58 | +33.1% | 1.23 | 3.05e+04 | — | — | 2026-09-30T04:46:21.596 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 65 | Float64 | 45×11×50 | 815.33 | +32.6% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.659 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 66 | Float64 | 45×11×50 | 815.32 | +32.6% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.659 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 67 | Float64 | 45×11×50 | 817.03 | +32.4% | 1.22 | 3.03e+04 | — | — | 2026-09-30T04:46:21.648 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 68 | Float64 | 45×11×50 | 813.72 | +32.9% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.642 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 69 | Float64 | 45×11×50 | 813.61 | +34.4% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.617 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 70 | Float64 | 45×11×50 | 813.36 | +34.5% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.612 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 71 | Float64 | 45×11×50 | 801.03 | +36.6% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.481 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 72 | Float64 | 45×11×50 | 801.00 | +35.0% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.480 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 73 | Float64 | 45×11×50 | 801.27 | +34.9% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.478 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 74 | Float64 | 45×11×50 | 804.93 | +34.3% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.469 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 75 | Float64 | 45×11×50 | 804.29 | +34.4% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.439 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 76 | Float64 | 45×11×50 | 804.24 | +34.3% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.423 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 77 | Float64 | 45×11×50 | 805.35 | +36.0% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.397 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 78 | Float64 | 45×11×50 | 811.21 | +35.2% | 1.23 | 3.05e+04 | — | — | 2026-09-30T04:46:21.446 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 79 | Float64 | 45×15×50 | 820.36 | +33.9% | 1.22 | 4.11e+04 | — | — | 2026-09-30T04:46:21.450 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 80 | Float64 | 45×11×50 | 812.06 | +33.0% | 1.23 | 3.05e+04 | — | — | 2026-09-30T04:46:21.603 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 81 | Float64 | 45×11×50 | 812.51 | +32.9% | 1.23 | 3.05e+04 | — | — | 2026-09-30T04:46:21.675 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 82 | Float64 | 45×11×50 | 817.17 | +32.2% | 1.22 | 3.03e+04 | — | — | 2026-09-30T04:46:21.678 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 83 | Float64 | 45×11×50 | 817.28 | +32.2% | 1.22 | 3.03e+04 | — | — | 2026-09-30T04:46:21.656 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 84 | Float64 | 45×11×50 | 814.21 | +32.7% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.632 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 85 | Float64 | 45×11×50 | 813.98 | +34.5% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.582 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 86 | Float64 | 45×11×50 | 813.97 | +34.5% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.582 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 87 | Float64 | 45×11×50 | 801.05 | +36.7% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.467 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 88 | Float64 | 45×11×50 | 803.60 | +34.4% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.474 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 89 | Float64 | 45×11×50 | 803.51 | +34.4% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.494 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 90 | Float64 | 45×11×50 | 804.61 | +34.2% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.498 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 91 | Float64 | 45×11×50 | 804.20 | +34.3% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.495 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 92 | Float64 | 45×11×50 | 804.21 | +34.3% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.462 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 93 | Float64 | 45×11×50 | 805.32 | +35.9% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.425 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 94 | Float64 | 45×11×50 | 805.35 | +36.1% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.407 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 95 | Float64 | 45×15×50 | 820.27 | +33.8% | 1.22 | 4.11e+04 | — | — | 2026-09-30T04:46:21.462 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 96 | Float64 | 45×11×50 | 812.11 | +33.0% | 1.23 | 3.05e+04 | — | — | 2026-09-30T04:46:21.562 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 97 | Float64 | 45×11×50 | 815.34 | +32.5% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.663 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 98 | Float64 | 45×11×50 | 815.70 | +32.5% | 1.23 | 3.03e+04 | — | — | 2026-09-30T04:46:21.670 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 99 | Float64 | 45×11×50 | 810.09 | +33.4% | 1.23 | 3.06e+04 | — | — | 2026-09-30T04:46:21.660 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 100 | Float64 | 45×11×50 | 807.10 | +33.9% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.648 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 101 | Float64 | 45×11×50 | 805.98 | +35.8% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.606 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 102 | Float64 | 45×11×50 | 814.45 | +34.5% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.586 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 103 | Float64 | 45×11×50 | 801.55 | +36.7% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.451 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 104 | Float64 | 45×11×50 | 803.64 | +34.4% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.448 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 105 | Float64 | 45×11×50 | 803.65 | +34.4% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.440 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 106 | Float64 | 45×11×50 | 804.66 | +34.2% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.444 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 107 | Float64 | 45×11×50 | 804.27 | +34.3% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.469 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 108 | Float64 | 45×11×50 | 804.25 | +34.3% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.439 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 109 | Float64 | 45×11×50 | 805.33 | +34.2% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.412 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 110 | Float64 | 45×11×50 | 805.28 | +34.2% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.404 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 111 | Float64 | 45×15×50 | 812.92 | +32.8% | 1.23 | 4.15e+04 | — | — | 2026-09-30T04:46:21.399 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 112 | Float64 | 45×11×50 | 814.28 | +32.6% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.588 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 113 | Float64 | 45×11×50 | 814.30 | +32.7% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.623 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 114 | Float64 | 45×11×50 | 814.20 | +32.7% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.637 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 115 | Float64 | 45×11×50 | 807.07 | +32.7% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.636 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 116 | Float64 | 45×11×50 | 807.08 | +32.7% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.652 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 117 | Float64 | 45×11×50 | 806.76 | +32.7% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.609 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 118 | Float64 | 45×11×50 | 813.95 | +32.9% | 1.23 | 3.04e+04 | — | — | 2026-09-30T04:46:21.603 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 119 | Float64 | 45×11×50 | 801.30 | +35.0% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.481 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 120 | Float64 | 45×11×50 | 801.24 | +35.0% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.451 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 121 | Float64 | 45×11×50 | 801.71 | +34.9% | 1.25 | 3.09e+04 | — | — | 2026-09-30T04:46:21.445 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 122 | Float64 | 45×11×50 | 804.31 | +34.2% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.404 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 123 | Float64 | 45×11×50 | 804.30 | +34.3% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.420 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 124 | Float64 | 45×11×50 | 804.30 | +34.3% | 1.24 | 3.08e+04 | — | — | 2026-09-30T04:46:21.420 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 125 | Float64 | 45×11×50 | 805.83 | +34.0% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.376 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 126 | Float64 | 45×11×50 | 806.22 | +33.9% | 1.24 | 3.07e+04 | — | — | 2026-09-30T04:46:21.373 |
| `EarthOcean_tripolar_360x180x50_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 127 | Float64 | 45×15×50 | 812.96 | +32.8% | 1.23 | 4.15e+04 | — | — | 2026-09-30T04:46:21.373 |
