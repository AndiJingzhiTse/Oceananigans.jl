# Historical benchmark launchers

New studies use `../benchmark_suite.py` and its shared `../suite/` planner,
worker and reporting modules. This directory retains the older independent
Nibi and Rondeau controllers to reproduce historical runs and finish queued jobs.

Use their compatibility entry points under `results/nibi/` or `results/rondeau/`.
Python wrappers preserve the original `__file__` and import context, so existing
relative paths, source snapshots and finalizers continue to resolve. Rondeau
shell wrappers supply their original script directory explicitly.

Existing Nibi `.sbatch` files, Julia workers, environment setup and validation
tests remain at their original paths because queued jobs depend on them.
Recorded `run_metadata/` snapshots and benchmark data have not been rewritten.
New features belong in the unified suite rather than these historical controllers.
