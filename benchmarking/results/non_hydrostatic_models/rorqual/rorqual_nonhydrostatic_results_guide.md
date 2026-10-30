# Rorqual: non_hydrostatic_models

[Current server plan](../../../server/rorqual/rorqual_gpu_benchmarks.md) · [Workload definition](../../../server/rorqual/series.json)

- [Baseline](baseline/rorqual_nonhydrostatic_baseline_records.md): direct execution of the server workloads.
- [Dagger](dagger/rorqual_nonhydrostatic_dagger_records.md): the same model, workloads and numerical settings with Dagger.
- `comparison.md`, `comparison.csv`, `comparisons/`: generated matched comparisons inside this model/server folder.

This reorganization runs no new benchmarks. The shared workflow uses a replaceable Dagger adapter.
Existing records, including any comparisons already present, retain their original
series, dates, wrapper method and provenance. They are not certified as completed
measurements of the new plan. Historical root-level series and their `plot.md`
remain at their original paths. No timings were copied or invented for this layout.

Compare baseline and Dagger only for equivalent configurations within this model
and server. Speedup = baseline time / Dagger time; equal time = 1. Missing, failed
or incompatible cases have no ratio. Profiled and unprofiled timings stay separate.
