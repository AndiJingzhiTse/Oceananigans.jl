#!/usr/bin/env python3
"""Submit or summarize a four-GPU 1440x720x200 partition comparison on Nibi."""
import argparse
import csv
import fcntl
import math
from pathlib import Path
import re
import shutil
import subprocess
import time

from scaling import read_results
from refresh_scaling import commit_results, TERMINAL

SCRIPT_DIR = Path(__file__).resolve().parent
PARTITIONS = ("4x1x1", "2x2x1", "1x4x1")


def run(*args):
    return subprocess.run(args, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=60)


def submit(folder, account):
    if (folder / "job_id.txt").exists():
        raise SystemExit("This series already has a job; use a new run directory for another allocation")
    metadata = folder / "run_metadata"
    metadata.mkdir(exist_ok=True)
    for name in ("Project.toml", "Manifest.toml", "LocalPreferences.toml"):
        shutil.copy2(SCRIPT_DIR / "environment" / name, metadata / name)
    for name in ("partition_series.py", "partition_series.sbatch", "benchmark.sbatch", "run_benchmark.jl"):
        shutil.copy2(SCRIPT_DIR / name, metadata / name)
    (metadata / "revision.txt").write_text(run("git", "-C", str(SCRIPT_DIR), "rev-parse", "HEAD").stdout)
    result = run("sbatch", "--parsable", f"--account={account}",
                 f"--output={folder}/job.out", str(SCRIPT_DIR / "partition_series.sbatch"),
                 str(folder), str(SCRIPT_DIR))
    (folder / "submission.txt").write_text(result.stdout)
    if result.returncode:
        raise SystemExit(result.stdout)
    job = next(line.strip().split(";")[0] for line in reversed(result.stdout.splitlines())
               if re.fullmatch(r"\d+(;\S+)?", line.strip()))
    (folder / "job_id.txt").write_text(job + "\n")
    print(f"Submitted partition series as Slurm job {job}", flush=True)


