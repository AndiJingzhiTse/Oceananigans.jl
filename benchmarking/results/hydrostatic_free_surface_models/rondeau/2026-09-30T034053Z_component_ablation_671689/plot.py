#!/usr/bin/env python3
"""Plot minimum GPU step times from the saved component ablation results."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


root = Path(__file__).resolve().parent
cases = [
    ("baseline", "Baseline"),
    ("no_tracer_advection", "No tracer advection"),
    ("no_coriolis", "No Coriolis"),
    ("no_buoyancy", "No buoyancy"),
    ("no_closure", "No closure"),
    ("no_tracers", "No user tracers¹"),
]

times = []
for directory, _ in cases:
    records = json.loads((root / directory / "results.json").read_text())
    times.append(min(record["time_per_step_seconds"] for record in records) * 1000)

plt.rcParams.update({"svg.hashsalt": "rondeau-component-ablation", "svg.fonttype": "none"})
fig, ax = plt.subplots(figsize=(9, 5.2))
bars = ax.barh(
    [label for _, label in cases],
    times,
    color=["#245a81"] + ["#489b9b"] * 4 + ["#d3914e"],
)
ax.invert_yaxis()
ax.set_xlim(0, max(times) * 1.19)
ax.set_xlabel("Minimum time per step (ms; lower is faster)")
ax.set_title("Earth ocean component ablation · one A100 GPU", loc="left", pad=14)
ax.grid(axis="x", alpha=0.2)
ax.set_axisbelow(True)
for bar, value in zip(bars, times):
    ax.text(value + 0.45, bar.get_y() + bar.get_height() / 2, f"{value:.3f}", va="center")
fig.text(0.01, 0.01, "360 × 180 × 50 tripolar, Float32 · ¹ Also disables buoyancy", fontsize=9, color="#555555")
fig.tight_layout(rect=(0, 0.04, 1, 1))
svg_path = root / "component_ablation.svg"
fig.savefig(svg_path, metadata={"Date": None})
svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines()) + "\n")
fig.savefig(root / "component_ablation.png", dpi=180, metadata={"Software": "Matplotlib"})
