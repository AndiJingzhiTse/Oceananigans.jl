#!/usr/bin/env python3
"""Regenerate Rondeau charts from saved JSON, GPU summaries, and CPU samples.

Usage: python3 benchmarking/results/rondeau/plot_rondeau_results.py [run_folder]
Requires matplotlib. No benchmarks are launched by this script.
"""
import argparse
import csv
import json
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({"svg.hashsalt": "rondeau", "svg.fonttype": "none"})

SERIES = ("cpu_resolution", "gpu_resolution", "cpu_scaling_default", "cpu_scaling_fine",
          "gpu_scaling_fine", "gpu_scaling_super_fine")


def title_for(series):
    return series.replace("_", " ").replace("cpu", "CPU").replace("gpu", "GPU")


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
    title = title_for(series)
    notes = "Timings use the slowest MPI rank at each count." if distributed else "Timings use the saved minimum time per step."
    if series == "cpu_resolution":
        notes += " The 180 and 360 grids use latitude longitude geometry; 720 uses tripolar geometry."
    elif series == "gpu_resolution":
        notes += " All grids use latitude longitude geometry."
    elif series == "cpu_scaling_default":
        notes += (" Global grid: 360 × 180 × 50, tripolar with partial-cell bathymetry."
                  " At 64 and 128 ranks the last partitions receive the leftover cells,"
                  " so local grid sizes vary by rank. The 128-rank partition is 8 × 16 × 1"
                  " to keep x evenly divided across the tripolar fold.")
    elif series == "cpu_scaling_fine":
        notes += " Global grid: 720 × 360 × 50, tripolar with partial-cell bathymetry."
    elif series == "gpu_scaling_fine":
        notes += " Global grid: 720 × 360 × 50, tripolar with partial-cell bathymetry."
    elif series == "gpu_scaling_super_fine":
        levels = json.loads((configs[0] / "results.json").read_text())[0]["grid_size"][2]
        notes += f" Global grid: 1440 × 720 × {levels}, plain latitude longitude without bathymetry."
    md = [f"# Rondeau {title}", "", notes,
          "These timing runs use Float64, 60 simulated seconds per step, 2 warmup steps, and 5 samples of 10 steps.", ""]
    if distributed:
        speeds = [times[0] / t for t in times]
        baseline_count = counts[0]
        efficiencies = [s * baseline_count / n * 100 for s, n in zip(speeds, counts)]
        fig, ax = plt.subplots(figsize=(7, 4))
        x = range(len(counts))
        ax.plot(x, efficiencies, "o-", label="Measured MPI efficiency")
        ax.plot(x, [100] * len(counts), "x--", color="gray", label="Ideal (100%)")
        ax.set(xticks=list(x), xticklabels=labels, xlabel="CPU ranks" if series.startswith("cpu_scaling") else "GPUs",
               ylabel="MPI efficiency (%)", title=f"Rondeau — {title} MPI efficiency", ylim=(0, 110))
        if baseline_count > 1:
            ax.set_title(f"Rondeau — {title} MPI efficiency\n{baseline_count}-GPU baseline")
        ax.legend(); ax.grid(axis="y", alpha=.25)
        save(fig, folder / "mpi_efficiency.svg")
        md += ["![Measured and ideal MPI efficiency](mpi_efficiency.svg)", "",
               "| " + ("CPU ranks" if series.startswith("cpu_scaling") else "GPUs") + " | Seconds per step | Steps per second | " + ("Speedup" if baseline_count == 1 else f"Speedup vs {baseline_count} GPUs") + " | MPI efficiency | Ideal efficiency |",
               "|---:|---:|---:|---:|---:|---:|"]
        md += [f"| {n} | {t:.6f} | {1/t:.6f} | {s:.3f}× | {e:.1f}% | 100.0% |" for n,t,s,e in zip(counts,times,speeds,efficiencies)]
        if baseline_count == 1:
            md += ["", "MPI efficiency = (one-rank step time ÷ current step time) ÷ rank count × 100%. The one-rank measurement is the baseline. The table uses the slowest MPI rank at each count."]
        else:
            md += ["", f"MPI efficiency is relative to the {baseline_count}-GPU baseline: (baseline step time ÷ current step time) × {baseline_count} ÷ GPU count × 100%. The baseline is normalized to 100%; this does not measure efficiency relative to one GPU. Timings use the slowest rank."]
        if series == "gpu_scaling_super_fine":
            if (folder / "1_gpus/attempt.md").exists():
                md += ["", "The [one-GPU case](1_gpus/attempt.md) ran out of memory before warmup; no one-GPU timing is available."]
            md += ["", "[Rerun provenance](rerun.md) records the replacement measurements and any failed configurations."]
    else:
        factors = [b/a for a,b in zip(times, times[1:])]
        transitions = [f"{a} → {b}" for a,b in zip(counts, counts[1:])]
        x = range(len(factors))
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.scatter(x, factors, label="Measured time ratio")
        ax.scatter(x, [4]*len(factors), marker="x", color="gray", label="Grid point ratio (4×)")
        ax.set(xticks=list(x), xticklabels=transitions,
               ylabel="Step-time scaling factor (×)", xlabel="Horizontal resolution transition",
               title=f"Rondeau — {title} scaling factor", ylim=(0, max(4, *factors) * 1.12))
        ax.legend(); ax.grid(axis="y", alpha=.25)
        save(fig, folder / "scaling_factor_scatter.svg")
        md += ["![Step-time scaling factor](scaling_factor_scatter.svg)", "",
               "| Resolution transition | From time (s/step) | To time (s/step) | Measured scaling factor | Grid point ratio |",
               "|---|---:|---:|---:|---:|"]
        md += [f"| {transition} | {a:.6f} | {b:.6f} | {factor:.3f}× | 4.000× |"
               for transition,a,b,factor in zip(transitions,times,times[1:],factors)]
        md += ["", "Scaling factor = time per step at the larger resolution ÷ time per step at the smaller resolution. For example, 10 → 45 seconds gives 4.5×. The 4× reference is the ratio of horizontal grid points between adjacent configurations."]
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


