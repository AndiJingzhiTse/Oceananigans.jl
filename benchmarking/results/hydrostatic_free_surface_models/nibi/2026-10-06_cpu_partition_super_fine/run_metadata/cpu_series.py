#!/usr/bin/env python3
"""Submit, validate, and plot Nibi CPU scaling and four-node partition series."""
import argparse
import csv
import fcntl
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import time

from scaling import partition_for, read_results
from refresh_scaling import TERMINAL, commit_results

SCRIPT_DIR = Path(__file__).resolve().parent
BRANCH = "codex/nibi-gpu-strong-scaling"
PARTITIONS = ("4x1x1", "2x2x1", "1x4x1")


def run(*args):
    return subprocess.run(args, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=60)


def job_id(output):
    return next(line.strip().split(";")[0] for line in reversed(output.splitlines())
                if re.fullmatch(r"\d+(;\S+)?", line.strip()))


def save_jobs(folder, jobs):
    temporary = folder / "jobs.json.tmp"
    temporary.write_text(json.dumps(jobs, indent=2) + "\n")
    temporary.replace(folder / "jobs.json")


def submit(folder, mode):
    if (folder / "jobs.json").exists():
        raise SystemExit("Series already submitted; use a new directory for a new series")
    metadata = folder / "run_metadata"
    metadata.mkdir(exist_ok=True)
    for name in ("Project.toml", "Manifest.toml", "LocalPreferences.toml"):
        shutil.copy2(SCRIPT_DIR / "environment" / name, metadata / name)
    for name in ("cpu_series.py", "cpu_series.sbatch", "cpu_benchmark.sh", "run_cpu_benchmark.jl",
                 "finalize_cpu.sbatch", "scaling.py", "refresh_scaling.py"):
        shutil.copy2(SCRIPT_DIR / name, metadata / name)
    (metadata / "revision.txt").write_text(run("git", "-C", str(SCRIPT_DIR), "rev-parse", "HEAD").stdout)
    (metadata / "partitions.txt").write_text(run("scontrol", "show", "partition", "cpubase_bynode_b1").stdout)
    jobs = []
    if mode == "scaling":
        # Probe the next power of two without submitting an impossible allocation.
        probe = run("sbatch", "--test-only", "--account=def-fpoulin_cpu", "--partition=cpubase_bynode_b1",
                    "--nodes=1024", "--ntasks-per-node=1", "--cpus-per-task=192", "--mem=0",
                    "--time=01:00:00", "--wrap=true")
        (metadata / "1024_nodes_probe.txt").write_text(
            "Test-only Slurm request: 1024 nodes, 196608 cores, one rank/node, 192 cores/rank, mem=0, time=01:00:00.\n"
            f"Return code: {probe.returncode}\n{probe.stdout}"
            "Also: 1024 horizontal ranks cannot evenly divide 1440x720 (maximum power of two is 512).\n")
        cases = [(n, ["x".join(map(str, (*partition_for(n), 1)))]) for n in (1, 2, 4, 8, 16, 32, 64, 128, 256, 512)]
    else:
        cases = [(4, list(PARTITIONS))]
    (folder / "mode.txt").write_text(mode + "\n")
    for nodes, partitions in cases:
        destination = folder / f"{nodes}_nodes" if mode == "scaling" else folder
        destination.mkdir(exist_ok=True)
        result = run("sbatch", "--parsable", "--account=def-fpoulin_cpu", "--partition=cpubase_bynode_b1",
                     f"--job-name=nibi_cpu_{mode}_{nodes}", f"--nodes={nodes}", f"--ntasks={nodes}",
                     f"--time={'03:00:00' if mode == 'partition' else '01:00:00'}",
                     f"--output={destination}/job.out", str(SCRIPT_DIR / "cpu_series.sbatch"),
                     str(destination), str(SCRIPT_DIR), *partitions)
        (destination / "submission.txt").write_text(result.stdout)
        record = dict(nodes=nodes, cores=192 * nodes, partitions=partitions,
                      folder=str(destination.relative_to(folder)), job_id="",
                      state="SUBMISSION_FAILED" if result.returncode else "SUBMITTED")
        if not result.returncode:
            record["job_id"] = job_id(result.stdout)
            (destination / "job_id.txt").write_text(record["job_id"] + "\n")
        jobs.append(record)
        save_jobs(folder, jobs)  # Preserve every accepted allocation if a later call fails.
        print(f"{nodes} CPU nodes ({192 * nodes} cores): {record['state']} {record['job_id']}", flush=True)
        if result.returncode:
            break
    ids = [j["job_id"] for j in jobs if j["job_id"]]
    if ids:
        finalizer = run("sbatch", "--parsable", "--account=def-fpoulin_cpu",
                        "--dependency=afterany:" + ":".join(ids), f"--output={folder}/finalize.out",
                        str(SCRIPT_DIR / "finalize_cpu.sbatch"), str(folder), str(SCRIPT_DIR))
        (metadata / "finalizer_submission.txt").write_text(finalizer.stdout)
        if finalizer.returncode:
            raise RuntimeError("Benchmarks submitted, but finalizer submission failed: " + finalizer.stdout)
        (metadata / "finalizer_job_id.txt").write_text(job_id(finalizer.stdout) + "\n")


