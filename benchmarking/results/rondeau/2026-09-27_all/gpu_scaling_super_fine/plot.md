# Rondeau GPU scaling super fine

Timings use the slowest MPI rank at each count. Global grid: 1440 × 720 × 200, plain latitude longitude without bathymetry.
These timing runs use Float64, 60 simulated seconds per step, 2 warmup steps, and 5 samples of 10 steps.

![Measured and ideal MPI efficiency](mpi_efficiency.svg)

| GPUs | Seconds per step | Steps per second | Speedup vs 2 GPUs | MPI efficiency | Ideal efficiency |
|---:|---:|---:|---:|---:|---:|
| 2 | 0.991023 | 1.009058 | 1.000× | 100.0% | 100.0% |
| 4 | 0.517122 | 1.933778 | 1.916× | 95.8% | 100.0% |

MPI efficiency is relative to the 2-GPU baseline: (baseline step time ÷ current step time) × 2 ÷ GPU count × 100%. The baseline is normalized to 100%; this does not measure efficiency relative to one GPU. Timings use the slowest rank.

The [one-GPU case](1_gpus/attempt.md) ran out of memory before warmup; no one-GPU timing is available.

[Rerun provenance](rerun.md) records the replacement measurements and any failed configurations.
