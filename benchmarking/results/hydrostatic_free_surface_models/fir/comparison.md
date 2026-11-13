# Fir: hydrostatic baseline versus Dagger

Each case records its execution adapter, version, source hash and options. Ratios require equivalent workload settings and timing contracts; adapter identity may differ. The CSV records the source of each measurement, including any retained reference.

Speedup = baseline seconds per step / Dagger seconds per step. Above 1 favors Dagger; the equal-time reference is 1. Fastest and median timings are the maximum rank statistic. Only completed, validated pairs with matching configurations have ratios.

Nsight timings are compared only against the matching profiled variant. Shared-machine activity can affect timings; these are paired runs, not exclusive-node measurements.

Raw study and execution logs: `/home/anditse/Oceananigans.jl/.runtime/studies/2026-11-12_fir_weak512/hydrostatic_free_surface_models/fir`.

[Baseline records](baseline/plot.md) · [Dagger records](dagger/plot.md) · [All outcomes as CSV](comparison.csv)

## gpu_weak_scaling_512_x

| Case | Resolution / partition | Baseline outcome | Dagger outcome | Median s/step baseline / Dagger | Speedup |
|---|---|---|---|---:|---:|
| 1_ranks | 512x512x512 / 1x1x1 | PENDING | MISSING | — | — |
| 2_ranks | 1024x512x512 / 2x1x1 | PENDING | MISSING | — | — |
| 4_ranks | 2048x512x512 / 4x1x1 | PENDING | MISSING | — | — |
| 8_ranks | 4096x512x512 / 8x1x1 | PENDING | MISSING | — | — |
| 16_ranks | 8192x512x512 / 16x1x1 | PENDING | MISSING | — | — |

No completed, validated pair is available.

1_ranks: baseline: (None); estimated start N/A (scheduler timezone); dagger:

2_ranks: baseline: (None); estimated start N/A (scheduler timezone); dagger:

4_ranks: baseline: (None); estimated start N/A (scheduler timezone); dagger:

8_ranks: baseline: (None); estimated start N/A (scheduler timezone); dagger:

16_ranks: baseline: (None); estimated start N/A (scheduler timezone); dagger:

