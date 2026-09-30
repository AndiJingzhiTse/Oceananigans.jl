# Rondeau GPU scaling super fine

Timings use the slowest MPI rank at each count. Global grid: 1440 × 720 × 50, plain latitude longitude without bathymetry.
These timing runs use Float64, 60 simulated seconds per step, 2 warmup steps, and 5 samples of 10 steps.

![Measured and ideal MPI efficiency](mpi_efficiency.svg)

| GPUs | Seconds per step | Steps per second | Speedup | MPI efficiency | Ideal efficiency |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.503440 | 1.986335 | 1.000× | 100.0% | 100.0% |
| 2 | 0.257514 | 3.883282 | 1.955× | 97.7% | 100.0% |
| 4 | 0.140908 | 7.096807 | 3.573× | 89.3% | 100.0% |

MPI efficiency = (one-rank step time ÷ current step time) ÷ rank count × 100%. The one-rank measurement is the baseline. The table uses the slowest MPI rank at each count.
