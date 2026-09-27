#!/usr/bin/env python3
"""Regenerate Rondeau charts from saved JSON, GPU summaries, and CPU samples.

Usage: python3 benchmarking/results/rondeau/plot_rondeau_results.py [run_folder]
Requires matplotlib. No benchmarks are launched by this script.
"""
import argparse
import csv
import json
import math
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({"svg.hashsalt": "rondeau", "svg.fonttype": "none"})


def save(fig, path):
    fig.tight_layout()
    fig.savefig(path, metadata={"Date": None})
    path.write_text("\n".join(line.rstrip() for line in path.read_text().splitlines()) + "\n")
    plt.close(fig)


def timing(folder):
    records = json.loads((folder / "results.json").read_text())
    return max(r["time_per_step_seconds"] for r in records)


def performance(root, series, distributed=False):
    folder = root / series
    configs = sorted((p for p in folder.iterdir() if p.is_dir() and (p / "results.json").exists()),
                     key=lambda p: int(p.name.split("_" if distributed else "x")[0]))
    counts = [int(p.name.split("_" if distributed else "x")[0]) for p in configs]
    times = [timing(p) for p in configs]
    labels = [str(n) if distributed else p.name.replace("x", " × ") for n, p in zip(counts, configs)]
    chart_labels = [label + "\n" + ("Tripolar" if n == 720 else "Latitude longitude")
                    for label, n in zip(labels, counts)] if series == "cpu_resolution" else labels
    title = series.replace("_", " ").replace("cpu", "CPU").replace("gpu", "GPU")
    x = range(len(counts))
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(x, [1 / t for t in times], "o-", label="Measured")
    if distributed:
        ax.plot(x, [n / times[0] for n in counts], "x--", color="gray", label="Ideal linear scaling")
        ax.legend()
    ax.set(xticks=list(x), xticklabels=chart_labels, ylabel="Simulation steps per second", title=f"Rondeau — {title}",
           xlabel=("CPU MPI ranks (one thread per rank)" if series == "cpu_scaling" else "GPUs (one MPI rank per GPU)")
           if distributed else "Grid resolution (50 vertical levels)")
    ax.grid(axis="y", alpha=.25)
    ax.set_ylim(bottom=0)
    save(fig, folder / "speed.svg")
    notes = "Timings use the slowest MPI rank at each count." if distributed else "Timings use the saved minimum time per step."
    if series == "cpu_resolution":
        notes += " The 180 and 360 grids use latitude longitude geometry; 720 uses tripolar geometry."
    elif series == "gpu_resolution":
        notes += " All grids use latitude longitude geometry."
    md = [f"# Rondeau {title}", "", "![Simulation speed](speed.svg)", "", notes, "",
          "Speed means simulation steps per second (the reciprocal of step time). Each step advances 60 simulated seconds. These timing runs use Float64, 2 warmup steps, and 5 samples of 10 steps.", ""]
    if distributed:
        speeds = [times[0] / t for t in times]
        efficiencies = [s / n * 100 for s, n in zip(speeds, counts)]
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(x, efficiencies, "o-", label="Measured")
        ax.axhline(100, color="gray", linestyle="--", label="Ideal")
        ax.set(xticks=list(x), xticklabels=labels, xlabel="CPU ranks" if series == "cpu_scaling" else "GPUs",
               ylabel="MPI efficiency (%)", title=f"Rondeau — {title}", ylim=(0, 110))
        ax.legend(); ax.grid(axis="y", alpha=.25)
        save(fig, folder / "mpi_efficiency.svg")
        md += ["![MPI efficiency](mpi_efficiency.svg)", "", "Efficiency = one-rank time / parallel time / rank count × 100%.", "",
               "| Count | Seconds per step | Steps per second | Speedup | Efficiency |", "|---:|---:|---:|---:|---:|"]
        md += [f"| {n} | {t:.6f} | {1/t:.6f} | {s:.3f}× | {e:.1f}% |" for n,t,s,e in zip(counts,times,speeds,efficiencies)]
    else:
        factors = [b/a for a,b in zip(times, times[1:])]
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.scatter(range(len(factors)), factors, label="Measured time ratio")
        ax.scatter(range(len(factors)), [4]*len(factors), marker="x", label="Grid point ratio (4×)")
        ax.set(xticks=list(range(len(factors))), xticklabels=[f"{a} → {b}" for a,b in zip(counts,counts[1:])],
               ylabel="Time / grid point ratio", xlabel="Horizontal resolution increase", title=f"Rondeau — {title}")
        ax.legend(); ax.grid(axis="y", alpha=.25)
        save(fig, folder / "scaling_factor_scatter.svg")
        md += ["![Adjacent resolution scaling](scaling_factor_scatter.svg)", "",
               "| Grid | Grid points | Seconds per step | Steps per second | Time ratio to previous |", "|---|---:|---:|---:|---:|"]
        md += [f"| {label} | {math.prod(map(int,p.name.split('x'))):,} | {t:.6f} | {1/t:.6f} | {times[i]/times[i-1]:.3f}× |" if i else
               f"| {label} | {math.prod(map(int,p.name.split('x'))):,} | {t:.6f} | {1/t:.6f} | — |" for i,(p,label,t) in enumerate(zip(configs,labels,times))]
    (folder / "plot.md").write_text("\n".join(md) + "\n")


def pie(folder, names, values, title, explanation, unit):
    selected = [(n,v) for n,v in zip(names,values) if v > 0]
    names, values = zip(*selected)
    fig, ax = plt.subplots(figsize=(9, 5))
    total = sum(values)
    wedges, _, _ = ax.pie(values, autopct=lambda p: f"{p:.1f}%" if p >= 5 else "", startangle=90)
    ax.legend(wedges, [f"{n} ({v/total:.1%})" for n,v in zip(names,values)], loc="center left", bbox_to_anchor=(1, .5))
    ax.set_title(title)
    save(fig, folder / "pie_chart.svg")
    md = [f"# {title}", "", "![Activity breakdown](pie_chart.svg)", "", explanation, "",
          f"| Category | {unit} | Share |", "|---|---:|---:|"]
    md += [f"| {n} | {v:,.0f} | {v/total*100:.2f}% |" for n,v in zip(names,values)]
    (folder / "plot.md").write_text("\n".join(md) + "\n")


def profiles(root):
    for folder in sorted((root / "nsys_gpu").iterdir()):
        if not folder.is_dir():
            continue
        totals = dict.fromkeys(["Gc", "Gu", "Gv", "Others"], 0)
        with (folder / "kernel_summary_cuda_gpu_kern_sum.csv").open() as f:
            for row in csv.DictReader(f):
                category = next((c for c in ("Gc", "Gu", "Gv") if f"gpu_compute_hydrostatic_free_surface_{c}_" in row["Name"]), "Others")
                totals[category] += int(row["Total Time (ns)"])
        pie(folder, list(totals), list(totals.values()), f"Rondeau GPU kernels — {folder.name.replace('x', ' × ')}",
            "Matches the Andi 5070 Ti grouping: hydrostatic free surface Gc, Gu, Gv kernels and all remaining kernels. Shares use summed GPU kernel duration from `kernel_summary_cuda_gpu_kern_sum.csv`, not elapsed wall time. The capture includes startup, warmup and measured steps; concurrent kernel durations can overlap.", "Kernel duration (ns)")
    folder = root / "nsys_cpu" / "720x360x50"
    summary = folder / "cpu_sample_summary.csv"
    if summary.exists():
        with summary.open() as f:
            rows = list(csv.DictReader(f))
        # Exclusive leaf frames only: every captured sample belongs to one category.
        totals = {}
        for row in rows:
            category = row["category"]
            totals[category] = totals.get(category, 0) + int(row["samples"])
        pie(folder, list(totals), list(totals.values()), "Rondeau CPU samples — 720 × 360 × 50",
            "Exclusive leaf-frame counts from Nsight Systems CPU sampling (`COMPOSITE_EVENTS` joined to `SAMPLING_CALLCHAINS` at stack depth 0). All captured process-tree threads are included. Each sample is counted once, without summing ancestor frames. This capture includes compilation, startup, 2 warmup steps and 2 measured steps, so it is not a pure timestep breakdown. Unlike GPU pies, percentages describe CPU samples rather than kernel duration. See `cpu_sample_summary.csv` for symbols and categories.", "CPU samples")


