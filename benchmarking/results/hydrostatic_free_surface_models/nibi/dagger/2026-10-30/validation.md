# Pre-submission validation

- Resolved the pull rebase, preserving all 110 files from the prior Nibi failure-record commit byte-for-byte at their original Nibi paths.
- Shared benchmark suite: 47 tests passed.
- Dagger comparison suite: 7 tests passed.
- Checked all 40 run configurations and all 20 matched pairs: exact GPU counts, canonical fine/super_fine resolutions, identical baseline/Dagger settings except execution mode, valid MPI partitions, and two warmup steps plus five ten-step timing windows.
- Python compilation and shell syntax checks passed.
- Measurements remain pending until Slurm execution and the existing worker/report validation succeed. No pending case is plotted as a completed measurement.
- Setup allocation 25389810 installs Dagger 0.22.7 and precompiles dependencies before any dependent GPU allocation can execute.
