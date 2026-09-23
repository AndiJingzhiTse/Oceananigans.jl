# Benchmark results

Each benchmark run has its own folder. A run folder may contain:

- `results.json`: machine readable benchmark output
- `results.md`: generated benchmark report
- `plot.md`: plot and compact data table
- `kernel_summary.csv`: Nsight Systems CUDA kernel summary, when available
- `profile.nsys-rep`: Nsight Systems capture, when available
- `profile.sqlite`: Nsight Systems analysis database, when available

Nsight Systems capture and database files are kept locally and ignored by Git because they can be several gigabytes.

## Runs

| Folder | Architecture | Configuration |
|---|---|---|
| `2026-09-17_cpu` | CPU | Local Earth ocean benchmarks |
| `2026-09-17_gpu` | NVIDIA GPU | Local Earth ocean benchmarks |
| `2026-09-18_cpu_distributed` | Distributed CPU | Tripolar Earth ocean scaling across MPI ranks |
| `2026-09-22_nsys_gpu_720x360x50` | NVIDIA GPU | Nsight Systems profile for a 720 × 360 × 50 tripolar grid |
| `2026-09-23_nsys_gpu_360x180x50` | NVIDIA GPU | Nsight Systems profile for a 360 × 180 × 50 tripolar grid |

For future runs, create a new folder and pass its JSON path to the benchmark command. For example:

```powershell
New-Item -ItemType Directory -Path benchmarking/results/2026-09-22_gpu
julia --project=benchmarking benchmarking/run_benchmarks.jl --device=GPU --output=benchmarking/results/2026-09-22_gpu/results.json
```
