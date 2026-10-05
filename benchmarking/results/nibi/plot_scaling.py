#!/usr/bin/env python3
"""Plot completed Nibi measurements; requires matplotlib (scipy-stack module)."""
import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from scaling import read_results

plt.rcParams.update({"svg.hashsalt": "nibi", "svg.fonttype": "none"})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    folder = args.run_dir.resolve()
    attempts = list(csv.DictReader((folder / "attempts.csv").open()))
    successful = {int(a["gpus"]): a for a in attempts if a["state"] == "COMPLETED"}
    if 1 not in successful:
        raise SystemExit("No completed 1-GPU baseline; efficiency cannot be calculated")
    rows = []
    for count, attempt in sorted(successful.items()):
        entries = read_results(folder / f"{count}_gpus", count)
        fastest = max(e["time_per_step_seconds"] for e in entries)
        median = max(e["time_per_step_median_seconds"] for e in entries)
        slowest = max(e["time_per_step_max_seconds"] for e in entries)
        rows.append((count, int(attempt["nodes"]), attempt["partition"], fastest, median, slowest))
    baseline, baseline_median = rows[0][3:5]
    counts = [r[0] for r in rows]
    efficiency = [100 * baseline / (r[0] * r[3]) for r in rows]
    median_efficiency = [100 * baseline_median / (r[0] * r[4]) for r in rows]
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.plot(counts, efficiency, "o-", label="Measured: fastest window, slowest rank")
    ax.plot(counts, median_efficiency, "s--", label="Median windows, slowest rank", alpha=0.75)
    ax.axhline(100, linestyle=":", color="gray", label="Ideal")
    ax.set_xscale("log", base=2)
    ax.set_xticks(counts, [str(n) for n in counts])
    ax.set(xlabel="GPUs / MPI ranks (one rank per H100)", ylabel="MPI strong-scaling efficiency (%)",
           title="Nibi — 1440 × 720 × 200, Float64", ylim=(0, max(110, max(efficiency) * 1.1)))
    ax.grid(alpha=0.25)
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()
    fig.savefig(folder / "mpi_efficiency.svg", metadata={"Date": None})
    plt.close(fig)
    md = ["# Nibi GPU strong scaling", "",
          "Global grid: 1440 × 720 × 200 (207,360,000 cells), latitude–longitude without bathymetry.",
          "Float64, WENOVectorInvariantDefault, WENO7, CATKE, T/S, SplitRungeKutta3; Δt = 60 s.",
          "Two warmup steps, then five windows of ten steps, matching the Rondeau reference.", "",
          "![MPI efficiency](mpi_efficiency.svg)", "",
          "| GPUs | Nodes | Partition | Fastest-window s/step | Median s/step | Speedup | MPI efficiency | Median efficiency | Spread |",
          "|---:|---:|---|---:|---:|---:|---:|---:|---:|"]
    for row, eff, med_eff in zip(rows, efficiency, median_efficiency):
        count, nodes, partition, fastest, median, slowest = row
        md.append(f"| {count} | {nodes} | {partition} | {fastest:.6f} | {median:.6f} | "
                  f"{baseline / fastest:.3f}× | {eff:.1f}% | {med_eff:.1f}% | {(slowest / fastest - 1) * 100:.1f}% |")
    md += ["", "MPI efficiency = T₁ / (N × Tₙ) × 100%. Tₙ is the maximum across ranks of each rank's fastest timing window, as in the reference. "
           "Median efficiency uses the maximum rank median and the one-rank median baseline. "
           "Spread = (maximum rank/window time ÷ fastest-window slowest-rank time − 1) × 100%. "
           "The suite does not retain individual windows, so these aggregates are not a synchronized per-window maximum.", "",
           f"Highest successful count: **{max(counts)} GPUs**.", "",
           "## Attempt status", "", "| GPUs | Job | State | Exit code | Reason |", "|---:|---|---|---|---|"]
    for attempt in attempts:
        reason = attempt["reason"].replace("|", "/").replace("\n", " ")
        md.append(f"| {attempt['gpus']} | {attempt['job_id']} | {attempt['state']} | {attempt['exit_code']} | {reason} |")
    (folder / "plot.md").write_text("\n".join(md) + "\n")
    print(f"Saved {folder / 'mpi_efficiency.svg'} ({len(rows)} completed counts)")


if __name__ == "__main__":
    main()
