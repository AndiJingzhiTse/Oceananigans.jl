# Benchmark configuration

Global resolution: 1440 × 720 × 200. Grid type: LatitudeLongitudeGrid.
Partition: 32 × 24 × 1.
768 cores; 4 nodes; 768 MPI ranks; 1 pinned Julia threads per rank.
Local resolution: x 45–45, y 30–30, z 200. Remainder cells are distributed evenly; the global grid is preserved.
Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=60 s; two warmup steps, five ten-step windows.
SplitExplicitFreeSurface(substeps=30, extend_halos=false): exchange halos at every substep.