def affinity_count(value):
    count = 0
    seen = set()
    for item in value.strip().split(","):
        edges = list(map(int, item.split("-")))
        if len(edges) not in (1, 2) or min(edges) < 0:
            raise ValueError("Invalid CPU affinity")
        cpus = set(range(edges[0], edges[-1] + 1))
        if not cpus or seen.intersection(cpus):
            raise ValueError("Invalid or overlapping CPU affinity")
        seen.update(cpus)
        count += len(cpus)
    return count


def validate(case, nodes, partition):
    entries = read_results(case, nodes, tuple(map(int, partition.split("x"))))
    layout = json.loads((case / "cpu_layout.json").read_text())
    if (len(layout) != nodes or {r["rank"] for r in layout} != set(range(nodes))
            or len({r["hostname"] for r in layout}) != nodes):
        raise ValueError("Expected one MPI rank on each distinct CPU node")
    for rank in layout:
        if rank["threads"] != 192 or rank["cpus_per_task"] != 192 or affinity_count(rank["cpu_affinity"]) != 192:
            raise ValueError("Expected 192 threads bound to 192 cores per rank")
    for entry in entries:
        if entry["metadata"]["num_threads"] != 192:
            raise ValueError("Benchmark did not use 192 Julia threads")
        timings = [entry[k] for k in ("time_per_step_seconds", "time_per_step_median_seconds", "time_per_step_max_seconds")]
        if any(not math.isfinite(t) or t <= 0 for t in timings) or timings != sorted(timings):
            raise ValueError("Invalid timing statistics")
    return max(e["time_per_step_seconds"] for e in entries), max(e["time_per_step_median_seconds"] for e in entries)


