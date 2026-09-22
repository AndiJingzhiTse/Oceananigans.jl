# Benchmark results

Each benchmark run has its own folder. A run folder may contain:

- `results.json`: machine readable benchmark output
- `results.md`: generated benchmark report
- `plot.md`: plot and compact data table

## Runs

| Folder | Architecture | Configuration |
|---|---|---|
| `2026-09-17_cpu` | CPU | Local Earth ocean benchmarks |
| `2026-09-17_gpu` | NVIDIA GPU | Local Earth ocean benchmarks |
| `2026-09-18_cpu_distributed` | Distributed CPU | Tripolar Earth ocean scaling across MPI ranks |

For future runs, create a new folder and pass its JSON path to the benchmark command. For example:

```powershell
New-Item -ItemType Directory -Path benchmarking/results/2026-09-22_gpu
julia --project=benchmarking benchmarking/run_benchmarks.jl --device=GPU --output=benchmarking/results/2026-09-22_gpu/results.json
```
