# Rondeau benchmark suite

Run `run_rondeau_suite.sh` from a Bash terminal on Rondeau. It can run one series at a time or all series sequentially. It uses the saved Andi 5070 Ti results to choose matching settings.

## Plot saved results

The [2026-09-27 plots](2026-09-27_all/plots.md) show step-time scaling factors across
CPU/GPU resolutions and MPI efficiency across CPU/GPU rank counts,
and Nsight activity pies. Recreate the SVG charts and Markdown tables using
Python 3 with matplotlib:

```bash
python3 benchmarking/results/rondeau/plot_rondeau_results.py
```

Pass another run folder as the positional argument to plot a different complete
suite. The generator reads saved JSON, GPU kernel summaries, and the CPU sample
summary; it does not launch benchmarks. To regenerate the CPU sample summary
from a local Nsight capture first:

```bash
source ~/.config/oceananigans/rondeau-env.sh
nsys export --type=sqlite --output=/tmp/rondeau-cpu.sqlite \
    benchmarking/results/rondeau/2026-09-27_all/nsys_cpu/720x360x50/profile.nsys-rep
python3 benchmarking/results/rondeau/plot_rondeau_results.py --cpu-sqlite /tmp/rondeau-cpu.sqlite
```

GPU pies sum kernel durations using the Andi Gc/Gu/Gv/Others grouping. The CPU
pie counts exclusive leaf-frame samples, grouped by resolved kernel, LLVM,
Julia runtime, other Julia code, other resolved code, or unresolved frames.
Runtime samples can include compilation, garbage collection, and dispatch.
Both capture types include startup and warmup. CPU sample percentages and GPU
kernel-duration percentages measure different activity and should not be
compared directly.

| Series | Global grids or rank counts | Geometry |
|---|---|---|
| CPU resolution | 180 × 90 × 50, 360 × 180 × 50, 720 × 360 × 50 | Latitude longitude for 180 and 360; tripolar for 720 |
| GPU resolution | 180 × 90 × 50, 360 × 180 × 50, 720 × 360 × 50, 1440 × 720 × 50 | Latitude longitude |
| CPU MPI scaling | 720 × 360 × 50 on 1, 2, 4, 8, 16, 32, 64, 128 ranks | Tripolar |
| GPU MPI scaling | 720 × 360 × 50 on 1, 2, 4 GPUs | Tripolar |
| Nsight GPU | 360 × 180 × 50, 720 × 360 × 50 | Tripolar |
| Nsight CPU | 720 × 360 × 50 | Tripolar |

Timing runs use Float64, WENOVectorInvariantDefault, WENO7, CATKE, SplitRungeKutta3, tracers T and S, a 60 second simulation time step, 2 warmup steps, and 5 samples of 10 steps. Nsight runs use 2 warmup steps and 1 sample of 2 steps. CPU profiling uses a sampling period of 1,000,000 CPU cycles with DWARF backtraces. The captured timeline includes startup, compilation, model construction, warmup, and measurement; it is not restricted to the timed window.

The CPU resolution series reproduces the original change in geometry at 720. It therefore does not measure pure resolution scaling. CPU runs use one Julia thread, including each MPI rank. The saved CPU Nsight result also reports one thread; set `PROFILE_CPU_THREADS=16` if you want an additional comparison with 16 threads.

## Configured Rondeau account

For the configured `ajtse` account, load the installed benchmark tools into an existing terminal:

```bash
source ~/.config/oceananigans/rondeau-env.sh
```

New Bash terminals load this file automatically through `~/.bashrc` and `~/.bash_profile`. It selects Julia 1.12.7, CUDA-aware Open MPI 4.1.7, Nsight Systems 2024.5.1, and the installed CUDA 12.3.2 toolkit. The benchmarking environment has its own MPI library preferences in `benchmarking/LocalPreferences.toml`. The system `/usr/bin/mpiexec` does not have CUDA support; use the launcher selected by this environment. CUDA.jl is configured to use CUDA 12.3 artifacts. The account also has an OpenMPI artifact override in `~/.julia/artifacts/Overrides.toml`, so NetCDF/HDF5 dependencies use the same installed MPI library rather than mixing bundled Open MPI 5 with system Open MPI 4. This override applies to the account's Julia depot.

## Prepare the environment

Use the repository revision and Julia version used for the laptop results when possible. The saved results used Julia 1.12.7. Check available resources and tools in your Rondeau terminal:

```bash
hostname
lscpu
nvidia-smi
command -v julia mpiexec nsys
mpiexec --version
nsys --version
nsys status --environment
```

