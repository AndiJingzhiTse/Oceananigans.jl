# Initial Nibi strong-scaling run — October 5, 2026

New 8-, 16-, 64-, and 128-GPU attempts were submitted later on October 5.
See [current follow-up status](retry_status.md) for their job IDs and outcomes.
The initial run is documented below; its cancelled-attempt evidence is
preserved under `previous_attempts/<job_id>/` in each retried count.

**Highest successful count: 32 H100 GPUs on four nodes.** The fixed global
grid was 1440 × 720 × 200 (207,360,000 cells). The slowest rank's fastest
window was **0.098326 s/step**, versus **1.021135 s/step** on one GPU:
**10.39× speedup and 32.5% MPI efficiency**.

See the [efficiency plot and complete timing table](plot.md),
[SVG](mpi_efficiency.svg), and [attempt log](attempts.csv).

## What completed and what prevented going further

| GPUs | Outcome | Evidence |
|---:|---|---|
| 1 | Completed; all rank results verified | [Results](1_gpus/results.json), [job log](1_gpus/job.out) |
| 2 | Completed; all rank results verified | [Results](2_gpus/results.json), [job log](2_gpus/job.out) |
| 4 | Completed; all rank results verified | [Results](4_gpus/results.json), [job log](4_gpus/job.out) |
| 8 | Submitted, stayed pending with `Priority`; cancelled under the user's instruction to finish with the largest completed count | [Queue snapshot](8_gpus/previous_attempts/23239392/queue_before_cancel.txt), [accounting](8_gpus/previous_attempts/23239392/accounting.txt) |
| 16 | Submitted, stayed pending with `Priority`; cancelled under the same instruction | [Queue snapshot](16_gpus/previous_attempts/23239393/queue_before_cancel.txt), [accounting](16_gpus/previous_attempts/23239393/accounting.txt) |
| 32 | Completed; all 32 rank results verified | [Results](32_gpus/results.json), [job log](32_gpus/job.out) |
| 64 | Submitted, stayed pending with `Priority`; estimated start 03:10 on October 5; cancelled under the user's instruction | [Queue snapshot](64_gpus/previous_attempts/23239396/queue_before_cancel.txt), [accounting](64_gpus/previous_attempts/23239396/accounting.txt) |
| 128 | Feasibility check accepted; estimated start 21:24 on October 6; not submitted because of the long wait | [Slurm feasibility output](run_metadata/feasibility_128.txt) |
| 256 | Actual submission rejected: `Requested node configuration is not available` | [Submission output](256_gpus/submission.txt), [exit code](256_gpus/submission_exit_code.txt) |

All times above and in queue snapshots use **America/Toronto (EDT)**.
At cancellation, the 8- and 16-GPU estimates were 03:20 and 01:30 on
October 5 respectively. Estimates changed during the run; these snapshots
are observations of scheduler state, not guaranteed start times.

The sweep stopped at a **queue constraint**, rather than an observed
application or MPI failure at 64 GPUs. The scheduler ran 32 GPUs before
8 and 16 GPUs, so those intermediate counts remain unmeasured. The plot
leaves gaps rather than interpolating through them. No timings were copied
from the historical Nibi guide.

The separate **capacity constraint at 256 GPUs** is supported by Nibi's
[node inventory](run_metadata/node_inventory.txt): 29 nodes advertise
`gpu:h100:8`, totaling 232 full H100 GPUs, while 256 GPUs would require
32 such nodes. MIG devices and MI300A GPUs do not satisfy an `h100:1`
per-task request. This run demonstrates success up to 32 GPUs; it does
not establish an application scaling limit at 32, 64, or 128 GPUs.

## Method and reproducibility

The model and timing parameters match the Rondeau `gpu_scaling_super_fine`
reference, with the requested depth increased from 50 to 200 levels:
Float64; plain latitude–longitude without bathymetry;
WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3;
Δt = 60 s; two warmup steps; five windows of ten steps.
All counts use `Distributed(GPU())`, including the baseline.

Horizontal partitions are 1×1, 1×2, 2×2, 4×2, 4×4, 8×4,
8×8 for 1, 2, 4, 8, 16, 32, 64 GPUs respectively. Both horizontal
dimensions divide evenly; the successful 32-GPU local grid is
180 × 180 × 200. Counts use one MPI rank per GPU, up to eight GPUs per
node, eight CPUs per rank, and one Julia/OpenBLAS thread per rank.
The measured runs requested 64 GiB host memory for partial nodes and
all node memory for full nodes. Wall-time requests were shortened to
fit backfill windows, without changing benchmark parameters.

Each successful job first verified distinct GPU UUIDs and a CUDA-aware
MPI ring exchange, including across four nodes at 32 GPUs. Then the
suite timed the model and saved results from every rank. The validator
checked rank completeness, local grid sizes, precision, samples,
steps, Δt, and finite positive timings. Timing statistics and their
aggregation across ranks are described in [plot.md](plot.md).

Jobs were queued together and ran on different nodes when Slurm allowed.
The 1/2/4-GPU jobs requested partial nodes, allowing other allocations to share them. The 32-GPU
job occupied four full GPU nodes. No profiling was performed to separate
communication overhead from GPU kernel overhead at 32 GPUs.

Software: Julia 1.10.10, this Oceananigans 0.113.0 checkout,
CUDA.jl 6.1.0, MPI.jl 0.20.27, OpenMPI_jll 4.1.9 redirected to system
OpenMPI 4.1.5. Modules: StdEnv/2023, gcc/12.3, openmpi/4.1.5,
cuda/12.6, julia/1.10.10. The GPU is NVIDIA H100 80GB HBM3.
The [manifest](run_metadata/Manifest.toml),
[MPI preferences](run_metadata/LocalPreferences.toml), DRAC helper,
module/GPU snapshots, launch scripts, and revisions are retained.
The suite reports zero GPU memory for distributed runs; GPU identity
is instead evidenced by the UUID checks and hardware snapshots.

The first 1/2/4-GPU jobs passed transport checks but produced no benchmark
timings because the included suite's entry-point guard did not invoke
`main()`. This was corrected, all three jobs were rerun, and the validator
rejected the initial jobs. Their logs are preserved in
`initial_transport_only/` under each count. They are excluded from the plot.
Initial and final launch-script snapshots are distinguished in `run_metadata/`.

All initial benchmark jobs finished or were cancelled. New attempts are
tracked in [retry_status.md](retry_status.md) and [attempts.csv](attempts.csv).
Use the [parent instructions](../README.md) to monitor or rerun the sweep.
