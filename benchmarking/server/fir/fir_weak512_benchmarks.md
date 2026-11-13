# Fir Cartesian 512³ weak scaling

Approved custom study: hydrostatic and nonhydrostatic models, baseline execution
only (no Dagger, no profiling). This opt-in workload does not change Fir's
standard series. Each model has five cases on 1, 2, 4, 8 and 16 H100 GPUs.
Global resolution is `(512 × GPUs) × 512 × 512`, with partition `GPUs × 1 × 1`,
one MPI rank/GPU and one Julia computation thread/rank. Local resolution stays
512³, or 134,217,728 interior cells/GPU.

Both models use Float64 RectilinearGrid, periodic x/y, bounded z, WENO5
momentum/tracer advection, one buoyancy tracer b, no closure or Coriolis.
Cell spacing is 1000 × 1000 × 10 m; the initial domain is
512 km × 512 km × 5.12 km and only x grows. Δt stays 10 s at every count.
Initial conditions are deterministic, with stable stratification
`b = 1e-5*z + 1e-6*cospi(x/64000)*cospi(y/64000)*sinpi(z/5120)`,
u = 0.1 m/s, v = 0.05 m/s and w = 0. Each 512-km x slab has the same workload.

Hydrostatic: SplitRungeKutta3, split-explicit free surface, 30 requested
substeps, extended halos. Record the retained substeps. Nonhydrostatic:
RungeKutta3, rigid lid, default DistributedFFTBasedPoissonSolver. Its x rank
count must divide Ny=512, which all five layouts satisfy. Verify the final
maximum absolute velocity divergence is at most 1e-10 s⁻¹.

Each case verifies distinct GPUs and CUDA-aware MPI communication, runs two
untimed warmup steps followed by five synchronized ten-step timing windows,
and checks finite model fields. Report the maximum rank minimum and median
seconds/step. Weak efficiency is the measured one-GPU time divided by the
measured time; ideal timing is constant and ideal efficiency is 100%.

Use project-local temporary storage and an isolated Julia environment at
`.runtime/environments/fir_weak512`. The OpenMPI temporary alias
`~/.ocean-tmp/weak512` must point to `.runtime/tmp/weak512` inside the checkout.
Prepare the environment with `scripts/env/setup_environment.jl`, then plan:

```bash
python3 benchmarking/scripts/benchmark_suite.py \
  --study .runtime/studies/2026-11-12_fir_weak512 \
  --config benchmarking/server/fir/weak512_config.json \
  --models both --modes baseline --series gpu_weak_scaling_512_x --gpu-only --plan
```

Review the saved configurations before `--study ... --resume`. This study
publishes into a separate `baseline/gpu_weak_scaling_512_x/` series inside
each model's Fir results folder to preserve standard Earth-ocean measurements.
It has ten benchmark jobs plus reporting finalizers; reporting jobs are not
additional benchmark cases. Fresh dated study paths are required for retries.
