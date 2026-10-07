# Report finalizer outcome

Slurm finalizer **23304753** reached its time limit on October 6, 2026.
It repeatedly queried completed benchmark job **23304752** after that job
had disappeared from the live queue. Accounting reported `COMPLETED, 0:0`,
but the live query returned `Invalid job id specified`, preventing finalizer completion.

The benchmark measurements and reports remain in this directory. This was a
report-finalizer failure, not a benchmark failure. The repetitive raw log is
archived at `/scratch/anditse/nibi_archived_logs/2026-10-06_cpu_partition_super_fine/finalize_23304753.out`.
