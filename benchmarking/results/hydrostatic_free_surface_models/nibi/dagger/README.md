# Nibi baseline / Dagger comparison

The controller runs HydrostaticFreeSurfaceModel and NonhydrostaticModel on
LatitudeLongitudeGrid at fine (720 × 360 × 100) and super_fine
(1440 × 720 × 200), each on 1, 2, 4, 8 and 16 H100 GPUs. Each baseline/Dagger
pair shares one Slurm allocation; pair order alternates by GPU count. Each
variant starts a fresh Julia/MPI process. Baseline does not load Dagger.
Dagger 0.22.7 matches the Rondeau reference environment.

Results for each model are in its own `nibi/dagger/2026-10-30/` directory.
The `baseline/` and `dagger/` children retain independent series records;
`comparison.md` and `comparison.csv` report only validated matched timings.
The suite worker preserves the Rondeau window wrapper: one fetched task scoped
to the current MPI process and its sole Julia computation thread, including
CUDA synchronization. This tests dispatch overhead, not Dagger domain decomposition.

Hydrostatic uses earth_ocean, WENOVectorInvariantDefault, WENO7, CATKE,
SplitRungeKutta3, 30 requested free-surface substeps and extended GPU halos.
Nonhydrostatic uses the shared Rondeau configuration: WENO7, ScalarDiffusivity,
RungeKutta3, a rigid lid and checked CG pressure solves with LocalFFTPreconditioner.
Both use Float64, T/S tracers, Δt=60 s, two untimed steps and five ten-step windows.
Nonhydrostatic initial conditions use seed 1234; hydrostatic retains the existing
unseeded earth_ocean initialization. Paired configurations and partitions match.
Retained substeps, rank placement, local sizes and device memory are in raw results.
Failures, including pressure convergence or GPU memory failures, are retained and
excluded from performance plots. No historical cluster timing substitutes for a run.

From the repository root:

```bash
bash benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/setup.sh
python3 benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/compare_nibi.py
python3 benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/compare_nibi.py --submit --commit
python3 benchmarking/results/hydrostatic_free_surface_models/nibi/dagger/compare_nibi.py --refresh --commit
```

Planning submits nothing. Submission skips cases already submitted. After-any
Slurm finalizers refresh validation, comparisons and plots, then commit the two
Nibi result trees. Failed cases require a fresh `--date` directory for retries.
The Julia environment and temporary files live under the repository's ignored
`.runtime/` directory. Do not change the source checkout while queued jobs use it.
