# One-GPU attempt — 1440 × 720 × 200

The Float64 latitude-longitude case failed during model construction on
2026-10-05, before warmup or measurement. CUDA could not allocate another
1.702 GiB while using 37.877 / 39.381 GiB of effective A100 memory.

No timing result is available for this grid on one GPU. The previous
1440 × 720 × 50 result was removed when this series was replaced.
The complete error remains in the local, ignored `run.log`.

See [rerun provenance](../rerun.md) for settings and commands.
