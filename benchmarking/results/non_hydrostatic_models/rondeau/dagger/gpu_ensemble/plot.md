# Four independent single-GPU simulations

Each case runs four independent simulations, one GPU and one MPI rank per simulation. Each has two warmup steps and five windows of ten steps. All four finish warmup before a common timing gate opens. Timed makespan ends when the slowest simulation finishes its windows. Dispatch time includes model construction, compilation, warmup and final validation; worker/package initialization is recorded separately as setup time.

Both variants use direct CUDA/MPI timestepping inside each model. The baseline submits four concurrent Distributed calls; Dagger submits four full-simulation tasks before fetching any. Simulations/hour = 4 × 3600 / timed makespan; each simulation represents a 50-step timing block. These are ensemble throughput measurements on a shared server.

| Resolution per simulation | GPUs / simulations | Outcome | Timed makespan (s) | Dispatch time (s) | Simulations/hour |
|---|---:|---|---:|---:|---:|
| [360 × 180 × 50](default/configuration.md) | 4 / 4 | COMPLETED | 92.1904 | 246.5704 | 156.1984 |