The launcher in this script assumes Open MPI and a single server. Its `--map-by core --bind-to core` settings bind each MPI rank to a separate physical core. Set `CPU_COUNTS` to the counts available to you. GPU runs require NVIDIA CUDA GPUs. Set `CUDA_VISIBLE_DEVICES` to GPUs assigned to you; each MPI rank must see the same complete list, and Oceananigans assigns one GPU to each local rank.

Instantiate and precompile before launching MPI processes:

```bash
julia --project=benchmarking -e 'using Pkg; Pkg.instantiate(); Pkg.precompile()'
```

For MPI scaling, load the server's CUDA aware Open MPI installation and configure MPI.jl to use it. MPIPreferences is included in the benchmarking environment. Select the system library:

```bash
julia --project=benchmarking -e 'using MPIPreferences; MPIPreferences.use_system_binary()'
julia --project=benchmarking -e 'using MPI; MPI.versioninfo(); println("CUDA aware MPI: ", MPI.has_cuda())'
```

This setup updates your Rondeau environment and creates MPI preferences. Start fresh Julia processes afterward. The MPI library loaded by Julia must match the `mpiexec` command. The suite checks rank counts before every MPI run, and GPU checks print rank assignments and perform a reduction on GPU buffers. GPU MPI runs set `JULIA_CUDA_MEMORY_POOL=none` for compatibility with MPI libraries that use legacy CUDA IPC.

See the [MPI.jl configuration guide](https://juliaparallel.org/MPI.jl/stable/configuration/) and [CUDA aware MPI notes](https://juliaparallel.org/MPI.jl/stable/knownissues/#CUDA-aware-MPI). Linux CPU sampling depends on access to the perf subsystem; `nsys status --environment` reports availability. See the [Nsight Systems user guide](https://docs.nvidia.com/nsight-systems/UserGuide/).

## Run the suite

Start in the repository root on Rondeau, optionally inside `tmux` so a disconnected terminal does not stop the run. These examples use your four available GPUs, indices 0 through 3. Substitute the actual indices if they differ.

Preview all commands without launching jobs or creating outputs:

```bash
DRY_RUN=1 bash benchmarking/results/rondeau/run_rondeau_suite.sh all
```

Run the complete suite, including scaling across 1, 2, and 4 GPUs:

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3 bash benchmarking/results/rondeau/run_rondeau_suite.sh all
```

Or launch each series separately:

```bash
bash benchmarking/results/rondeau/run_rondeau_suite.sh cpu_resolution
CUDA_VISIBLE_DEVICES=0 bash benchmarking/results/rondeau/run_rondeau_suite.sh gpu_resolution
CPU_COUNTS="1 2 4 8 16 32 64 128" bash benchmarking/results/rondeau/run_rondeau_suite.sh cpu_scaling
CUDA_VISIBLE_DEVICES=0,1,2,3 bash benchmarking/results/rondeau/run_rondeau_suite.sh gpu_scaling
CUDA_VISIBLE_DEVICES=0 bash benchmarking/results/rondeau/run_rondeau_suite.sh nsys_gpu
bash benchmarking/results/rondeau/run_rondeau_suite.sh nsys_cpu
```

Supported MPI counts and partitions are 1 → 1 × 1 × 1, 2 → 1 × 2 × 1, 4 → 2 × 2 × 1, 8 → 2 × 4 × 1, 16 → 4 × 4 × 1, 32 → 8 × 4 × 1, 64 → 8 × 8 × 1, and 128 → 16 × 8 × 1. The default GPU scaling counts are 1, 2, and 4. Every MPI rank uses one GPU; the global grid stays fixed across counts. Oceananigans assigns the first N GPUs from the visible list to an N rank run.

Each invocation creates a unique folder under `benchmarking/results/rondeau/`. Every configuration has its own `results.json`, generated `results.md`, and `run.log`. The suite also records the repository revision, Julia version, working tree status, CPU information, GPU topology, and the environment manifest when available. MPI results contain one record per rank; use the slowest rank to compute run time, speedup, and efficiency.

Nsight captures and exported databases can be several gigabytes. Store large outputs on the shared data volume by setting `OUTPUT_ROOT` to your directory there:

```bash
OUTPUT_ROOT=/mnt/autofs/sutton.math/fsys2/ajtse/benchmark_results/Rondeau CUDA_VISIBLE_DEVICES=0,1,2,3 bash benchmarking/results/rondeau/run_rondeau_suite.sh all
```

Replace the userid and path if needed. The small reports can later be copied into `benchmarking/results/rondeau/` for comparison. Large profile files remain ignored by Git. Open `profile.nsys-rep` in Nsight Systems. GPU kernel summaries are exported beside the captures and can be grouped into Gc, Gu, Gv, and all other kernels.