def refresh(folder):
    jobs = json.loads((folder / "jobs.json").read_text())
    mode = (folder / "mode.txt").read_text().strip()
    ids = [j["job_id"] for j in jobs if j["job_id"]]
    records, queued = {}, {}
    if ids:
        accounting = run("sacct", "-X", "-n", "-P", "-j", ",".join(ids), "--format=JobIDRaw,State%40,ExitCode,Reason%200")
        queue = run("squeue", "--start", "-h", "-j", ",".join(ids), "-o", "%i|%T|%R|%S")
        if accounting.returncode or queue.returncode:
            raise RuntimeError(accounting.stdout + queue.stdout)
        (folder / "accounting.txt").write_text(accounting.stdout)
        (folder / "queue.txt").write_text(queue.stdout)
        records = {r[0]: r for line in accounting.stdout.splitlines() if len(r := line.split("|")) >= 4}
        queued = {r[0]: r for line in queue.stdout.splitlines() if len(r := line.split("|")) >= 4}
    rows = []
    for job in jobs:
        record = records.get(job["job_id"])
        if record:
            job["state"] = record[1].split()[0].rstrip("+")
        q = queued.get(job["job_id"])
        job_details = f"{q[2]}; estimated start {q[3]} America/Toronto" if q else (record[3] if record else "")
        if job["state"] == "SUBMISSION_FAILED":
            job_details = (folder / job["folder"] / "submission.txt").read_text().strip()
        for partition in job["partitions"]:
            case = folder / job["folder"] / partition
            status = job["state"]
            details = job_details
            fastest = median = None
            if (case / "exit_code.txt").exists():
                exit_code = (case / "exit_code.txt").read_text().strip()
                status = "FAILED"
                details = f"Exit code {exit_code}; see {case.relative_to(folder)}/job.out"
                if exit_code == "0":
                    try:
                        fastest, median = validate(case, job["nodes"], partition)
                        status, details = "COMPLETED", "All ranks, threads, CPU affinity, and timings verified"
                    except (ValueError, KeyError, OSError, TypeError) as error:
                        status, details = "INVALID_RESULTS", str(error)
            elif (case / "started.txt").exists():
                status = "INTERRUPTED" if job["state"] in TERMINAL else "RUNNING"
            elif job["state"] in TERMINAL and job["state"] != "SUBMISSION_FAILED":
                status = "NOT_RUN"
            elif job["state"] == "RUNNING":
                status = "WAITING"
            rows.append(dict(nodes=job["nodes"], cores=job["cores"], partition=partition,
                             job_id=job["job_id"], state=status, fastest=fastest, median=median, details=details))
    save_jobs(folder, jobs)
    with (folder / "results.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    report(folder, mode, rows)
    print("; ".join(f"{r['nodes']} nodes {r['partition']}: {r['state']}" for r in rows), flush=True)
    return all(j["state"] in TERMINAL for j in jobs), rows


def report(folder, mode, rows):
    measured = [r for r in rows if r["state"] == "COMPLETED"]
    reference = next((r for r in measured if (r["nodes"] == 1 if mode == "scaling" else r["partition"] == "2x2x1")), None)
    lines = [f"# CPU {mode} — super-fine grid", "",
             "Fixed grid **1440 × 720 × 200**; one MPI rank per CPU node, 192 Julia threads and 192 physical cores per rank.",
             "Float64, earth_ocean, latitude–longitude without bathymetry, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3.",
             "Δt = 60 s; two warmup steps, then five windows of ten steps. CPU cores are bound with Slurm `--cpu-bind=cores`.", ""]
    if mode == "scaling":
        highest = max((r["nodes"] for r in measured), default=0)
        lines += [f"Highest verified run: **{highest} CPU nodes ({192 * highest} cores)**." if highest else "No CPU benchmark has completed and passed validation yet.",
                  "Only completed, validated runs count as reached; pending requests are retained.",
                  "The next power of two, 1024 nodes, exceeds this CPU partition's 699 configured nodes and cannot evenly divide the horizontal grid.",
                  "See [Slurm limit probe](run_metadata/1024_nodes_probe.txt) and [partition snapshot](run_metadata/partitions.txt).", ""]
    else:
        lines += ["The three layouts run sequentially on the same four allocated nodes (768 cores), with fresh Julia/MPI processes for each case.", ""]
    if measured:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        plt.rcParams.update({"svg.hashsalt": "nibi-cpu-series", "svg.fonttype": "none"})
        fig, ax = plt.subplots(figsize=(8, 4.5))
        if mode == "scaling" and reference:
            for key, label in (("fastest", "Fastest window"), ("median", "Median windows")):
                ax.plot([r["cores"] for r in measured], [100 * reference[key] / (r[key] * r["nodes"]) for r in measured], "o-", label=label)
            ax.set_xscale("log", base=2)
            ax.set_xticks([r["cores"] for r in measured], labels=[str(r["cores"]) for r in measured])
            ax.set(xlabel="CPU cores (192 per node)", ylabel="MPI efficiency relative to one node (%)")
            ax.axhline(100, color="gray", linestyle="--", linewidth=1)
        else:
            x = list(range(len(measured)))
            for offset, key, label in ((-0.18, "fastest", "Fastest window"), (0.18, "median", "Median windows")):
                ax.bar([i + offset for i in x], [r[key] for r in measured], width=0.36, label=label)
            ax.set(xticks=x, xticklabels=[r["partition"] if mode == "partition" else str(r["cores"]) for r in measured], ylabel="Seconds per step (lower is faster)")
        ax.set_title(f"Nibi CPU {mode} — 1440 × 720 × 200")
        ax.grid(axis="y", alpha=0.2)
        ax.legend()
        fig.tight_layout()
        svg = folder / "cpu_comparison.svg"
        fig.savefig(svg, metadata={"Date": None})
        svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
        plt.close(fig)
        lines += ["![CPU comparison](cpu_comparison.svg)", ""]
    label = "MPI efficiency" if mode == "scaling" else "Speedup vs 2×2×1"
    lines += [f"| Nodes | Cores | Partition | Job | State | Fastest s/step | Median s/step | {label} (fastest / median) | Details |",
              "|---:|---:|---|---|---|---:|---:|---|---|"]
    for r in rows:
        timings = f"{r['fastest']:.6f} | {r['median']:.6f}" if r["fastest"] else "— | —"
        metric = "—"
        if r["fastest"] and reference:
            if mode == "scaling":
                metric = " / ".join(f"{100 * reference[k] / (r[k] * r['nodes']):.1f}%" for k in ("fastest", "median"))
            else:
                metric = " / ".join(f"{reference[k] / r[k]:.3f}×" for k in ("fastest", "median"))
        details = r["details"].replace("|", "/").replace("\n", " ")
        lines.append(f"| {r['nodes']} | {r['cores']} | {r['partition']} | {r['job_id']} | {r['state']} | {timings} | {metric} | {details} |")
    lines += ["", "A window is ten consecutive steps; elapsed time is divided by ten. Fastest and median window times are calculated per rank, then the maximum over ranks is reported.",
              "Scaling efficiency = one-node time ÷ (measured time × node count). Missing or failed runs are excluded; efficiency requires a validated one-node baseline.",
              "Submission failures, queue limits, timeouts, and benchmark failures are recorded separately from successful measurements."]
    (folder / "plot.md").write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--submit", choices=("scaling", "partition"))
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()
    folder = args.run_dir.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    if args.submit:
        submit(folder, args.submit)
    committed = set()
    while True:
        try:
            with (folder / ".controller.lock").open("a") as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                done, rows = refresh(folder)
                finished = {(r["nodes"], r["partition"], r["state"]) for r in rows if r["state"] in TERMINAL or r["state"] in {"NOT_RUN", "INTERRUPTED"}}
                if args.commit and (done or finished - committed):
                    commit_results(folder, BRANCH, "Record Nibi super-fine CPU benchmark results and job outcomes")
                    committed = finished
        except (BlockingIOError, RuntimeError, subprocess.TimeoutExpired) as error:
            print(f"Refresh deferred: {error}", flush=True)
            if not args.watch:
                raise SystemExit(1)
            done = False
        if done or not args.watch:
            break
        time.sleep(60)


if __name__ == "__main__":
    main()
