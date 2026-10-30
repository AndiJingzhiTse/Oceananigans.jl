# Shared benchmark workflow requirements

These requirements describe the requested workflow. This document does not
implement the workflow, select a new Dagger algorithm or authorize benchmark
execution. The current implementation status is recorded below.

## Shared scripts across servers

Use one set of benchmark scripts for Rondeau without Slurm and for servers such
as Nibi, Fir and Rorqual with Slurm. Switching server or scheduler must require
only configuration and run selections, with no edits to executable scripts and
no separate copies of model or series code for each server.

Keep the common workflow responsible for planning, model construction, timing,
validation, provenance, result publication and comparison. Put server-specific
resources, environment setup and workload bounds in
`server/<server>/config.json` and `server/<server>/series.json`.
The existing server plans remain authoritative; this requirement does not add
series or change their numerical settings. Rondeau excludes partition series.

## Selectable models and execution modes

Expose these independent selections through one user-facing workflow:

| Selection | Supported values |
|---|---|
| Server | Rondeau, Nibi, Fir, Rorqual and other configured servers |
| Model | HydrostaticFreeSurfaceModel, NonhydrostaticModel, or both |
| Execution mode | Baseline, Dagger, or both |
| Series | All series configured for that server, or a selected subset |

Support any subset of the four model/mode combinations, including a single
combination, both modes for one model, both models in one mode, an explicit
mixed selection, or all four combinations:

| Model | Baseline | Dagger |
|---|---|---|
| HydrostaticFreeSurfaceModel | Selectable | Selectable |
| NonhydrostaticModel | Selectable | Selectable |

Selecting both models and both modes means the full set of four combinations.
Do not launch unselected combinations or automatically add a baseline run when
only Dagger was selected. A plan must list the resolved combinations, cases,
resource requests and output destinations before execution. Resume and reporting
must preserve these selections and the saved workload definitions.

The exact CLI syntax for selecting multiple combinations remains an
implementation choice; this document does not claim new flags already exist.

## Scheduler-independent execution

Choose the execution backend from server configuration. Keep scheduling separate
from model selection, execution mode and the benchmark workload.

| Backend | Responsibilities |
|---|---|
| Local, including Rondeau | Launch on available local resources, respect other users' GPU usage, monitor processes, enforce configured limits and release resources on exit |
| Slurm, including Nibi | Request configured resources through Slurm, record job IDs, launch workers inside the allocation, monitor queue/job states and retain execution evidence |

Both backends must accept the same resolved benchmark cases and execution
interface and produce the same scientific result schema. Baseline and Dagger
must both work through either backend. Local execution must not require Slurm
commands to be installed. Scheduler differences belong in backend adapters,
not duplicated benchmark scripts or special model/Dagger code paths.

Slurm manages allocations and process launches; the Dagger integration manages
its computational tasks within the resources supplied to it. Dagger must not
need its own Slurm submission controller or an independent resource-allocation
workflow. Record requested, allocated and used resources explicitly.

## Replaceable Dagger integration

Keep Dagger weakly coupled through a narrow execution adapter shared by the
local and Slurm backends. The common workflow owns series definitions, model
settings, validation, timing conventions and reporting. The adapter owns how
Dagger executes the selected work.

The adapter must receive the resolved workload/model settings, execution
resources and timing protocol, and return measurements and validation evidence
in the common format. The exact API and internal task granularity are deferred.
Do not make the whole-function wrapper a permanent architectural requirement.

Changing Dagger's scheduling strategy or replacing its implementation must not
require edits to server plans, scheduler adapters, baseline execution, model
selection, result paths or comparison logic, provided the execution contract
and measured workload remain compatible. Baseline-only runs must not initialize
Dagger. Keep Dagger dependencies and initialization inside its integration.

Record the chosen adapter/method, options, source and package versions with
each run so future implementations cannot silently reinterpret older results.
If an implementation changes the workload or timing meaning, record that change
and exclude incompatible speedup comparisons.

## Matched results and comparisons

The configured series themselves are the baseline workloads. Apply Dagger to
the same workloads and reuse model settings, grids, partitions, resource budgets,
initial seeds, timesteps, warmup and measured steps within each comparison.
Model-specific numerical settings remain explicit and shared between modes.

Retain results under:

```text
benchmarking/results/<model_family>/<server>/
├── baseline/<series>/<case>/
├── dagger/<series>/<case>/
├── comparison.md
├── comparison.csv
└── comparisons/
```

Compare Dagger with baseline within the same model and server. Use baseline time
divided by Dagger time, with equal time = 1. Profiled cases compare only with
matching profiled cases. A compatible retained baseline may be used with its
provenance; missing, failed or incompatible cases have no speedup ratio.
Keep historical measurements and their original validation limits intact.

Use the existing shared validation and artifact rules for both backends and
modes. Keep active studies and temporary files in project-controlled storage;
never use `/tmp`, `/var/tmp` or `/local_scratch`. Preserve raw profiles and
execution evidence with checksum manifests and keep large captures out of Git.

## Acceptance criteria for the future implementation

- The same entry point and unchanged scripts can plan and execute configured
  cases locally or through Slurm, using server configuration to choose the backend.
- Model/mode selections resolve correctly for every subset, including all four;
  each combination retains independent status, output and provenance.
- Rondeau and Slurm servers can run both baseline and Dagger through the shared
  workflow; local operation has no Slurm dependency.
- Replacing the Dagger adapter preserves the common interface, server plans and
  baseline behavior, with the new method identifiable in saved results.
- Equivalent cases share validation and reporting, and comparisons never invent
  missing results or combine incompatible measurements.

## Current status and scope

Server configuration, shared workload definitions and the model/server result
layout already exist. `benchmark_suite.py` supports one model and execution
mode per invocation with local or Slurm launch paths. `compare_dagger.py` is
currently a local-only paired controller using the historical Dagger method.

A unified selection interface for multiple model/mode combinations and the
replaceable Dagger execution contract are requirements for future work. The
local-only paired controller is not the intended final shared architecture.
The new Dagger implementation remains unspecified. Documenting these requirements
does not implement that integration or start new benchmark runs.
