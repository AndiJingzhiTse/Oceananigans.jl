# Dagger pressure-solver investigation

## Question and scope

Can scheduling independent work **inside** a nonhydrostatic pressure solver
reduce complete timestep time at fixed physics, precision, resolution and GPU count?

This branch starts at `main`, commit `aca5970fa`. The earlier window-wrapper and
four-model ensemble experiments are separate studies. Their timings are not a
baseline for this experiment. The existing benchmark checkout is left intact.
Rondeau CPU benchmark studies remain cancelled.

The initial problem uses a regular `RectilinearGrid`, periodic in all three
directions, with Float64. This intentionally differs from the existing
latitude-longitude ocean benchmark: its conjugate-gradient pressure operator
cannot be replaced by a Cartesian FFT inverse without changing the equation.
Begin with a Cartesian correctness and performance experiment; address the
spherical operator separately after establishing a benefit.

## Benchmark before implementation

`benchmark_pressure_solver.jl` exercises the native solver first. The small
32 × 24 × 16 configuration is an acceptance test, not a scaling result.
Configuration files specify resolution and MPI partition explicitly. The
native path supports horizontal MPI decompositions accepted by Oceananigans.

Two measurements are retained separately:

1. Pressure solves with a fixed right-hand side. Each operation includes copying
   that source into the solver's destructive workspace and the complete solve.
2. Complete `NonhydrostaticModel` timesteps of a decaying Taylor–Green initial
   velocity, with `Centered(order=2)`, `RungeKutta3`, constant viscosity 0.01,
   no tracers, buoyancy, Coriolis or free surface, and timestep 0.001.

The flow and numerical settings are deliberate research-case exceptions to the
ocean benchmark defaults. Every backend uses the same settings. Construction
is recorded separately. Two warmup operations precede five windows of ten
operations. CUDA synchronization brackets each window; MPI barriers occur
before timing, and the maximum rank duration is retained for each window.
The controller launches three fresh processes per backend, reversing backend
order on alternate repetitions. Retain individual runs and report their spread;
five windows in one process are not five independent experiments.

Use native, serial chunks, Julia `@async` chunks, and Dagger-scheduled chunks.
The three chunked variants share FFT batching, copying, workspaces and plans.
Comparing asynchronous Julia tasks against Dagger distinguishes the benefit of
concurrent CUDA streams from the choice of task scheduler. The native
solver remains the practical performance reference. Claim a simulation speedup
only from complete-timestep measurements.

## Acceptance criteria

- Construct a zero-mean pressure `cos(x) cos(2y) cos(3z)` at cell centers and
  generate the source with Oceananigans' **discrete** Laplacian.
- Independently apply that operator to the solved pressure. Record relative
  residual and relative solution error; both must pass the declared roundoff
  allowance `min(sqrt(eps(FT)), 100 eps(FT) max(N)^2)` using the global resolution.
  The cap prevents a meaningless large tolerance at Float32 and large grids.
  This is an accuracy gate for a direct FFT
  inverse, not a modification of the latitude-longitude CG tolerance.
- Require finite velocity fields and bounded absolute discrete divergence
  after the complete timestep sequence.
- Add random zero-mean sources, zero sources, Float32, non-cubic/odd grids,
  repeated solves and reference-trajectory comparisons when adding a backend.
- Reject unsupported grids, boundary conditions, free surfaces and resource
  placement explicitly. Do not substitute another operator or precision.
- Validate every MPI rank and distinct allocated GPU UUIDs. Preserve failed
  runs; exclude them from speedup calculations.

## Implementation sequence

1. Commit the native benchmark and its acceptance tests.
2. Commit this design and the upstream-source audit before adding solver code.
3. Build a benchmark-local, single-GPU periodic solver prototype with cached
   chunk workspaces and FFT plans. Schedule independent chunks within each
   transform stage. Use identical serial chunks as a control. Explicitly wait
   for device completion before dependent stages read their output.
4. Profile that prototype. Stage barriers, extra copies and small GPU tasks can
   erase any concurrency benefit. This milestone does not implement the
   paper's distributed redistribution pipeline and is not a reproduction.
5. Investigate an adapter to the authors' DaggerFFT backend and progressive
   MPI redistribution on 2 and 4 GPUs. Check API compatibility, Fourier layout,
   normalization, nullspace, plan/stream ownership and CUDA-aware MPI with
   real device-buffer communication tests before accepting results.
6. Consider a package extension and an upstream PR only after correctness and
   repeatable complete-timestep gains. Keep experimental dependencies outside
   the root `Project.toml` while the design remains unsettled.

## Upstream audit

Paper: <https://arxiv.org/html/2601.12209v1>, especially sections IV, V and VI-B.
It replaces FFT routines in Oceananigans' pressure solver and combines task
scheduling with communication and workspace changes; wrapping a full timestep
does not expose those operations to the scheduler.

The authors publish <https://github.com/sanatgp/DaggerFFT.jl>, inspected at
`8c0230efb1aaec998570c40241aadfcec20f52be`. This is distinct from the older
<https://github.com/sanatgp/DaggerFFT> benchmarking repository.
The package's declared Dagger compatibility is `0.18.14`, while its GPU
benchmark invokes `Dagger.MPIAcceleration` and `Dagger.accelerate!`.
Its GPU source exposes `gpu_fft!`/`gpu_ifft!` over stage-specific DArrays and
persistent workspaces; integration must follow the actual source API, rather
than assume the high-level README example is sufficient. Package loading and
runtime compatibility need experimental verification. Do not silently patch
the dependency declarations and call the result the published implementation.

