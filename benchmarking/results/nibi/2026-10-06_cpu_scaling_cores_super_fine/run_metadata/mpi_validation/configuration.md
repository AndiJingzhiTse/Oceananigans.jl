# MPI wrapper validation

Resolution: 72 × 36 × 8. Grid type: LatitudeLongitudeGrid.
Partition: 3 × 1 × 1; local resolution: 24 × 36 × 8.
Three cores, three MPI ranks, one pinned thread per rank.
Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.
Δt=1 s; one warmup step and two one-step windows.
Free-surface substeps=30, extend_halos=false.
These small-grid validation timings are excluded from the production scaling plot.
