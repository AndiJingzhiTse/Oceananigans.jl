# Rondeau benchmark plots

Resolution points show the ratio of adjacent step times. MPI efficiency uses the one-rank step time as its baseline, as in the Andi 5070 Ti reference. The data table directly follows each chart.

## CPU resolution

![CPU resolution chart](cpu_resolution/scaling_factor_scatter.svg)

| Resolution transition | From time (s/step) | To time (s/step) | Measured scaling factor | Grid point ratio |
|---|---:|---:|---:|---:|
| 180 → 360 | 3.126001 | 12.734940 | 4.074× | 4.000× |
| 360 → 720 | 12.734940 | 96.617069 | 7.587× | 4.000× |

The 360 → 720 CPU comparison also changes the grid from latitude longitude to tripolar geometry.

[Method and source data](cpu_resolution/plot.md)

## GPU resolution

![GPU resolution chart](gpu_resolution/scaling_factor_scatter.svg)

| Resolution transition | From time (s/step) | To time (s/step) | Measured scaling factor | Grid point ratio |
|---|---:|---:|---:|---:|
| 180 → 360 | 0.011853 | 0.033800 | 2.852× | 4.000× |
| 360 → 720 | 0.033800 | 0.125816 | 3.722× | 4.000× |
| 720 → 1440 | 0.125816 | 0.503266 | 4.000× | 4.000× |

[Method and source data](gpu_resolution/plot.md)

## CPU scaling

![CPU scaling chart](cpu_scaling/mpi_efficiency.svg)

| CPU ranks | Seconds per step | Steps per second | Speedup | MPI efficiency | Ideal efficiency |
|---:|---:|---:|---:|---:|---:|
| 1 | 99.772836 | 0.010023 | 1.000× | 100.0% | 100.0% |
| 2 | 62.044896 | 0.016117 | 1.608× | 80.4% | 100.0% |
| 4 | 35.604443 | 0.028086 | 2.802× | 70.1% | 100.0% |
| 8 | 18.389982 | 0.054377 | 5.425× | 67.8% | 100.0% |
| 16 | 10.964632 | 0.091202 | 9.100× | 56.9% | 100.0% |
| 32 | 5.835605 | 0.171362 | 17.097× | 53.4% | 100.0% |
| 64 | 3.783972 | 0.264273 | 26.367× | 41.2% | 100.0% |
| 128 | 2.141795 | 0.466898 | 46.584× | 36.4% | 100.0% |

[Method and source data](cpu_scaling/plot.md)

## GPU scaling

![GPU scaling chart](gpu_scaling/mpi_efficiency.svg)

| GPUs | Seconds per step | Steps per second | Speedup | MPI efficiency | Ideal efficiency |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.133612 | 7.484343 | 1.000× | 100.0% | 100.0% |
| 2 | 0.083338 | 11.999351 | 1.603× | 80.2% | 100.0% |
| 4 | 0.060002 | 16.666225 | 2.227× | 55.7% | 100.0% |

[Method and source data](gpu_scaling/plot.md)

## Nsight profiles

GPU pies use summed kernel durations; the CPU pie uses exclusive leaf-frame sample counts. The captures include startup, compilation, warmup and measured steps.

### GPU 360 × 180 × 50

![GPU 360 × 180 × 50 activity pie](nsys_gpu/360x180x50/pie_chart.svg)

| Category | Kernel duration (ns) | Share |
|---|---:|---:|
| Gc | 26,755,487 | 14.65% |
| Gu | 28,111,060 | 15.39% |
| Gv | 27,590,682 | 15.10% |
| Others | 100,213,857 | 54.86% |

[Method and source data](nsys_gpu/360x180x50/plot.md)

### GPU 720 × 360 × 50

![GPU 720 × 360 × 50 activity pie](nsys_gpu/720x360x50/pie_chart.svg)

| Category | Kernel duration (ns) | Share |
|---|---:|---:|
| Gc | 97,432,779 | 14.99% |
| Gu | 117,456,935 | 18.07% |
| Gv | 115,360,793 | 17.74% |
| Others | 319,934,172 | 49.21% |

[Method and source data](nsys_gpu/720x360x50/plot.md)

### CPU 720 × 360 × 50

![CPU 720 × 360 × 50 activity pie](nsys_cpu/720x360x50/pie_chart.svg)

| Category | CPU samples | Share |
|---|---:|---:|
| Unresolved leaf frames | 1,309,480 | 53.10% |
| LLVM compilation | 801,192 | 32.49% |
| Julia runtime / compilation | 169,725 | 6.88% |
| Other Julia code | 120,428 | 4.88% |
| Other resolved code | 65,259 | 2.65% |

[Method and source data](nsys_cpu/720x360x50/plot.md)
