# Rondeau GPU kernels — 360 × 180 × 50

![Activity breakdown](pie_chart.svg)

Matches the Andi 5070 Ti grouping: hydrostatic free surface Gc, Gu, Gv kernels and all remaining kernels. Shares use summed GPU kernel duration from `kernel_summary_cuda_gpu_kern_sum.csv`, not elapsed wall time. The capture includes startup, warmup and measured steps; concurrent kernel durations can overlap.

| Category | Kernel duration (ns) | Share |
|---|---:|---:|
| Gc | 26,755,487 | 14.65% |
| Gu | 28,111,060 | 15.39% |
| Gv | 27,590,682 | 15.10% |
| Others | 100,213,857 | 54.86% |
