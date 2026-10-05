#!/usr/bin/env python3
"""Submit and monitor a resumable power-of-two strong-scaling sweep on Nibi."""
import argparse
import csv
import json
import math
from pathlib import Path
import subprocess
import shutil
import time

SCRIPT_DIR = Path(__file__).resolve().parent
FIELDS = ("gpus", "nodes", "partition", "job_id", "state", "exit_code", "reason")


def partition_for(count):
    """Match Rondeau at 1/2/4 ranks, then balance horizontal local dimensions."""
    if count <= 4:
        return {1: (1, 1), 2: (1, 2), 4: (2, 2)}[count]
    options = [(rx, count // rx) for rx in range(1, count + 1)
               if count % rx == 0 and 1440 % rx == 0 and 720 % (count // rx) == 0]
    if not options:
        raise ValueError(f"No evenly divisible horizontal partition for {count} ranks")
    return min(options, key=lambda p: abs(math.log((1440 / p[0]) / (720 / p[1]))))


def read_results(folder, count):
    entries = json.loads((folder / "results.json").read_text())
    if len(entries) != count or {e["rank"] for e in entries} != set(range(count)):
        raise ValueError("Missing or duplicate MPI ranks")
    rx, ry = partition_for(count)
    for entry in entries:
        if entry["grid_size"] != [1440 // rx, 720 // ry, 200]:
            raise ValueError("Unexpected local grid size")
        if (entry["float_type"] != "Float64" or entry["samples"] != 5
                or entry["time_steps"] != 10 or entry["Δt"] != 60):
            raise ValueError("Unexpected benchmark settings")
        if not math.isfinite(entry["time_per_step_seconds"]) or entry["time_per_step_seconds"] <= 0:
            raise ValueError("Invalid step time")
    return entries


def command(*args):
    return subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def save_attempts(run_dir, attempts):
    temporary = run_dir / "attempts.csv.tmp"
    with temporary.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, FIELDS)
        writer.writeheader()
        writer.writerows(attempts)
    temporary.replace(run_dir / "attempts.csv")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--account", default="def-fpoulin_gpu")
    parser.add_argument("--counts", default="1,2,4,8,16,32,64,128,256,512")
    parser.add_argument("--poll-seconds", type=int, default=30)
    args = parser.parse_args()
    counts = [int(n) for n in args.counts.split(",")]
    if not counts or any(n < 1 or n & (n - 1) for n in counts):
        parser.error("GPU counts must be positive powers of two")
    if counts != sorted(set(counts)):
        parser.error("GPU counts must be unique and ascending")
    run_dir = args.run_dir.resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    metadata = run_dir / "run_metadata"
    if not metadata.exists():
        metadata.mkdir()
        for name in ("Project.toml", "Manifest.toml", "LocalPreferences.toml"):
            shutil.copy2(SCRIPT_DIR / "environment" / name, metadata / name)
        for name in ("benchmark.sbatch", "run_benchmark.jl", "scaling.py", "plot_scaling.py"):
            shutil.copy2(SCRIPT_DIR / name, metadata / name)
        repository = SCRIPT_DIR.parents[2]
        (metadata / "revision.txt").write_text(command("git", "-C", str(repository), "rev-parse", "HEAD").stdout)
        (metadata / "working_tree.txt").write_text(command("git", "-C", str(repository), "status", "--short").stdout)
        drac_root = Path(__import__("os").environ.get("DRAC_ROOT", str(Path.home() / "Oceananigans-DRAC")))
        shutil.copy2(drac_root / "src" / "drac_mpi.jl", metadata / "drac_mpi.jl")
        (metadata / "drac_revision.txt").write_text(command("git", "-C", str(drac_root), "rev-parse", "HEAD").stdout)
        (metadata / "partitions.txt").write_text(command("sinfo", "-o", "%P %a %l %D %G").stdout)
    attempts_path = run_dir / "attempts.csv"
    attempts = list(csv.DictReader(attempts_path.open())) if attempts_path.exists() else []

    for count in counts:
        folder = run_dir / f"{count}_gpus"
        folder.mkdir(exist_ok=True)
        previous = next((a for a in reversed(attempts) if int(a["gpus"]) == count), None)
        if previous and previous["state"] == "COMPLETED":
            read_results(folder, count)
            continue
        rx, ry = partition_for(count)
        nodes = max(1, count // 8)
        ranks_per_node = min(8, count)
        partition = f"{rx}x{ry}x1"
        # Resume live jobs instead of submitting duplicate work.
        if previous and previous["state"] in ("SUBMITTED", "PENDING", "RUNNING"):
            attempt = previous
        else:
            attempt = dict(zip(FIELDS, (count, nodes, partition, "", "", "", "")))
            attempts.append(attempt)
            submit = command("sbatch", "--parsable", f"--account={args.account}",
                             f"--nodes={nodes}", f"--ntasks={count}",
                             f"--ntasks-per-node={ranks_per_node}",
                             "--mem=0" if count >= 8 else "--mem=64G",
                             f"--job-name=nibi_scale_{count}", f"--output={folder}/job.out",
                             str(SCRIPT_DIR / "benchmark.sbatch"), str(folder), partition, str(SCRIPT_DIR))
            (folder / "submission.txt").write_text(submit.stdout)
            if submit.returncode:
                attempt.update(state="SUBMISSION_FAILED", exit_code=str(submit.returncode),
                               reason=submit.stdout.strip())
                save_attempts(run_dir, attempts)
                print(f"{count} GPUs: submission failed: {submit.stdout}", flush=True)
                break
            attempt.update(job_id=submit.stdout.strip().split(";")[0], state="SUBMITTED")
            save_attempts(run_dir, attempts)
            print(f"{count} GPUs: job {attempt['job_id']}, partition {partition}", flush=True)

        while True:
            accounting = command("sacct", "-X", "-n", "-P", "-j", attempt["job_id"],
                                 "--format=JobIDRaw,State,ExitCode,Reason")
            (folder / "accounting.txt").write_text(accounting.stdout)
            records = [line.split("|") for line in accounting.stdout.splitlines()]
            record = next((r for r in records if r[0] == attempt["job_id"]), None)
            if record and len(record) >= 4:
                state = record[1].split()[0].rstrip("+")
                attempt.update(state=state, exit_code=record[2], reason=record[3])
                save_attempts(run_dir, attempts)
                if state in ("COMPLETED", "FAILED", "CANCELLED", "TIMEOUT", "OUT_OF_MEMORY",
                             "NODE_FAIL", "PREEMPTED", "BOOT_FAIL", "DEADLINE", "REVOKED"):
                    break
            time.sleep(args.poll_seconds)

        if attempt["state"] == "COMPLETED" and attempt["exit_code"] == "0:0":
            try:
                read_results(folder, count)
            except (ValueError, KeyError, OSError) as error:
                attempt.update(state="INVALID_RESULTS", reason=str(error))
                save_attempts(run_dir, attempts)
            else:
                print(f"{count} GPUs: completed and all rank results verified", flush=True)
                continue
        print(f"{count} GPUs: {attempt['state']} ({attempt['exit_code']}); see {folder}/job.out", flush=True)
        break

    # A separate plotting step can be rerun while jobs are queued or running.
    print(f"Sweep stopped. Plot with: python3 {SCRIPT_DIR / 'plot_scaling.py'} {run_dir}", flush=True)


if __name__ == "__main__":
    main()
