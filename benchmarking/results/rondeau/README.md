# Rondeau benchmarks

[Setup and suite commands](rondeau.md) describe the configuration and environment.

| Run | Status | Results |
|---|---|---|
| [2026-09-27 suite](2026-09-27_all/README.md) | Timing series and GPU profiles complete; CPU profiling failed | CPU/GPU resolution, MPI scaling, and GPU kernel summaries |

Curated runs retain JSON results, generated Markdown reports, GPU kernel summaries,
and small environment snapshots. Raw `run.log` files, working-tree snapshots,
Nsight captures, and SQLite databases remain local and are ignored by Git.
Run folders are named by their UTC start date; suite-generated folders also include
the start time and process ID to keep separate invocations unique.
