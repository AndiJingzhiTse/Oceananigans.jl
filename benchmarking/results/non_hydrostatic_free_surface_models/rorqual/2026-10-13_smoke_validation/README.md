# Nonhydrostatic CPU/GPU MPI smoke validation

Validation only, separate from production timings:

- CPU: two ranks, 72 × 36 × 8, partition 2 × 1 × 1.
- CPU: sixteen ranks, 72 × 36 × 200, partition 4 × 4 × 1.
- GPU: two ranks, 72 × 36 × 200, partition 2 × 1 × 1.

Each allocation has a 20-minute limit and uses the full suite model/worker.
The additional 200-level cases check the production vertical discretization.
See [status](plot.md).