def summarize(folder):
    job = (folder / "job_id.txt").read_text().strip()
    accounting = run("sacct", "-X", "-n", "-P", "-j", job,
                     "--format=JobIDRaw,State%40,ExitCode,Reason%200")
    if accounting.returncode:
        raise RuntimeError(accounting.stdout)
    (folder / "accounting.txt").write_text(accounting.stdout)
    records = [line.split("|") for line in accounting.stdout.splitlines()]
    record = next((r for r in records if r[0] == job), None)
    state = record[1].split()[0].rstrip("+") if record else "SUBMITTED"
    queue = run("squeue", "--start", "-h", "-j", job, "-o", "%i|%T|%R|%S")
    if queue.returncode:
        raise RuntimeError(queue.stdout)
    (folder / "queue.txt").write_text(queue.stdout)
    rows = []
    for partition in PARTITIONS:
        decomposition = tuple(map(int, partition.split("x")))
        local_size = tuple(n // p for n, p in zip((1440, 720, 200), decomposition))
        case = folder / partition
        status_file = case / "exit_code.txt"
        if (case / "started.txt").exists():
            status = "RUNNING" if state not in TERMINAL else "INTERRUPTED"
        elif state in TERMINAL:
            status = "NOT_RUN"
        else:
            status = "WAITING" if state == "RUNNING" else state
        details = ""
        fastest = median = slowest = None
        if status_file.exists():
            exit_code = status_file.read_text().strip()
            status = "FAILED"
            details = f"Exit code {exit_code}; see {partition}/job.out"
            if exit_code == "0":
                try:
                    entries = read_results(case, 4, decomposition)
                    for key in ("time_per_step_seconds", "time_per_step_median_seconds", "time_per_step_max_seconds"):
                        if any(not math.isfinite(e[key]) or e[key] <= 0 for e in entries):
                            raise ValueError(f"Invalid timing statistic: {key}")
                    fastest = max(e["time_per_step_seconds"] for e in entries)
                    median = max(e["time_per_step_median_seconds"] for e in entries)
                    slowest = max(e["time_per_step_max_seconds"] for e in entries)
                    status = "COMPLETED"
                    details = "All four MPI rank results verified"
                except (ValueError, KeyError, OSError) as error:
                    status = "INVALID_RESULTS"
                    details = str(error)
        rows.append(dict(partition=partition, local_grid="×".join(map(str, local_size)),
                         state=status, fastest=fastest, median=median, slowest=slowest, details=details))
    with (folder / "partition_results.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    md = ["# Super-fine grid partition comparison", "",
          "Global grid: **1440 × 720 × 200**. Four H100 GPUs, one MPI rank per GPU, on one node.",
          "All three partitions run sequentially within the same allocation, each in a fresh Julia/MPI launch.",
          "Float64, latitude–longitude without bathymetry, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.",
          "Δt = 60 s; two warmup steps, then five windows of ten steps per partition.", "",
          f"Slurm job **{job}**: **{state}**. Whole-series wall-time limit: 30 minutes."]
    if queue.stdout.strip():
        md += ["", "Queue snapshot (America/Toronto): `" + queue.stdout.strip() + "`."]
    measured = [r for r in rows if r["state"] == "COMPLETED"]
    reference = next((r for r in measured if r["partition"] == "2x2x1"), None)
    if measured:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        plt.rcParams.update({"svg.hashsalt": "nibi-partitions", "svg.fonttype": "none"})
        fig, ax = plt.subplots(figsize=(7.2, 4.5))
        x = list(range(len(measured)))
        ax.bar([i - 0.18 for i in x], [r["fastest"] for r in measured], width=0.36,
               label="Fastest window, slowest rank")
        ax.bar([i + 0.18 for i in x], [r["median"] for r in measured], width=0.36,
               label="Median windows, slowest rank")
        ax.set(xticks=x, xticklabels=[r["partition"] for r in measured], ylabel="Seconds per step (lower is faster)",
               xlabel="MPI grid partition", title="Nibi — 1440 × 720 × 200 on four H100 GPUs")
        ax.legend(fontsize=9)
        ax.grid(axis="y", alpha=0.2)
        fig.tight_layout()
        svg = folder / "partition_comparison.svg"
        fig.savefig(svg, metadata={"Date": None})
        svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
        plt.close(fig)
        md += ["", "![Partition timing comparison](partition_comparison.svg)"]
    md += ["", "| Partition | Local grid per rank | State | Fastest s/step | Median s/step | Speedup vs 2×2×1 | Spread |",
           "|---|---|---|---:|---:|---:|---:|"]
    for row in rows:
        if row["fastest"] is not None:
            fastest, median = f"{row['fastest']:.6f}", f"{row['median']:.6f}"
            spread = f"{100 * (row['slowest'] / row['fastest'] - 1):.1f}%"
            speedup = f"{reference['fastest'] / row['fastest']:.3f}×" if reference else "—"
        else:
            fastest = median = spread = speedup = "—"
        md.append(f"| {row['partition']} | {row['local_grid']} | {row['state']} | {fastest} | {median} | {speedup} | {spread} |")
    md += ["", "A window is ten consecutive steps; each window's elapsed time is divided by ten. "
           "The fastest and median statistics are calculated per rank, then the maximum across the four ranks is reported. "
           "Speedup compares the fresh 2×2×1 measurement with each layout. Values above 1 mean faster than 2×2×1. "
           "Spread = (maximum rank/window time ÷ fastest statistic − 1) × 100%.", "",
           "Each partition retains its raw `results.json`, suite report, job log, hardware/modules/revision snapshots, "
           "and exit code. Failed or incomplete partitions are excluded from the chart."]
    for row in rows:
        if row["details"]:
            md += ["", f"{row['partition']}: {row['details']}."]
    (folder / "plot.md").write_text("\n".join(md) + "\n")
    print(f"Job {job}: {state}; " + "; ".join(f"{r['partition']}: {r['state']}" for r in rows), flush=True)
    return state in TERMINAL


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--account", default="def-fpoulin_gpu")
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--poll-seconds", type=int, default=60)
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()
    folder = args.run_dir.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    if args.submit:
        submit(folder, args.account)
    while True:
        with (folder / ".partition.lock").open("a") as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                done = summarize(folder)
            except (BlockingIOError, RuntimeError, subprocess.TimeoutExpired) as error:
                print(f"Refresh deferred: {error}", flush=True)
                if not args.watch:
                    raise SystemExit(1)
                done = False
            else:
                if done and args.commit:
                    commit_results(folder, "codex/nibi-gpu-strong-scaling",
                                   "Record Nibi four-GPU super-fine partition comparison results")
        if done or not args.watch:
            break
        time.sleep(args.poll_seconds)


if __name__ == "__main__":
    main()
