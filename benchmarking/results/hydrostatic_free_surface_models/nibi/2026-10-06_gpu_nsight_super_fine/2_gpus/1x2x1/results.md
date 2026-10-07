# Oceananigans Benchmark Results

## System Information

| Property | Value |
|----------|-------|
| Julia | 1.10.10 |
| Oceananigans | 0.113.0 |
| Architecture | Distributed{GPU{CUDABackend}, false, Partition{Int64, Int64, Int64}, Tuple{Int64, Int64, Int64}, Int64, Tuple{Int64, Int64, Int64}, Oceananigans.DistributedComputations.NeighboringRanks{Nothing, Nothing, Int64, Int64, Nothing, Nothing, Nothing, Nothing}, MPI.Comm, Vector{MPI.Request}, Base.RefValue{Int64}, Nothing} |
| CPU | INTEL(R) XEON(R) PLATINUM 8570 (icelake-client) |
| Threads | 1 |
| Hostname | g21.nibi.sharcnet |
| Adapt | 4.7.1 |
| CUDA | 6.1.0 |
| GPUArrays | 11.5.15 |
| GPUCompiler | 1.17.1 |
| KernelAbstractions | 0.9.43 |
| LLVM | 9.13.2 |

## Results

| Benchmark | Distributed | Float | Grid | Time/unit (ms) | Spread | Units/s | Points/s | Size | Chunks | Timestamp |
|-----------|-------------|-------|------|----------------|--------|---------|----------|------|--------|-----------|
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 0 | Float64 | 1440×360×200 | 544.87 | +7.1% | 1.84 | 1.90e+08 | — | — | 2026-10-07T13:07:51.627 |
| `EarthOcean_lat_lon_1440x720x200_F64_WENOVectorInvariantDefault_WENO7_CATKE_2tr` | rank 1 | Float64 | 1440×360×200 | 544.54 | +7.9% | 1.84 | 1.90e+08 | — | — | 2026-10-07T13:07:51.628 |

# Profiling configuration

Global resolution: 1440 × 720 × 200 (`super_fine`).
Grid type: LatitudeLongitudeGrid. MPI partition: 1x2x1.
Local resolution per rank: 1440 × 360 × 200.
2 H100 GPUs, one MPI rank and one Julia thread per GPU, on one node.
Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3, Δt=60 s.
Free-surface substeps=30 requested; extend_halos=true.
Two untimed steps: one warmup step and one unprofiled preflight window.
Nsight captures five ten-step timing windows and timing-helper finalization.
CUDA profiler API start/stop markers exclude initialization and warmup; JSON output and finite-state checks follow capture.
