# Distributed CPU benchmark scaling

```mermaid
xychart-beta
    title "Earth ocean benchmark: time per simulated unit"
    x-axis "MPI ranks / CPU cores" [1, 2, 4, 8, 16]
    y-axis "Time per unit (ms)" 0 --> 70000
    line [66266.96, 46150.35, 31254.41, 15739.47, 9113.13]
```

The values are the slowest rank at each core count, which determines the elapsed time of the synchronized distributed simulation.

| CPU cores | Time per unit (ms) |
|---:|---:|
| 1 | 66,266.96 |
| 2 | 46,150.35 |
| 4 | 31,254.41 |
| 8 | 15,739.47 |
| 16 | 9,113.13 |
