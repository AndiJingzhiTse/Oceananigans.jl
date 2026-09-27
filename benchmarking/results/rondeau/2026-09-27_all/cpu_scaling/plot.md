# Rondeau CPU scaling

![Simulation speed](speed.svg)

Timings use the slowest MPI rank at each count.

Speed means simulation steps per second (the reciprocal of step time). Each step advances 60 simulated seconds. These timing runs use Float64, 2 warmup steps, and 5 samples of 10 steps.

![MPI efficiency](mpi_efficiency.svg)

Efficiency = one-rank time / parallel time / rank count × 100%.

| Count | Seconds per step | Steps per second | Speedup | Efficiency |
|---:|---:|---:|---:|---:|
| 1 | 99.772836 | 0.010023 | 1.000× | 100.0% |
| 2 | 62.044896 | 0.016117 | 1.608× | 80.4% |
| 4 | 35.604443 | 0.028086 | 2.802× | 70.1% |
| 8 | 18.389982 | 0.054377 | 5.425× | 67.8% |
| 16 | 10.964632 | 0.091202 | 9.100× | 56.9% |
| 32 | 5.835605 | 0.171362 | 17.097× | 53.4% |
| 64 | 3.783972 | 0.264273 | 26.367× | 41.2% |
| 128 | 2.141795 | 0.466898 | 46.584× | 36.4% |
