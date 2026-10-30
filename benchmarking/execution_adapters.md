# Execution adapters

The shared workflow chooses models, series and resources independently of the
execution implementation. `src/suite/backends.py` launches allocated workers
locally or through Slurm. Every worker uses one selected Julia execution adapter;
backend code neither imports Dagger nor chooses its task graph.

The default adapters live in `src/suite/execution/baseline/` and
`src/suite/execution/dagger/`. Baseline calls the synchronized timestep window
directly. Dagger currently spawns that same whole window on the current process
and computation thread, then fetches completion. Model construction, warmup,
outer MPI/GPU synchronization, validation and output remain shared.

## Adapter API, version 1

An adapter directory contains `adapter.json`, `adapter.jl` and any relative Julia
helper files it needs. It must not contain source symlinks. The Julia file defines
a module named `BenchmarkAdapter` with:

- `execute_window!(window!, model, Δt, steps, context)`: execute the requested
  workload and return after all work contributing to this timing window finishes.
- `metadata()`: return a JSON-serializable dictionary containing a
  `"package_versions"` dictionary. Extra method-specific metadata may be included.

`window!(model, Δt, steps, is_gpu, device)` is the common direct implementation.
It selects the assigned CUDA device, advances the model and synchronizes the
task's CUDA stream. An adapter may schedule this callback or implement finer
internal scheduling while preserving the declared workload and timing contract.
It receives the mutable model on its owning MPI process.

The context is a named tuple with `is_gpu`, `device`, `comm`, `rank`, `ranks`,
`configuration` and `options`. It supplies the assigned resources, full resolved
case settings and adapter options. Use only resources inside the supplied local
assignment or Slurm allocation. MPI ownership, synchronization and thread-safety
constraints still apply. Scheduling must not submit separate Slurm jobs.

The current manifest for the whole-function Dagger adapter is:

```json
{
  "api_version": 1,
  "id": "dagger_whole_function",
  "version": "1",
  "mode": "dagger",
  "timing_contract": "oceananigans/timestep_window/v1",
  "dependencies": {
    "Dagger": {
      "uuid": "d58978e5-989f-55fb-8d15-ea34adc7bf54",
      "version": "0.22.7"
    }
  }
}
```

The dependencies are installed only when the isolated environment setup helper
is given `--adapter DIRECTORY`. They do not become root Oceananigans dependencies.
Baseline-only runs do not load or initialize the Dagger adapter. A shared
environment containing Dagger can still be used for both modes.

## Replacing Dagger execution

Create a directory implementing the same API, change its manifest ID/version,
and select it when creating a study:

```bash
python3 benchmarking/scripts/benchmark_suite.py \
  --study .runtime/benchmark_studies/custom-dagger \
  --config benchmarking/server/rondeau/config.json \
  --models both --modes both \
  --dagger-adapter /absolute/path/to/adapter --plan
```

`--dagger-options '{"key":"value"}'` passes a JSON object to that adapter.
The built-in whole-function adapter accepts an empty options object only.
Server configuration may instead provide `dagger_adapter` and `dagger_options`;
a relative adapter path is resolved against the server config folder. No model,
series, backend, baseline or report changes are required to select a replacement.

For cluster environment preparation:

```bash
bash benchmarking/scripts/env/setup.sh nibi --adapter /absolute/path/to/adapter
```

For a local isolated environment, the underlying helper can be used directly:

```bash
julia benchmarking/scripts/env/setup_environment.jl \
  .runtime/environments/benchmark --adapter /absolute/path/to/adapter
```

Set project-controlled temporary storage first, as shown in the
[benchmarking guide](benchmarking_guide.md).
Local setup keeps existing/default MPI preferences when `EBROOTOPENMPI` is unset;
set that variable to the configured system MPI prefix when needed. Select the
resulting environment with the workflow's `--project` option.

## Captures and compatibility

Planning records the manifest, options and a SHA-256 digest of adapter sources
in each case's `execution_adapter`. The selected directory is copied to
`<series>/run_metadata/src/suite/adapter/`; queued jobs execute that copy, not
the original mutable adapter path. Source and frozen configuration checks run
before and after a case. Per-rank results must identify the planned adapter.

Comparisons ignore adapter identity when matching workloads, but require equal
timing contracts and all other workload settings. A replacement measuring a
different unit of work must declare a different contract; such measurements have
no baseline/Dagger ratio until an equivalent baseline is provided. Method IDs,
versions, options, source hashes and package versions remain recorded even when
contracts match. The comparison CSV identifies source records and method IDs.

The implementation is checked by Python workflow/backend tests and
`test/test_execution_adapters.jl`, which exercises the actual direct and Dagger
interfaces. Slurm unit tests simulate scheduler submission, accounting and
finalizers; they do not replace a live cluster validation run.
