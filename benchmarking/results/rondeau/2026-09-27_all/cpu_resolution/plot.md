# Rondeau CPU resolution

Timings use the saved minimum time per step. The 180 and 360 grids use latitude longitude geometry; 720 uses tripolar geometry.
These timing runs use Float64, 60 simulated seconds per step, 2 warmup steps, and 5 samples of 10 steps.

![Step-time scaling factor](scaling_factor_scatter.svg)

| Resolution transition | From time (s/step) | To time (s/step) | Measured scaling factor | Grid point ratio |
|---|---:|---:|---:|---:|
| 180 → 360 | 3.126001 | 12.734940 | 4.074× | 4.000× |
| 360 → 720 | 12.734940 | 96.617069 | 7.587× | 4.000× |

Scaling factor = time per step at the larger resolution ÷ time per step at the smaller resolution. For example, 10 → 45 seconds gives 4.5×. The 4× reference is the ratio of horizontal grid points between adjacent configurations.
