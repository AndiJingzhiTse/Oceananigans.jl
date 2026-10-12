# CPU scaling extension provenance

Started at 2026-09-27 20:04:18 UTC on Rondeau. Only CPU scaling at 32, 64,
and 128 ranks was requested; previously saved cases were not rerun.

The captured revision and environment snapshots describe this extension,
not the original suite invocation. `suite.patch` records the local changes
to the launcher relative to the captured revision as a zero-context diff
(`git apply --unidiff-zero`). The manifest is a snapshot.

```bash
source ~/.config/oceananigans/rondeau-env.sh
CPU_COUNTS="32 64 128" OUTPUT_ROOT=/local_scratch/ajtse/rondeau-extensions \
    bash benchmarking/results/rondeau/run_rondeau_suite.sh cpu_scaling
```

Validated results are copied into the parent run's `cpu_scaling/` folders.
All three cases use one Julia thread per rank, a 720 × 360 × 50 tripolar global
grid, Float64, WENOVectorInvariantDefault, WENO7, CATKE, SplitRungeKutta3,
tracers T and S, dt = 60 seconds, two warmup steps, and five samples of ten steps.
Partitions are 8 × 4 × 1, 8 × 8 × 1, and 16 × 8 × 1, respectively.

All three cases completed successfully; the final case finished at 2026-09-27T21:26:36.764Z UTC.
The package manifest matches the original suite snapshot byte for byte. MPI checks
passed, and binding logs showed one distinct physical core per rank in each case.
