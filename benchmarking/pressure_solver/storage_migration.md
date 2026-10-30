# Single-checkout storage migration

Use `/u/ajtse/Oceananigans.jl` for all branch work. The Dagger branch is
`codex/dagger-pressure-solver`; commit changes before switching branches.
All additional Git worktrees have been retired.

Runtime files, environments, temporary files and archives now live in the
ignored `.runtime/` directory in this checkout. The migrated pressure-solver
environment is `.runtime/dagger_pressure/environment/`; its source dependency
now points to this checkout. Set TMPDIR, TMP, TEMP and
OMPI_MCA_orte_tmpdir_base to `.runtime/tmp/` using an absolute path.
Do not create or write anything under `/local_scratch`.

The previous `/local_scratch/ajtse` tree was archived before cleanup:

- Archive: `.runtime/archive/local_scratch-2026-10-29.tar.gz`
- Inventory: `.runtime/archive/local_scratch-2026-10-29.manifest.json`
- Verification: `.runtime/archive/local_scratch-2026-10-29.verified.json`
- Entries verified: 25369
- Compressed bytes: 696478046
- Archive SHA-256: `900a303f8acdfeb81cf1154dc6d8e877d7b86824f74f60f2f8b638e4dc3b7fed`

Each original regular file was checked by SHA-256 against its archived copy;
symlink targets were checked verbatim. An old path under `/local_scratch/ajtse/`
maps to `local_scratch/<relative path>` inside the archive. Old `.git` pointer
files are historical metadata, not additional usable checkouts. All detached
source revisions remain in the `codex/benchmarking` branch history.

Original result records and environment snapshots retain historical paths and
checksums. Use the inventory to locate their archived data; do not rewrite
measurements to make old paths look current. The existing curated Nsight files
inside `benchmarking/results/` remain in place. Large archives are excluded
from Git.

The previously uncommitted Rondeau instructions and Nibi follow-up notes were
committed on `codex/benchmarking` as `438c88577` and preserved in this checkout.