The declared dependency resolved to Dagger 0.18.16 during the initial setup
attempt. Its installed source has no `Acceleration`/`MPIAcceleration` API,
while DaggerFFT imports `Acceleration` and uses the newer MPI interface.
This is a source-level compatibility concern, not a completed package-load
test. The isolated upstream installation was stopped after 608 seconds while
downloading dependencies; no upstream DaggerFFT execution result is claimed.

A candidate explanation is the author's own Dagger fork:
<https://github.com/sanatgp/Dagger.jl/tree/4a1b8fa7640918023117ff18eb7c21b39cc062ae>.
Its `DaggerFFT` branch declares version 0.18.14 and includes the MPI acceleration
API missing from the registered release. Pin and test this fork explicitly
before attributing results to the authors' implementation; its relationship
to the exact paper build has not been verified. An older Oceananigans integration
is also available at <https://github.com/sanatgp/Oceananigans.jl/tree/06227c5bf215>.
That source uses global host gathers and older solver signatures, so it requires
an independent correctness and data-movement review before adaptation.

The first prototype is our own benchmark-local chunked solver on Dagger 0.22.7.
It does not vendor or modify DaggerFFT. Each chunk owns a CUDA stream, buffer
and transform plans; the serial control waits after each chunk, while Dagger
submits all disjoint chunks in a stage before fetching. Both retain stage
barriers. Multi-GPU redistribution and bounded transforms remain future work.
The `async_chunks` control submits the same work with Julia `@async`, retaining
the same streams and waits. Dagger must also beat this concurrent control to
support a claim about a benefit from its scheduler specifically.

Run the native and prototype GPU acceptance tests together:

```sh
julia --threads=1 --project=benchmarking/pressure_solver benchmarking/pressure_solver/runtests.jl
python3 -m unittest discover -s benchmarking/test -p 'test_pressure_solver_study.py'
```

For the first four-way comparison, add
`--backends native serial_chunks async_chunks dagger_chunks` to the controller.
The prototype supports one local GPU only; the native backend supports MPI.

## Running and storage

Execute from a data filesystem. All four temporary variables must resolve
outside `/tmp` and `/var/tmp`, including through symlinks. Set them before
Julia/package setup, tests or child processes start. Large files and environments
belong under `/local_scratch/ajtse/dagger_poisson/`; only small validated records
should be retained under
`benchmarking/results/non_hydrostatic_models/rondeau/gpu_pressure_solver/`.

Example setup (Julia 1.11+ supports `[sources]`; on 1.10 explicitly `Pkg.develop`
the checkout path in the isolated environment):

```sh
export TMPDIR=/local_scratch/ajtse/dagger_poisson/tmp
mkdir -p "$TMPDIR"
export TMP="$TMPDIR" TEMP="$TMPDIR" OMPI_MCA_orte_tmpdir_base="$TMPDIR"
export JULIA_NUM_PRECOMPILE_TASKS=1 OPENBLAS_NUM_THREADS=1
julia --project=benchmarking/pressure_solver -e 'using Pkg; Pkg.instantiate()'
export CUDA_VISIBLE_DEVICES=GPU_UUID_OF_AN_AVAILABLE_DEVICE
julia --threads=1 --project=benchmarking/pressure_solver benchmarking/test/test_pressure_solver.jl
```

Run the controller with the actual allocated GPU UUIDs (use `--plan` to inspect
commands without launching). It defaults to native-only measurements until a
backend is explicitly selected:

```sh
python3 benchmarking/scripts/pressure_solver_study.py \
  --config benchmarking/pressure_solver/smoke.toml \
  --project benchmarking/pressure_solver \
  --output /local_scratch/ajtse/dagger_poisson/native-study \
  --gpus GPU_UUID_OF_AN_AVAILABLE_DEVICE --repeats 3 --timeout 600
```

Use a fresh output directory: the controller refuses to overwrite a study.
For MPI runs, provide one UUID per rank and an explicit compatible partition.
Configure `MPIPreferences` in this isolated project and verify
`MPI.Get_library_version()` against `mpiexec --version` before launching ranks.
On Rondeau, use the CUDA-aware OpenMPI library and launcher together:

```sh
julia --project=benchmarking/pressure_solver -e 'using MPIPreferences; MPIPreferences.use_system_binary(library_names=["/opt/uw/openmpi/4.1.7-with-cuda/lib/libmpi.so"], mpiexec="/opt/uw/openmpi/4.1.7-with-cuda/bin/mpiexec")'
julia --project=benchmarking/pressure_solver -e 'using MPI; println(MPI.Get_library_version())'
/opt/uw/openmpi/4.1.7-with-cuda/bin/mpiexec --version
```

The initial two-rank acceptance attempt caught MPICH loaded under an OpenMPI
launcher and stopped in MPI initialization. `MPIPreferences` is an explicit
project dependency so the project's stored binding preferences are applied.
Retain this setup failure separately from numerical failures. The completed
single-GPU comparison used MPICH consistently for all four backends; it is
not a cross-library MPI scaling comparison.

Each rank records its GPU, thread count, MPI library, source revision, dirty
state, configuration and accuracy checks. The study retains environment files,
exact commands, logs, per-case outcomes and file checksums. Setup and compilation
are excluded from warmed execution timings. Stop on numerical, resource or
timeout failures; the timeout terminates the owning process group.

Shared-server results do not establish exclusive access. Begin on one available
GPU with a ten-minute per-process limit, record observed durations, and obtain
resource availability before extending to larger allocations. No background
multi-day run is needed for this first milestone.
