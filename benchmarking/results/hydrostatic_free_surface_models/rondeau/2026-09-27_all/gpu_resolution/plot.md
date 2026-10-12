# Rondeau GPU resolution

Timings use the saved minimum time per step. All grids use latitude longitude geometry.
These timing runs use Float64, 60 simulated seconds per step, 2 warmup steps, and 5 samples of 10 steps.

![Step-time scaling factor](scaling_factor_scatter.svg)

| Resolution transition | From time (s/step) | To time (s/step) | Measured scaling factor | Grid point ratio |
|---|---:|---:|---:|---:|
| 180 → 360 | 0.011853 | 0.033800 | 2.852× | 4.000× |
| 360 → 720 | 0.033800 | 0.125816 | 3.722× | 4.000× |
| 720 → 1440 | 0.125816 | 0.503266 | 4.000× | 4.000× |

Scaling factor = time per step at the larger resolution ÷ time per step at the smaller resolution. For example, 10 → 45 seconds gives 4.5×. The 4× reference is the ratio of horizontal grid points between adjacent configurations.
