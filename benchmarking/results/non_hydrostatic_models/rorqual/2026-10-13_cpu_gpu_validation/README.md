# Nonhydrostatic functional CPU/GPU MPI validation

LatitudeLongitudeGrid 72 × 36 × 200, rigid lid, standard full-suite model.
CPU: 16 ranks, partition 4 × 4 × 1. GPU: 2 ranks, partition 2 × 1 × 1.
Two untimed steps followed by two windows of two steps; these functional
validation timings are separate from the production five ten-step windows.
The pressure solver uses the same global iteration bound on every rank.
See [status](plot.md).
