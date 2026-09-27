# Rondeau GPU resolution

![Simulation speed](speed.svg)

Timings use the saved minimum time per step. All grids use latitude longitude geometry.

Speed means simulation steps per second (the reciprocal of step time). Each step advances 60 simulated seconds. These timing runs use Float64, 2 warmup steps, and 5 samples of 10 steps.

![Adjacent resolution scaling](scaling_factor_scatter.svg)

| Grid | Grid points | Seconds per step | Steps per second | Time ratio to previous |
|---|---:|---:|---:|---:|
| 180 × 90 × 50 | 810,000 | 0.011853 | 84.365500 | — |
| 360 × 180 × 50 | 3,240,000 | 0.033800 | 29.585654 | 2.852× |
| 720 × 360 × 50 | 12,960,000 | 0.125816 | 7.948143 | 3.722× |
| 1440 × 720 × 50 | 51,840,000 | 0.503266 | 1.987020 | 4.000× |
