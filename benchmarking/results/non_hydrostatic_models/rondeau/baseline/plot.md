# baseline benchmarks

Each series folder contains its configurations, measurements and provenance. Only completed measurements appear in timing tables and plots.

| Series | Completed cases | Report |
|---|---:|---|
| `gpu_ensemble` | 1 | [Details](gpu_ensemble/plot.md) |
| `gpu_nsight_scaling_default` | 3 | [Details](gpu_nsight_scaling_default/plot.md) |
| `gpu_resolution` | 2 | [Details](gpu_resolution/plot.md) |
| `gpu_scaling_fine` | 3 | [Details](gpu_scaling_fine/plot.md) |
| `gpu_weak_scaling` | 2 | [Details](gpu_weak_scaling/plot.md) |

## gpu_ensemble

Each case runs four independent simulations, one GPU and one MPI rank per simulation. Each has two warmup steps and five windows of ten steps. All four finish warmup before a common timing gate opens. Timed makespan ends when the slowest simulation finishes its windows. Dispatch time includes model construction, compilation, warmup and final validation; worker/package initialization is recorded separately as setup time.

Both variants use direct CUDA/MPI timestepping inside each model. The baseline submits four concurrent Distributed calls; Dagger submits four full-simulation tasks before fetching any. Simulations/hour = 4 × 3600 / timed makespan; each simulation represents a 50-step timing block. These are ensemble throughput measurements on a shared server.

| Resolution per simulation | GPUs / simulations | Outcome | Timed makespan (s) | Dispatch time (s) | Simulations/hour |
|---|---:|---|---:|---:|---:|
| [360 × 180 × 50](gpu_ensemble/default/configuration.md) | 4 / 4 | COMPLETED | 91.9509 | 328.1954 | 156.6053 |

## gpu_nsight_scaling_default

![gpu_nsight_scaling_default](gpu_nsight_scaling_default/gpu_nsight_scaling_default.svg)

![gpu_nsight_scaling_default_kernels](gpu_nsight_scaling_default/gpu_nsight_scaling_default_kernels.svg)

| Case | Ranks | Global resolution | Partition | Fastest / median s per step | Median MPI efficiency | Validation |
|---|---:|---|---|---:|---:|---|
| [1_ranks](gpu_nsight_scaling_default/1_ranks/configuration.md) | 1 | 360 × 180 × 50 | 1 × 1 × 1 | 0.808531 / 1.127963 | 100.0% | Current suite checks |
| [2_ranks](gpu_nsight_scaling_default/2_ranks/configuration.md) | 2 | 360 × 180 × 50 | 2 × 1 × 1 | 1.843828 / 2.828368 | 19.9% | Current suite checks |
| [4_ranks](gpu_nsight_scaling_default/4_ranks/configuration.md) | 4 | 360 × 180 × 50 | 2 × 2 × 1 | 1.883249 / 2.861755 | 9.9% | Current suite checks |

## gpu_resolution

![gpu_resolution](gpu_resolution/gpu_resolution.svg)

| Case | Ranks | Global resolution | Partition | Fastest / median s per step | Median MPI efficiency | Validation |
|---|---:|---|---|---:|---:|---|
| [default](gpu_resolution/default/configuration.md) | 1 | 360 × 180 × 50 | 1 × 1 × 1 | 0.332311 / 0.384814 | — | Current suite checks |
| [fine](gpu_resolution/fine/configuration.md) | 1 | 720 × 360 × 100 | 1 × 1 × 1 | 3.582070 / 4.351423 | — | Current suite checks |

## gpu_scaling_fine

![gpu_scaling_fine](gpu_scaling_fine/gpu_scaling_fine.svg)

| Case | Ranks | Global resolution | Partition | Fastest / median s per step | Median MPI efficiency | Validation |
|---|---:|---|---|---:|---:|---|
| [1_ranks](gpu_scaling_fine/1_ranks/configuration.md) | 1 | 720 × 360 × 100 | 1 × 1 × 1 | 3.499310 / 4.023600 | 100.0% | Current suite checks |
| [2_ranks](gpu_scaling_fine/2_ranks/configuration.md) | 2 | 720 × 360 × 100 | 2 × 1 × 1 | 7.418771 / 8.388280 | 24.0% | Current suite checks |
| [4_ranks](gpu_scaling_fine/4_ranks/configuration.md) | 4 | 720 × 360 × 100 | 2 × 2 × 1 | 4.423683 / 4.997257 | 20.1% | Current suite checks |

## gpu_weak_scaling

![gpu_weak_scaling](gpu_weak_scaling/gpu_weak_scaling.svg)

| Case | Ranks | Global resolution | Partition | Fastest / median s per step | Median MPI efficiency | Validation |
|---|---:|---|---|---:|---:|---|
| [1_ranks](gpu_weak_scaling/1_ranks/configuration.md) | 1 | 360 × 180 × 50 | 1 × 1 × 1 | 0.345378 / 0.383486 | 100.0% | Current suite checks |
| [2_ranks](gpu_weak_scaling/2_ranks/configuration.md) | 2 | 720 × 360 × 100 | 2 × 1 × 1 | 7.732817 / 8.453616 | 18.1% | Current suite checks |