def cpu_category(symbol, module, unresolved):
    if unresolved:
        return "Unresolved leaf frames"
    for name in ("Gc", "Gu", "Gv"):
        if f"compute_hydrostatic_free_surface_{name}" in symbol:
            return name
    if "LLVM" in module or "llvm::" in symbol:
        return "LLVM compilation"
    if "julia_" in symbol or "japi" in symbol or "jlcapi" in symbol:
        return "Other Julia code"
    if Path(module).name.startswith("libjulia"):
        return "Julia runtime / compilation"
    return "Other resolved code"


def cpu_summary(database, root):
    with sqlite3.connect(f"file:{database.resolve()}?mode=ro", uri=True) as connection:
        rows = connection.execute("""
            SELECT COALESCE(s.value, '[unknown]'), COALESCE(m.value, '[unknown]'),
                   COALESCE(c.unresolved, CASE WHEN s.value IS NULL THEN 1 ELSE 0 END), COUNT(*)
            FROM COMPOSITE_EVENTS e
            LEFT JOIN SAMPLING_CALLCHAINS c ON c.id = e.id AND c.stackDepth = 0
            LEFT JOIN StringIds s ON s.id = c.symbol
            LEFT JOIN StringIds m ON m.id = c.module
            GROUP BY 1, 2, 3 ORDER BY COUNT(*) DESC, 1, 2, 3
        """).fetchall()
    if not rows:
        raise ValueError("CPU capture contains no sampling events")
    grouped = {}
    for symbol, module, unresolved, count in rows:
        # Anonymous JIT addresses do not provide stable function identities.
        symbol = "[unresolved]" if unresolved else symbol
        key = (symbol, module, unresolved)
        grouped[key] = grouped.get(key, 0) + count
    with (root / "nsys_cpu/720x360x50/cpu_sample_summary.csv").open("w") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["symbol", "module", "unresolved", "samples", "category"])
        for (symbol, module, unresolved), count in sorted(grouped.items(), key=lambda item: (-item[1], item[0])):
            writer.writerow([symbol, module, unresolved, count, cpu_category(symbol, module, unresolved)])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_folder", nargs="?", type=Path, default=Path(__file__).parent / "2026-09-27_all")
    parser.add_argument("--cpu-sqlite", type=Path, help="Exported Nsight CPU SQLite capture; regenerate exclusive leaf sample CSV")
    args = parser.parse_args()
    root = args.run_folder
    if args.cpu_sqlite:
        cpu_summary(args.cpu_sqlite, root)
    for series in ("cpu_resolution", "gpu_resolution", "cpu_scaling", "gpu_scaling"):
        performance(root, series, "scaling" in series)
    profiles(root)
    (root / "plots.md").write_text("# Rondeau benchmark plots\n\n"
        "Charts follow the Andi 5070 Ti reference grouping and scaling definitions.\n\n"
        "| Series | Report | Speed | Scaling |\n|---|---|---|---|\n" +
        "\n".join(f"| {s.replace('_', ' ')} | [Report]({s}/plot.md) | [Chart]({s}/speed.svg) | [Chart]({s}/{'mpi_efficiency' if 'scaling' in s else 'scaling_factor_scatter'}.svg) |" for s in ("cpu_resolution", "gpu_resolution", "cpu_scaling", "gpu_scaling")) +
        "\n\nProfiles: [GPU 360](nsys_gpu/360x180x50/plot.md), [GPU 720](nsys_gpu/720x360x50/plot.md), [CPU 720](nsys_cpu/720x360x50/plot.md).\n\n" +
        "\n\n".join(f"## {s.replace('_', ' ').replace('cpu', 'CPU').replace('gpu', 'GPU')}\n\n![Simulation speed]({s}/speed.svg)" for s in ("cpu_resolution", "gpu_resolution", "cpu_scaling", "gpu_scaling")) +
        "\n\n## Nsight profiles\n\nGPU pies show summed kernel duration; the CPU pie shows exclusive leaf-frame sample counts. Captures include compilation, startup, warmup and measured steps. See individual reports for definitions and source data.\n\n" +
        "\n\n".join(f"![{label}]({path}/pie_chart.svg)" for label,path in [("GPU 360 × 180 × 50", "nsys_gpu/360x180x50"), ("GPU 720 × 360 × 50", "nsys_gpu/720x360x50"), ("CPU 720 × 360 × 50", "nsys_cpu/720x360x50")]) + "\n")


if __name__ == "__main__":
    main()
