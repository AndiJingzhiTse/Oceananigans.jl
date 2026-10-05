#!/usr/bin/env python3
"""Refresh all submitted counts, regenerate plots, and optionally watch to completion."""
import argparse
import csv
import fcntl
import json
from pathlib import Path
import subprocess
import sys
import time

from scaling import read_results, save_attempts

TERMINAL = {"COMPLETED", "FAILED", "CANCELLED", "TIMEOUT", "OUT_OF_MEMORY", "NODE_FAIL",
            "PREEMPTED", "BOOT_FAIL", "DEADLINE", "REVOKED", "INVALID_RESULTS", "SUBMISSION_FAILED"}


def run(*args):
    return subprocess.run(args, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=60)


def refresh(folder, counts):
    attempts = list(csv.DictReader((folder / "attempts.csv").open()))
    latest = {int(a["gpus"]): a for a in attempts}
    selected = [latest[n] for n in counts]
    ids = [a["job_id"] for a in selected if a["job_id"] and a["state"] not in TERMINAL]
    if ids:
        accounting = run("sacct", "-X", "-n", "-P", "-j", ",".join(ids),
                         "--format=JobIDRaw,State%40,ExitCode,Reason%200")
        if accounting.returncode:
            raise RuntimeError(accounting.stdout)
        records = {r[0]: r for line in accounting.stdout.splitlines()
                   if len(r := line.split("|")) >= 4}
        queue = run("squeue", "-h", "-j", ",".join(ids), "-o", "%i|%T|%R|%S")
        if queue.returncode:
            raise RuntimeError(queue.stdout)
        queued = {r[0]: r for line in queue.stdout.splitlines()
                  if len(r := line.split("|")) >= 4}
        for attempt in selected:
            record = records.get(attempt["job_id"])
            if record is None:
                continue
            count = int(attempt["gpus"])
            destination = folder / f"{count}_gpus"
            (destination / "accounting.txt").write_text("|".join(record) + "\n")
            state = record[1].split()[0].rstrip("+")
            attempt.update(state=state, exit_code=record[2], reason=record[3])
            q = queued.get(attempt["job_id"])
            if q:
                (destination / "queue.txt").write_text("|".join(q) + "\n")
                attempt["reason"] = f"{q[2]}; estimated start {q[3]} America/Toronto"
            if state == "COMPLETED":
                try:
                    if record[2] != "0:0":
                        raise ValueError(f"Nonzero exit code {record[2]}")
                    read_results(destination, count)
                except (ValueError, KeyError, OSError, json.JSONDecodeError) as error:
                    attempt.update(state="INVALID_RESULTS", reason=str(error))
    save_attempts(folder, attempts)
    completed = [int(a["gpus"]) for a in latest.values() if a["state"] == "COMPLETED"]
    for count in completed:
        read_results(folder / f"{count}_gpus", count)
    lines = ["# Follow-up benchmark attempts", "",
             "Requested counts: " + ", ".join(map(str, counts)) + " GPUs. Global grid remains 1440 × 720 × 200.",
             "These jobs were submitted on October 5, 2026, with 20-minute wall-time requests. "
             "Previous cancelled-attempt evidence is preserved under each count's `previous_attempts/`.", "",
             "Queue estimates use America/Toronto and may change. Pending jobs are retained until they run or fail.", "",
             f"Highest verified count so far: **{max(completed)} GPUs**.", "",
             "| GPUs | Slurm job | State | Exit code | Details |", "|---:|---|---|---|---|"]
    for attempt in selected:
        details = attempt["reason"].replace("|", "/").replace("\n", " ")
        count = int(attempt["gpus"])
        if attempt["state"] == "COMPLETED":
            details = f"All {count} rank results verified; [results]({count}_gpus/results.json)."
        lines.append(f"| {count} | {attempt['job_id']} | {attempt['state']} | {attempt['exit_code']} | {details} |")
    lines += ["", "[MPI efficiency plot and timing table](plot.md) · [Full attempt history](attempts.csv)", "",
              "Failure details, when available, are retained in each count's `job.out` and `accounting.txt`."]
    (folder / "retry_status.md").write_text("\n".join(lines) + "\n")
    plotted = run(sys.executable, str(Path(__file__).with_name("plot_scaling.py")), str(folder))
    if plotted.returncode:
        raise RuntimeError(plotted.stdout)
    print("; ".join(f"{a['gpus']} GPUs: {a['state']} ({a['job_id']})" for a in selected), flush=True)
    return all(a["state"] in TERMINAL for a in selected)


def commit_results(folder, branch):
    repository = Path(__file__).resolve().parents[3]
    current = run("git", "-C", str(repository), "branch", "--show-current")
    if current.returncode or current.stdout.strip() != branch:
        raise RuntimeError("Results saved; automatic commit skipped because the git branch changed")
    if run("git", "-C", str(repository), "diff", "--cached", "--quiet").returncode:
        raise RuntimeError("Results saved; automatic commit skipped because the index contains other changes")
    relative = str(folder.relative_to(repository))
    staged = run("git", "-C", str(repository), "add", "--", relative)
    if staged.returncode:
        raise RuntimeError(staged.stdout)
    if run("git", "-C", str(repository), "diff", "--cached", "--quiet").returncode == 0:
        return
    committed = run("git", "-C", str(repository), "-c", "user.name=Andi Tse", "-c",
                    "user.email=103150017+AndiJingzhiTse@users.noreply.github.com", "commit", "--quiet",
                    "-m", "Record completed Nibi 8, 16, 64, and 128 GPU benchmark attempts")
    if committed.returncode:
        raise RuntimeError(committed.stdout)
    print("Committed verified results and terminal job states locally.", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--counts", default="8,16,64,128")
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--poll-seconds", type=int, default=60)
    parser.add_argument("--commit", action="store_true", help="Commit run artifacts locally when all selected jobs terminate")
    parser.add_argument("--branch", default="codex/nibi-gpu-strong-scaling")
    args = parser.parse_args()
    folder = args.run_dir.resolve()
    counts = [int(n) for n in args.counts.split(",")]
    while True:
        with (folder / ".controller.lock").open("a") as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                done = refresh(folder, counts)
                if done and args.commit:
                    commit_results(folder, args.branch)
            except (BlockingIOError, subprocess.TimeoutExpired, RuntimeError) as error:
                print(f"Refresh deferred: {error}", flush=True)
                if not args.watch:
                    raise SystemExit(1)
                done = False
        if done or not args.watch:
            break
        time.sleep(args.poll_seconds)


if __name__ == "__main__":
    main()