def report_table(path):
    lines = path.read_text().splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("| "))
    end = next((i for i in range(start, len(lines)) if not lines[i].startswith("|")), len(lines))
    return "\n".join(lines[start:end])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_folder", nargs="?", type=Path, default=Path(__file__).parent / "2026-09-27_all")
    parser.add_argument("--cpu-sqlite", type=Path, help="Exported Nsight CPU SQLite capture; regenerate exclusive leaf sample CSV")
    args = parser.parse_args()
    root = args.run_folder
    if args.cpu_sqlite:
        cpu_summary(args.cpu_sqlite, root)
    available_series = tuple(series for series in SERIES
                             if (root / series).is_dir()
                             and any((folder / "results.json").exists()
                                     for folder in (root / series).iterdir() if folder.is_dir()))
    for series in available_series:
        performance(root, series, "scaling" in series)
    profiles(root)
    super_fine_configs = sorted((root / "gpu_scaling_super_fine").glob("*_gpus"), key=lambda p: int(p.name.split("_")[0]))
    super_fine_results = [p for p in super_fine_configs if (p / "results.json").exists()]
    super_fine_levels = json.loads((super_fine_results[0] / "results.json").read_text())[0]["grid_size"][2] if super_fine_results else 200
    sections = ["# Rondeau benchmark plots", "",
                "## Benchmark configuration", "",
                "All timing cases call `earth_ocean` through `benchmarking/run_benchmarks.jl`."
                " Grid dimensions below are global; MPI partitions split the horizontal grid across ranks.", "",
                "| Series | Global resolution | `grid_type` passed to `earth_ocean` | Grid constructed | MPI ranks |",
                "|---|---|---|---|---|",
                "| CPU resolution | 180 × 90 × 50; 360 × 180 × 50 | `lat_lon` | Plain `LatitudeLongitudeGrid`, no bathymetry | 1 |",
                "| CPU resolution | 720 × 360 × 50 | `tripolar` | `TripolarGrid` with immersed partial-cell bathymetry | 1 |",
                "| GPU resolution | 180 × 90 × 50; 360 × 180 × 50; 720 × 360 × 50; 1440 × 720 × 50 | `lat_lon` | Plain `LatitudeLongitudeGrid`, no bathymetry | 1 |",
                "| CPU scaling default | 360 × 180 × 50 | `tripolar` | `TripolarGrid` with immersed partial-cell bathymetry | 1, 2, 4, 8, 16, 32, 64, 128 |",
                "| CPU scaling fine | 720 × 360 × 50 | `tripolar` | `TripolarGrid` with immersed partial-cell bathymetry | 1, 2, 4, 8, 16, 32, 64, 128 |",
                "| GPU scaling fine | 720 × 360 × 50 | `tripolar` | `TripolarGrid` with immersed partial-cell bathymetry | 1, 2, 4 |",
                f"| GPU scaling super fine | 1440 × 720 × {super_fine_levels} | `lat_lon` | Plain `LatitudeLongitudeGrid`, no bathymetry | " + ", ".join(p.name.split("_")[0] for p in super_fine_results) + " |", "",
                "All timing runs pass `float_type=Float64`, `zstar_coordinate=false`,"
                " `momentum_advection=WENOVectorInvariantDefault`, `tracer_advection=WENO7`,"
                " `closure=CATKE`, `timestepper=SplitRungeKutta3`, and `tracers=T,S` to the runner."
                " The runner passes the corresponding objects and the listed dimensions and grid type"
                " to `earth_ocean`. Timing uses `dt=60` simulated seconds, 2 warmup steps,"
                " and 5 samples of 10 steps; each CPU rank has one Julia thread."
                " `earth_ocean` uses a 7-cell halo, exponentially spaced vertical levels over 5000 m,"
                " a split explicit free surface with 30 substeps, TEOS-10 seawater buoyancy,"
                " and spherical Coriolis. The latitude longitude domain spans 0–360° longitude"
                " and −80–85° latitude. These are model settings, not extra command-line arguments.", "",
                "The 1440 GPU scaling run uses `lat_lon` because the benchmark bathymetry dataset"
                " has no 1440 × 720 tripolar file. Its timings therefore differ in both resolution"
                " and grid type from GPU scaling fine; compare MPI efficiency within each series.", "",
                "Resolution points show the ratio of adjacent step times. MPI efficiency uses the one-rank step time as its baseline, as in the Andi 5070 Ti reference. The data table directly follows each chart.", ""]
    missing_series = [title_for(series) for series in SERIES if series not in available_series]
    if missing_series:
        sections += ["Results pending: " + ", ".join(missing_series) + ".", ""]
    for series in available_series:
        name = title_for(series)
        chart = "mpi_efficiency.svg" if "scaling" in series else "scaling_factor_scatter.svg"
        report = root / series / "plot.md"
        sections += [f"## {name}", "", f"![{name} chart]({series}/{chart})", "",
                     report_table(report), ""]
        if series == "cpu_resolution":
            sections += ["The 360 → 720 CPU comparison also changes the grid from latitude longitude to tripolar geometry.", ""]
        elif series == "cpu_scaling_default":
            sections += ["At 64 and 128 CPU ranks the 360 × 180 horizontal grid does not divide evenly;"
                         " the last partitions receive the leftover cells, and the chart uses the slowest rank."
                         " The 128-rank partition is 8 × 16 × 1 to keep x evenly divided across the tripolar fold.", ""]
        elif series == "gpu_scaling_super_fine" and (root / series / "1_gpus/attempt.md").exists():
            sections += ["The one-GPU case exceeded available GPU memory before warmup. MPI efficiency is normalized to the two-GPU baseline: (two-GPU step time ÷ current step time) × 2 ÷ GPU count × 100%. See [rerun provenance](gpu_scaling_super_fine/rerun.md).", ""]
        sections += [f"[Method and source data]({series}/plot.md)", ""]
    sections += ["## Nsight profiles", "",
                 "These profiling cases use `tripolar` grids with immersed partial-cell bathymetry"
                 " and the same model parameters above, but use 2 warmup steps and 1 sample of 2 steps.", "",
                 "GPU pies use summed kernel durations; the CPU pie uses exclusive leaf-frame sample counts. The captures include startup, compilation, warmup and measured steps.", ""]
    for label, path in [("GPU 360 × 180 × 50", "nsys_gpu/360x180x50"),
                        ("GPU 720 × 360 × 50", "nsys_gpu/720x360x50"),
                        ("CPU 720 × 360 × 50", "nsys_cpu/720x360x50")]:
        sections += [f"### {label}", "", f"![{label} activity pie]({path}/pie_chart.svg)", "",
                     report_table(root / path / "plot.md"), "", f"[Method and source data]({path}/plot.md)", ""]
    (root / "plots.md").write_text("\n".join(sections))


if __name__ == "__main__":
    main()
