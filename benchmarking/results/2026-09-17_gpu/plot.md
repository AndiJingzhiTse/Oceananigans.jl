# GPU benchmark scaling

```mermaid
xychart-beta
    title "Earth ocean benchmark: GPU time per simulated unit"
    x-axis "Grid points" [810000, 3240000, 12960000]
    y-axis "Time per unit (ms)" 0 --> 1600
    line [101.87, 375.16, 1438.83]
```

| Grid | Grid points | Time per unit (ms) |
|---|---:|---:|
| 180 × 90 × 50 | 810,000 | 101.87 |
| 360 × 180 × 50 | 3,240,000 | 375.16 |
| 720 × 360 × 50 | 12,960,000 | 1,438.83 |

All three GPU measurements use latitude longitude geometry.
