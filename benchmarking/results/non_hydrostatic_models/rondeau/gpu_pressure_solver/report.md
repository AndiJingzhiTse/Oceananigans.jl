# GPU pressure-solver acceptance: Rondeau, 2026-10-29

The initial single-GPU prototype passes the numerical checks but does **not**
accelerate this small acceptance case. These measurements validate the benchmark
and expose overhead; they do not reproduce the paper's distributed pipeline or
establish performance at ocean-model resolutions.

## Fixture and measurement

- Grid: uniform `RectilinearGrid`, **32 × 24 × 16**, extent (2π, 2π, 2π), fully periodic.
- One NVIDIA A100-SXM4-40GB, one MPI rank, partition **1 × 1 × 1**, one Julia computation thread.
- NonhydrostaticModel, Float64, Centered(order=2), RungeKutta3,
  ScalarDiffusivity(ν=0.01), Δt=0.001, no tracers, buoyancy, Coriolis or free surface.
- Three fresh processes per backend, alternating forward/reverse backend order.
  Each process uses two warmups and five windows of ten pressure solves and ten
  timesteps. CUDA synchronization brackets each window. Pressure timings include
  restoring the destructive solver workspace. Construction/compilation is excluded.
- Values below are medians of three process-level medians. Ranges are the
  minimum/maximum of those process medians; they are not confidence intervals.
- Speedup = native timestep seconds / variant timestep seconds; equal time = **1**.
  The three chunked implementations share plans, copies and workspaces.

| Backend | Pressure solve (ms) | Timestep (ms) | Timestep range (ms) | Timestep speedup |
|---|---:|---:|---:|---:|
| Native batched FFT | 0.0583 | 0.8659 | 0.8287–0.8913 | 1.0000 |
| Serial chunks | 1.4734 | 5.0069 | 4.8977–5.1562 | 0.1729 |
| Julia @async chunks | 1.5433 | 5.2474 | 5.0469–5.5486 | 0.1650 |
| Dagger chunks | 3.3177 | 10.8958 | 10.5546–11.3355 | 0.0795 |

All 12 process runs passed pressure residual/solution-error, finite velocity and
post-step divergence checks. The largest relative pressure residual was
1.14699e-15
with tolerance 2.2737367544323206e-11. The largest absolute divergence was
1.10692e-15.
No failed measurements enter this table. The machine was shared; exclusive
access was not claimed.

## Native MPI acceptance

The native benchmark also passed on **2 GPUs**, 2 MPI ranks, partition
**2 × 1 × 1**, global resolution **32 × 24 × 16**, local resolution
**16 × 24 × 16**. Both ranks used distinct allocated GPUs. The recomputed
relative pressure residual was 1.4547409562571969e-15 and maximum divergence
1.0860247781804347e-15. This is a correctness check, not a strong-scaling result.
The Dagger prototype currently supports one local GPU only.

The initial two-rank launch failed before simulation because an OpenMPI launcher
was paired with MPICH. Its evidence is retained in `mpi_setup_failure/`.
After making MPIPreferences a direct environment dependency, the loaded library
and launcher were both verified as OpenMPI 4.1.7, and the retry passed.

## Provenance and limitations

- Benchmark first: `4c35ba17a`; design before implementation: `d41cbe8f2`.
  Three pre-implementation native runs remain in the raw study's `native_baseline/`.
- All four-way comparison records used clean source `eb60b37a5`.
- The successful MPI acceptance used clean source `b87f11f8c`.
  Later provenance guards/metadata additions did not change the FFT algorithm.
- Julia 1.12.7, Oceananigans 0.113.0, CUDA.jl 6.1.0,
  CUDA runtime 12.9.0, reported driver API 12.4.0, Dagger 0.22.7.
- All four single-GPU backends used MPICH 5.0.1 consistently. The separate
  two-GPU acceptance used CUDA-aware system OpenMPI 4.1.7. These two studies
  are not combined into an MPI scaling comparison.
- The prototype retains stage barriers and additional chunk copies. This study
  does not isolate the cost of every component and demonstrates no Dagger gain.
- Bounded boundary conditions, latitude–longitude conjugate gradient, multi-GPU Dagger redistribution,
  full ocean configurations, larger grids and publication-level uncertainty
  analysis remain future work.

[Design and exact commands](../../../../pressure_solver/approach.md) ·
[Process summaries](prototype_comparison/summary.json) ·
[All process outcomes](prototype_comparison/outcomes.json) ·
[Upstream source audit](upstream_audit.json)

Environment snapshots, commands, raw windows and numerical checks are retained
with each study. Snapshots preserve original absolute checkout paths; reproduce
by developing the desired revision in a new isolated environment. File checksums
cover the retained evidence. Raw execution and test logs remain under:

`/local_scratch/ajtse/dagger_poisson/2026-10-29/`

All task temporary data used that data filesystem. An interrupted upstream
package download was removed only after confirming its owning process exited.

## Checks

The final GPU test entry point passed 172 Julia checks (configuration, native
acceptance, chunked inverses and trajectories). The controller acceptance test
also passed. A separate timeout check verified parent/child process termination.
The native MPI acceptance passed on both allocated GPUs. These are benchmark
and prototype checks; the full Oceananigans test suite was not run.
