# Profiling configuration

Global resolution: 1440 × 720 × 200 (`super_fine`).
Grid type: LatitudeLongitudeGrid. MPI partition: 1x4x1.
Local resolution per rank: 1440 × 180 × 200.
4 H100 GPUs, one MPI rank and one Julia thread per GPU, on one node.
Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3, Δt=60 s.
Free-surface substeps=30 requested; extend_halos=true.
Two untimed steps: one warmup step and one unprofiled preflight window.
Nsight captures five ten-step timing windows and timing-helper finalization.
CUDA profiler API start/stop markers exclude initialization and warmup; JSON output and finite-state checks follow capture.
