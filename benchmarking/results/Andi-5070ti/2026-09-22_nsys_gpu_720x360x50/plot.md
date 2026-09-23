# Nsight GPU kernel time breakdown

![Pie chart of GPU kernel time for the 720 × 360 × 50 benchmark](pie_chart.svg)

| Component | GPU kernel time |
|---|---:|
| Gc | 28.0% |
| Gu | 15.1% |
| Gv | 14.9% |
| Others | 42.0% |

Gc, Gu, and Gv contain the total times for CUDA kernels whose names begin with `gpu_compute_hydrostatic_free_surface_Gc_`, `gpu_compute_hydrostatic_free_surface_Gu_`, and `gpu_compute_hydrostatic_free_surface_Gv_`. Others contains the remaining GPU kernel time. Values come from `kernel_summary.csv`.
