# Fir non_hydrostatic_models: dagger

[Server/model overview](../README.md) · [Current workloads](../../../../server/fir/series.json)

Retained measurements belong in `<series>/<case>/`, with configurations,
per-rank results, validation evidence and source/environment provenance.
Raw captures belong in `<series>/raw_profiles/` with checksum manifests and
remain excluded from Git. Closed logs belong in `<series>/run_records/`.

No new-plan measurements were executed as part of the reorganization.
Existing records retain their original settings and validation limits.

The default adapter uses the existing whole-function wrapper. Future adapters record their own method, version and source. Existing wrapper results retain their historical provenance.
