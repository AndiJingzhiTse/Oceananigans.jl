# Rondeau CPU resolution

![Simulation speed](speed.svg)

Timings use the saved minimum time per step. The 180 and 360 grids use latitude longitude geometry; 720 uses tripolar geometry.

Speed means simulation steps per second (the reciprocal of step time). Each step advances 60 simulated seconds. These timing runs use Float64, 2 warmup steps, and 5 samples of 10 steps.

![Adjacent resolution scaling](scaling_factor_scatter.svg)

| Grid | Grid points | Seconds per step | Steps per second | Time ratio to previous |
|---|---:|---:|---:|---:|
| 180 × 90 × 50 | 810,000 | 3.126001 | 0.319897 | — |
| 360 × 180 × 50 | 3,240,000 | 12.734940 | 0.078524 | 4.074× |
| 720 × 360 × 50 | 12,960,000 | 96.617069 | 0.010350 | 7.587× |
