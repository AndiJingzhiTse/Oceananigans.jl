#!/usr/bin/env python3
"""Run fresh-process pressure-solver pairs and retain all numerical outcomes."""

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import signal
import statistics
import subprocess
import sys
import time


def run_command(command, environment, log, timeout):
    process = subprocess.Popen(command, env=environment, stdout=log, stderr=subprocess.STDOUT,
                               start_new_session=True)
    try:
        code = process.wait(timeout=timeout)
        if code:
            raise subprocess.CalledProcessError(code, command)
    except BaseException:
        try:
            os.killpg(process.pid, signal.SIGTERM)
            process.wait(timeout=10)
        except ProcessLookupError:
            pass
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
        raise


def accepted_records(directory, ranks, gpu_uuids):
    records = [json.loads((directory / f"rank_{rank}.json").read_text()) for rank in range(ranks)]
    actual_devices = []
    for rank, record in enumerate(records):
        if record["rank"] != rank or record["ranks"] != ranks or record["status"] != "COMPLETED":
            raise ValueError("Incomplete MPI results")
        if not record["pressure_validation"]["passed"] or not record["model_validation"]["passed"]:
            raise ValueError("Numerical validation failed")
        for key, validation in (("pressure", record["pressure_validation"]), ("model", record["model_validation"])):
            metrics = ("relative_residual", "relative_error") if key == "pressure" else ("maximum_divergence",)
            tolerance = validation["tolerance"]
            if not 0 < tolerance < 1 or any(not math.isfinite(validation[metric]) or
                                           not 0 <= validation[metric] <= tolerance for metric in metrics):
                raise ValueError("Numerical validation values do not satisfy the recorded tolerance")
        if record["configuration"] != records[0]["configuration"]:
            raise ValueError("MPI ranks used different configurations")
        for key in ("pressure_timing", "timestep_timing"):
            seconds = record[key]["maximum_rank_seconds"]
            if len(seconds) != record["configuration"]["windows"] or not all(math.isfinite(value) and value > 0 for value in seconds):
                raise ValueError("Incomplete or nonfinite timing windows")
        actual_devices.append(record["gpu_uuid"].removeprefix("GPU-"))
    expected_devices = [uuid.removeprefix("GPU-") for uuid in gpu_uuids]
    if len(set(actual_devices)) != ranks or set(actual_devices) != set(expected_devices):
        raise ValueError("GPU placement differs from the requested allocation")
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--gpus", required=True, help="Comma-separated GPU UUIDs")
    parser.add_argument("--backends", nargs="+", default=["native"],
                        choices=["native", "serial_chunks", "async_chunks", "dagger_chunks"])
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=600, help="Seconds per fresh process")
    parser.add_argument("--julia", default="julia")
    parser.add_argument("--mpiexec", default="mpiexec")
    parser.add_argument("--plan", action="store_true")
    args = parser.parse_args()
    if args.repeats < 1 or args.timeout < 1:
        parser.error("Repeats and timeout must be positive")
    if len(set(args.backends)) != len(args.backends):
        parser.error("Backends must be distinct")
    for variable in ("TMPDIR", "TMP", "TEMP", "OMPI_MCA_orte_tmpdir_base"):
        directory = Path(os.environ.get(variable, "/tmp")).resolve()
        if not directory.is_dir() or any(directory == root or root in directory.parents
                                         for root in (Path("/tmp"), Path("/var/tmp"))):
            parser.error(f"Set {variable} to an existing data-filesystem directory")
    gpu_uuids = args.gpus.split(",")
    if len(set(gpu_uuids)) != len(gpu_uuids):
        parser.error("GPU UUIDs must be distinct")
    script = Path(__file__).with_name("benchmark_pressure_solver.jl")
    commands = []
    for repeat in range(args.repeats):
        backends = args.backends if repeat % 2 == 0 else list(reversed(args.backends))
        for backend in backends:
            directory = args.output.resolve() / f"repeat_{repeat + 1}" / backend
            command = [args.julia, f"--project={args.project.resolve()}", "--threads=1",
                       str(script), str(args.config.resolve()), str(directory), backend]
            if len(gpu_uuids) > 1:
                command = [args.mpiexec, "--bind-to", "core", "-np", str(len(gpu_uuids)), *command]
            commands.append((directory, backend, command))
    if args.plan:
        print(json.dumps([command for _, _, command in commands], indent=2))
        return
    args.output.mkdir(parents=True, exist_ok=False)
    shutil.copy2(args.config, args.output / "configuration.toml")
    environment_directory = args.output / "environment"
    environment_directory.mkdir()
    for name in ("Project.toml", "Manifest.toml", "LocalPreferences.toml"):
        source = args.project / name
        if source.exists():
            shutil.copy2(source, environment_directory / name)
    environment = dict(os.environ, CUDA_VISIBLE_DEVICES=",".join(gpu_uuids),
                       OPENBLAS_NUM_THREADS="1", JULIA_NUM_THREADS="1", JULIA_NUM_PRECOMPILE_TASKS="1")
    outcomes = []
    source_revision = None
    for directory, backend, command in commands:
        directory.mkdir(parents=True)
        outcome = dict(backend=backend, directory=str(directory), command=command, status="RUNNING")
        started = time.monotonic()
        print("Running:", " ".join(command), flush=True)
        with (directory / "job.log").open("w") as log:
            try:
                run_command(command, environment, log, args.timeout)
                records = accepted_records(directory, len(gpu_uuids), gpu_uuids)
                if any(record["source_dirty"] or record["backend"] != backend for record in records):
                    raise ValueError("Measurements require a clean source tree and the requested backend")
                if source_revision is not None and records[0]["source_revision"] != source_revision:
                    raise ValueError("Source revision changed during the study")
                source_revision = records[0]["source_revision"]
                outcome.update(status="COMPLETED", pressure_seconds=records[0]["pressure_timing"]["median_seconds_per_operation"],
                               timestep_seconds=records[0]["timestep_timing"]["median_seconds_per_operation"])
            except (subprocess.SubprocessError, ValueError, OSError) as error:
                outcome.update(status="FAILED", error=str(error))
        outcomes.append(outcome)
        outcome["wall_seconds"] = time.monotonic() - started
        (args.output / "outcomes.json").write_text(json.dumps(outcomes, indent=2) + "\n")
        if outcome["status"] != "COMPLETED":
            sys.exit("Study stopped after a failed case; inspect job.log")
    summary = {}
    for backend in args.backends:
        selected = [outcome for outcome in outcomes if outcome["backend"] == backend]
        summary[backend] = {metric: statistics.median(outcome[metric] for outcome in selected)
                            for metric in ("pressure_seconds", "timestep_seconds")}
        for metric in ("pressure_seconds", "timestep_seconds"):
            summary[backend][metric + "_range"] = [min(outcome[metric] for outcome in selected),
                                                   max(outcome[metric] for outcome in selected)]
    if "native" in summary:
        for values in summary.values():
            values["pressure_speedup"] = summary["native"]["pressure_seconds"] / values["pressure_seconds"]
            values["timestep_speedup"] = summary["native"]["timestep_seconds"] / values["timestep_seconds"]
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    checksums = {str(path.relative_to(args.output)): hashlib.sha256(path.read_bytes()).hexdigest()
                 for path in args.output.rglob("*") if path.is_file()}
    (args.output / "checksums.json").write_text(json.dumps(checksums, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
