"""
Growth Allocation Engine — Publication-Ready Visualizations (CLEAN VERSION)

This script generates executive-facing figures explaining causal growth allocation.

Figures:
1. Incremental LTV by Channel
2. Baseline vs Optimized Budget Allocation
3. Spend vs Incremental Value (Saturation)
4. ROI vs Incremental LTV
5. Executive Decision Framework

IMPORTANT:
- Read-only: no model retraining
- Optimized for clarity, not density
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

# -----------------------------
# Paths
# -----------------------------
DATA_DIR = Path("growth_engine/datadesign")
FIG_DIR = Path("growth_engine/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Load Data (schema-accurate)
# -----------------------------
channel_summary = pd.read_csv(DATA_DIR / "channel_summary.csv")
baseline_alloc = pd.read_csv(DATA_DIR / "baseline_allocation.csv")
optimal_alloc = pd.read_csv(DATA_DIR / "optimal_allocation.csv")

# -----------------------------
# Derived Metrics
# -----------------------------
channel_summary["roi"] = (
    channel_summary["incremental_ltv"] /
    channel_summary["avg_cost"]
)

baseline_total = baseline_alloc["expected_incremental_value"].sum()
optimal_total = optimal_alloc["expected_incremental_value"].sum()
delta_value = optimal_total - baseline_total
delta_pct = delta_value / baseline_total * 100

# ============================================================================
# FIGURE 1 — Incremental LTV by Channel
# ============================================================================
plt.figure(figsize=(9, 5))

sorted_channels = channel_summary.sort_values("incremental_ltv")

bars = plt.barh(
    sorted_channels["channel"],
    sorted_channels["incremental_ltv"],
    color="#2563eb",
    alpha=0.9
)

for i, val in enumerate(sorted_channels["incremental_ltv"]):
    plt.text(
        val - 0.6,
        i,
        f"${val:.2f}",
        va="center",
        ha="right",
        color="white",
        fontsize=11,
        fontweight="bold"
    )

plt.xlabel("Incremental LTV per User ($)")
plt.title("Incremental LTV by Acquisition Channel")
plt.xlim(0, sorted_channels["incremental_ltv"].max() * 1.05)
plt.tight_layout()
plt.savefig(FIG_DIR / "01_incremental_ltv_by_channel.png", dpi=300)
plt.close()

# ============================================================================
# FIGURE 2 — Baseline vs Optimized Allocation
# ============================================================================
alloc_compare = baseline_alloc.merge(
    optimal_alloc,
    on="channel",
    how="inner"
)

x = np.arange(len(alloc_compare))
width = 0.35

plt.figure(figsize=(10, 5))

plt.bar(
    x - width/2,
    alloc_compare["spend"],
    width,
    label="Baseline",
    color="#94a3b8"
)

plt.bar(
    x + width/2,
    alloc_compare["optimal_spend"],
    width,
    label="Optimized",
    color="#2563eb"
)

for i, (base, opt) in enumerate(
    zip(alloc_compare["spend"], alloc_compare["optimal_spend"])
):
    plt.text(i - width/2, base * 1.02, f"${base/1e3:.0f}k", ha="center", fontsize=9)
    plt.text(i + width/2, opt * 1.02, f"${opt/1e3:.0f}k", ha="center", fontsize=9)

plt.xticks(x, alloc_compare["channel"], rotation=15)
plt.ylabel("Spend ($)")
plt.title(
    f"Budget Reallocation: Baseline vs Optimized\n"
    f"Same $500k budget → +${delta_value:,.0f} incremental value (+{delta_pct:.1f}%)"
)
plt.legend()
plt.tight_layout()
plt.savefig(FIG_DIR / "02_naive_vs_optimized_allocation.png", dpi=300)
plt.close()

# ============================================================================
# FIGURE 3 — Spend vs Incremental Value (Saturation)
# ============================================================================
sat = optimal_alloc.merge(
    channel_summary,
    on="channel",
    how="left"
)

bubble_sizes = np.log1p(sat["avg_cost"]) * 1200

plt.figure(figsize=(9, 6))

scatter = plt.scatter(
    sat["optimal_spend"],
    sat["expected_incremental_value"],
    s=bubble_sizes,
    c=sat["incremental_ltv"],
    cmap="viridis",
    alpha=0.45,
    edgecolors="black"
)

for _, row in sat.iterrows():
    plt.annotate(
        row["channel"],
        (row["optimal_spend"], row["expected_incremental_value"]),
        xytext=(6, 6),
        textcoords="offset points",
        fontsize=9,
        fontweight="bold"
    )

plt.xlabel("Optimized Spend ($)")
plt.ylabel("Expected Incremental Value ($)")
plt.title("Channel Saturation & Diminishing Returns")
plt.colorbar(scatter, label="Incremental LTV")
plt.gca().xaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, _: f"${x/1e3:.0f}k")
)
plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M")
)
plt.tight_layout()
plt.savefig(FIG_DIR / "03_spend_vs_incremental_value_saturation.png", dpi=300)
plt.close()

# ============================================================================
# FIGURE 4 — ROI vs Incremental LTV
# ============================================================================
roi = channel_summary.copy()
roi["naive_roi"] = roi["incremental_ltv"] / roi["avg_cost"]

bubble_sizes = np.log1p(roi["avg_cost"]) * 800

plt.figure(figsize=(9, 6))

scatter = plt.scatter(
    roi["naive_roi"],
    roi["incremental_ltv"],
    s=bubble_sizes,
    c=roi["incremental_ltv"],
    cmap="viridis",
    alpha=0.5,
    edgecolors="black"
)

for _, row in roi.iterrows():
    plt.annotate(
        row["channel"],
        (row["naive_roi"], row["incremental_ltv"]),
        xytext=(6, 6),
        textcoords="offset points",
        fontsize=9,
        fontweight="bold"
    )

plt.axvline(roi["naive_roi"].median(), linestyle="--", color="gray", alpha=0.5)
plt.axhline(roi["incremental_ltv"].median(), linestyle="--", color="gray", alpha=0.5)

plt.xlabel("Naive ROI (Incremental LTV / Cost)")
plt.ylabel("Incremental LTV per User ($)")
plt.title("Why ROI-Based Allocation Misleads")
plt.tight_layout()
plt.savefig(FIG_DIR / "04_roi_vs_incremental_ltv_scatter.png", dpi=300)
plt.close()

# ============================================================================
# FIGURE 5 — Executive Summary Flow
# ============================================================================
plt.figure(figsize=(11, 3))
plt.axis("off")

steps = [
    "User & Channel Data",
    "Causal Uplift",
    "LTV Forecast",
    "Incremental Value",
    "Budget Optimization",
    "Allocation Decision"
]

for i, step in enumerate(steps):
    plt.text(
        i,
        0.5,
        step,
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#e5e7eb")
    )

for i in range(len(steps) - 1):
    plt.arrow(i + 0.25, 0.5, 0.5, 0, head_width=0.04, color="black")

plt.xlim(-0.5, len(steps))
plt.title("Growth Allocation Decision Framework")
plt.tight_layout()
plt.savefig(FIG_DIR / "05_executive_summary_flow.png", dpi=300)
plt.close()

# ============================================================================
# SUMMARY
# ============================================================================
print("\nVISUALIZATION GENERATION COMPLETE\n")
print(f"Baseline Expected Value: ${baseline_total:,.0f}")
print(f"Optimized Expected Value: ${optimal_total:,.0f}")
print(f"Incremental Gain: ${delta_value:,.0f} ({delta_pct:.2f}%)")
print(f"Figures saved to: {FIG_DIR.resolve()}")
