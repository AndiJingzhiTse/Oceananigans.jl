# Rondeau benchmarks

[Setup and suite commands](rondeau.md) describe the configuration and environment.

| Run | Status | Results |
|---|---|---|
| [2026-09-27 suite](2026-09-27_all/README.md) | All timing series and profiles complete | [Charts](2026-09-27_all/plots.md), CPU/GPU resolution, MPI scaling, and Nsight summaries |

Curated runs retain JSON results, generated Markdown reports, GPU kernel summaries,
CPU sample summaries, charts, and small environment snapshots. Raw `run.log` files, working-tree snapshots,
Nsight captures, and SQLite databases remain local and are ignored by Git.
Run folders are named by their UTC start date; suite-generated folders also include
the start time and process ID to keep separate invocations unique.
