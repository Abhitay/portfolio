"""
Growth Allocation Engine - Publication-Ready Visualizations

This script generates executive-level diagrams explaining the growth decision logic:
1. Incremental LTV by Channel (why high-conversion ≠ high value)
2. Naive vs Optimized Budget Allocation (reallocation strategy)
3. Spend vs Incremental Value (channel saturation & diminishing returns)
4. ROI vs Incremental LTV Scatter (why ROI-based decisions mislead)
5. Executive Summary Diagram (data flow & decision framework)

Data Sources:
- channel_summary.csv: base channel metrics (incremental_ltv, avg_cost)
- baseline_allocation.csv: equal/proportional baseline spend
- optimal_allocation.csv: MILP-optimized allocation
- incremental_ltv_results.csv: causal incremental LTV per channel

Do NOT modify or retrain models. These are read-only visualizations.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

# Set style for publication-ready plots
plt.style.use("seaborn-v0_8-darkgrid")
sns.set_palette("husl")

# Ensure figures directory exists
figures_dir = Path("growth_engine/figures")
figures_dir.mkdir(exist_ok=True, parents=True)

# ============================================================================
# DATA LOADING
# ============================================================================

# Base channel metrics (incremental LTV and cost per user)
channel_summary = pd.read_csv("growth_engine/datadesign/channel_summary.csv")

# Baseline allocation (proportional or equal spend)
baseline_allocation = pd.read_csv("growth_engine/datadesign/baseline_allocation.csv")

# Optimal allocation (MILP-optimized)
optimal_allocation = pd.read_csv("growth_engine/datadesign/optimal_allocation.csv")

# Incremental LTV results (causal estimates from uplift + LTV models)
incremental_ltv = pd.read_csv("growth_engine/datadesign/incremental_ltv_results.csv")

print("✓ Loaded data:")
print(f"  - {len(channel_summary)} channels with incremental LTV metrics")
print(f"  - Baseline allocation: ${baseline_allocation['spend'].sum():,.0f}")
print(f"  - Optimal allocation: ${optimal_allocation['optimal_spend'].sum():,.0f}")

# ============================================================================
# 1. INCREMENTAL LTV BY CHANNEL
# ============================================================================
# Purpose: Show why high-conversion channels (paid_search) have lower
#          incremental value than high-trust channels (referral).
#          This justifies favoring causal LTV over naive conversion rates.

fig, ax = plt.subplots(figsize=(10, 6))

# Sort by incremental_ltv descending
sorted_channels = channel_summary.sort_values("incremental_ltv", ascending=True)

colors = ["#2ecc71" if x > sorted_channels["incremental_ltv"].median() else "#e74c3c" 
          for x in sorted_channels["incremental_ltv"]]

bars = ax.barh(
    sorted_channels["channel"],
    sorted_channels["incremental_ltv"],
    color=colors,
    edgecolor="black",
    linewidth=1.5,
    alpha=0.85
)

# Annotation: Add value labels
for i, (channel, value) in enumerate(zip(sorted_channels["channel"], sorted_channels["incremental_ltv"])):
    ax.text(
        value + 0.3,
        i,
        f"${value:.2f}",
        va="center",
        fontsize=11,
        fontweight="bold"
    )

ax.set_xlabel("Incremental LTV per User ($)", fontsize=12, fontweight="bold")
ax.set_ylabel("Channel", fontsize=12, fontweight="bold")
ax.set_title(
    "Incremental LTV by Channel\n(Causal Attribution: Why ROI ≠ Incremental Value)",
    fontsize=13,
    fontweight="bold",
    pad=20
)
ax.grid(axis="x", alpha=0.3, linestyle="--")
ax.set_xlim(0, sorted_channels["incremental_ltv"].max() * 1.15)

# Add footnote
fig.text(
    0.99, 0.01,
    "Green: Above median | Red: Below median. Causal uplift + Cox survival model.",
    ha="right", fontsize=9, style="italic", color="gray"
)

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig(figures_dir / "01_incremental_ltv_by_channel.png", dpi=300, bbox_inches="tight")
print("\n✓ Saved: 01_incremental_ltv_by_channel.png")
plt.close()

# ============================================================================
# 2. NAIVE VS OPTIMIZED BUDGET ALLOCATION
# ============================================================================
# Purpose: Show the reallocation strategy. Highlight:
#   - Paid search: spend cap due to diminishing returns
#   - Referral: maintains high spend (best causal value)
#   - Organic: increase from constraints to full allocation
#   - Social ads: absent or minimal (poor incremental value)

fig, ax = plt.subplots(figsize=(12, 6))

# Merge baseline and optimal
allocation_comparison = baseline_allocation.merge(
    optimal_allocation[["channel", "optimal_spend"]],
    on="channel",
    how="outer"
)

allocation_comparison = allocation_comparison.fillna(0)

# Ensure both dataframes have same channels
channels = sorted(allocation_comparison["channel"].unique())
x = np.arange(len(channels))
width = 0.35

# Prepare data for grouped bar chart
baseline_spend = []
optimal_spend = []

for ch in channels:
    baseline_val = allocation_comparison[allocation_comparison["channel"] == ch]["spend"].values
    optimal_val = allocation_comparison[allocation_comparison["channel"] == ch]["optimal_spend"].values
    
    baseline_spend.append(baseline_val[0] if len(baseline_val) > 0 else 0)
    optimal_spend.append(optimal_val[0] if len(optimal_val) > 0 else 0)

# Create bars
bars1 = ax.bar(x - width/2, baseline_spend, width, label="Baseline (Equal/Proportional)", 
               color="#3498db", edgecolor="black", linewidth=1.2, alpha=0.85)
bars2 = ax.bar(x + width/2, optimal_spend, width, label="Optimized (MILP)", 
               color="#e74c3c", edgecolor="black", linewidth=1.2, alpha=0.85)

# Add value labels and delta annotations
for i, (base, opt) in enumerate(zip(baseline_spend, optimal_spend)):
    delta = opt - base
    
    # Baseline value
    ax.text(i - width/2, base + 5000, f"${base/1e3:.0f}k", 
            ha="center", va="bottom", fontsize=9, fontweight="bold")
    
    # Optimal value
    ax.text(i + width/2, opt + 5000, f"${opt/1e3:.0f}k", 
            ha="center", va="bottom", fontsize=9, fontweight="bold")
    
    # Delta annotation
    if abs(delta) > 5000:
        arrow = "↑" if delta > 0 else "↓"
        color = "#27ae60" if delta > 0 else "#c0392b"
        ax.text(i, max(base, opt) + 30000, f"{arrow} {abs(delta)/1e3:.0f}k",
                ha="center", va="bottom", fontsize=8, color=color, fontweight="bold")

ax.set_xlabel("Channel", fontsize=12, fontweight="bold")
ax.set_ylabel("Budget Allocation ($)", fontsize=12, fontweight="bold")
ax.set_title(
    "Budget Reallocation: Baseline vs Optimized\n(MILP Optimization with Causal LTV)",
    fontsize=13,
    fontweight="bold",
    pad=20
)
ax.set_xticks(x)
ax.set_xticklabels(channels, fontsize=11)
ax.legend(fontsize=11, loc="upper left", framealpha=0.95)
ax.grid(axis="y", alpha=0.3, linestyle="--")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x/1e3:.0f}k"))

fig.text(
    0.99, 0.01,
    "Reallocation driven by: incremental LTV, cost per user, and channel capacity constraints.",
    ha="right", fontsize=9, style="italic", color="gray"
)

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig(figures_dir / "02_naive_vs_optimized_allocation.png", dpi=300, bbox_inches="tight")
print("✓ Saved: 02_naive_vs_optimized_allocation.png")
plt.close()

# ============================================================================
# 3. SPEND VS INCREMENTAL VALUE (CHANNEL SATURATION)
# ============================================================================
# Purpose: Bubble chart showing spend vs expected incremental value.
#          Saturation = high spend, low marginal value per dollar.
#          Justifies MILP constraints and capped spend on paid_search.

fig, ax = plt.subplots(figsize=(11, 7))

# Merge optimal allocation with channel metrics
saturation_data = optimal_allocation.merge(
    channel_summary[["channel", "incremental_ltv", "avg_cost"]],
    on="channel"
)

# Calculate expected incremental value per dollar (value per cost)
saturation_data["value_per_dollar"] = saturation_data["incremental_ltv"] / saturation_data["avg_cost"]

# Bubble size = avg_cost (cost per user, proxy for volume/saturation)
bubble_sizes = saturation_data["avg_cost"] * 1000  # Scale for visibility

# Color by incremental LTV (higher = greener)
colors_scatter = saturation_data["incremental_ltv"]

scatter = ax.scatter(
    saturation_data["optimal_spend"],
    saturation_data["expected_incremental_value"],
    s=bubble_sizes,
    c=colors_scatter,
    cmap="RdYlGn",
    alpha=0.6,
    edgecolors="black",
    linewidth=2,
    vmin=channel_summary["incremental_ltv"].min(),
    vmax=channel_summary["incremental_ltv"].max()
)

# Annotate each bubble with channel name
for idx, row in saturation_data.iterrows():
    ax.annotate(
        row["channel"],
        (row["optimal_spend"], row["expected_incremental_value"]),
        fontsize=10,
        fontweight="bold",
        ha="center",
        va="center"
    )

ax.set_xlabel("Optimized Spend ($)", fontsize=12, fontweight="bold")
ax.set_ylabel("Expected Incremental Value ($)", fontsize=12, fontweight="bold")
ax.set_title(
    "Channel Saturation & Diminishing Returns\n(Bubble Size = Cost per User)",
    fontsize=13,
    fontweight="bold",
    pad=20
)

# Add colorbar
cbar = plt.colorbar(scatter, ax=ax, label="Incremental LTV ($)")
cbar.set_label("Incremental LTV ($)", fontsize=11, fontweight="bold")

# Format axes
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x/1e3:.0f}k"))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x/1e6:.1f}M"))
ax.grid(alpha=0.3, linestyle="--")

fig.text(
    0.99, 0.01,
    "Interpretation: Paid search shows high spend but lower incremental value (saturation).\n"
    "Organic grows with budget but constrained by reach.",
    ha="right", fontsize=8, style="italic", color="gray"
)

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig(figures_dir / "03_spend_vs_incremental_value_saturation.png", dpi=300, bbox_inches="tight")
print("✓ Saved: 03_spend_vs_incremental_value_saturation.png")
plt.close()

# ============================================================================
# 4. ROI VS INCREMENTAL LTV SCATTER
# ============================================================================
# Purpose: Demonstrate why naive ROI (value/cost) misleads budget allocation.
#          ROI-optimized allocation differs from causal incremental LTV allocation.
#          X: Naive ROI, Y: Incremental LTV, labeled by channel.

fig, ax = plt.subplots(figsize=(11, 7))

# Calculate naive ROI (incremental LTV / avg cost per user)
roi_analysis = channel_summary.copy()
roi_analysis["naive_roi"] = roi_analysis["incremental_ltv"] / roi_analysis["avg_cost"]

# Size by average cost (proxy for market opportunity)
bubble_sizes_roi = roi_analysis["avg_cost"] * 2000

scatter_roi = ax.scatter(
    roi_analysis["naive_roi"],
    roi_analysis["incremental_ltv"],
    s=bubble_sizes_roi,
    c=roi_analysis["incremental_ltv"],
    cmap="viridis",
    alpha=0.6,
    edgecolors="black",
    linewidth=2
)

# Annotate channels
for idx, row in roi_analysis.iterrows():
    ax.annotate(
        row["channel"],
        (row["naive_roi"], row["incremental_ltv"]),
        fontsize=10,
        fontweight="bold",
        ha="center",
        va="center"
    )

# Add reference lines to highlight quadrants
median_roi = roi_analysis["naive_roi"].median()
median_ltv = roi_analysis["incremental_ltv"].median()

ax.axvline(median_roi, color="gray", linestyle="--", linewidth=2, alpha=0.5, label="Median ROI")
ax.axhline(median_ltv, color="gray", linestyle="--", linewidth=2, alpha=0.5, label="Median Incremental LTV")

ax.set_xlabel("Naive ROI (Incremental LTV / Avg Cost)", fontsize=12, fontweight="bold")
ax.set_ylabel("Incremental LTV per User ($)", fontsize=12, fontweight="bold")
ax.set_title(
    "Why ROI-Based Decisions Mislead: ROI vs Incremental LTV\n"
    "(Bubble Size = Market Opportunity)",
    fontsize=13,
    fontweight="bold",
    pad=20
)

cbar_roi = plt.colorbar(scatter_roi, ax=ax, label="Incremental LTV ($)")
ax.grid(alpha=0.3, linestyle="--")
ax.legend(fontsize=10, loc="lower right")

# Quadrant annotations
ax.text(0.98, 0.98, "High ROI\nHigh LTV\n(Ideal)", 
        transform=ax.transAxes, fontsize=9, ha="right", va="top",
        bbox=dict(boxstyle="round", facecolor="#2ecc71", alpha=0.3))
ax.text(0.02, 0.98, "Low ROI\nHigh LTV\n(Trust Value)", 
        transform=ax.transAxes, fontsize=9, ha="left", va="top",
        bbox=dict(boxstyle="round", facecolor="#f39c12", alpha=0.3))
ax.text(0.98, 0.02, "High ROI\nLow LTV\n(Avoid)", 
        transform=ax.transAxes, fontsize=9, ha="right", va="bottom",
        bbox=dict(boxstyle="round", facecolor="#e74c3c", alpha=0.3))

fig.text(
    0.99, -0.02,
    "Insight: Paid search has high ROI but low incremental LTV (new users to low-value segments).\n"
    "Referral has lower ROI but high incremental LTV (self-selecting, high-value users).",
    ha="right", fontsize=8, style="italic", color="gray"
)

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig(figures_dir / "04_roi_vs_incremental_ltv_scatter.png", dpi=300, bbox_inches="tight")
print("✓ Saved: 04_roi_vs_incremental_ltv_scatter.png")
plt.close()

# ============================================================================
# 5. EXECUTIVE SUMMARY DIAGRAM (Flow Chart)
# ============================================================================
# Purpose: High-level storytelling diagram showing the decision framework.
#          Data → Uplift → LTV → Optimization → Allocation

fig, ax = plt.subplots(figsize=(14, 6))

# Define flow boxes
flow_steps = [
    {
        "name": "Data Collection",
        "y": 0.5,
        "x": 0.05,
        "details": "User demographics,\nchannel exposure,\nconversion & revenue"
    },
    {
        "name": "Causal Uplift\nEstimation",
        "y": 0.5,
        "x": 0.22,
        "details": "XGBoost treatment\neffect modeling\nper user, per channel"
    },
    {
        "name": "LTV Forecast\n(Survival Model)",
        "y": 0.5,
        "x": 0.39,
        "details": "Cox PH regression\nwith churn hazard\ndiscount rate: 10%"
    },
    {
        "name": "Incremental Value\nCalculation",
        "y": 0.5,
        "x": 0.56,
        "details": "Uplift × LTV\nper channel\naggregated metrics"
    },
    {
        "name": "MILP Budget\nOptimization",
        "y": 0.5,
        "x": 0.73,
        "details": "OR-Tools solver\nmax total value\nsubject to constraints"
    },
    {
        "name": "Allocation\nDecision",
        "y": 0.5,
        "x": 0.90,
        "details": "Deploy budget\nper channel\nexpected return"
    },
]

# Draw boxes and labels
for step in flow_steps:
    # Box
    box = plt.Rectangle(
        (step["x"] - 0.055, step["y"] - 0.12),
        0.11, 0.24,
        transform=ax.transAxes,
        facecolor="#ecf0f1",
        edgecolor="#34495e",
        linewidth=2.5,
        zorder=2
    )
    ax.add_patch(box)
    
    # Title
    ax.text(
        step["x"], step["y"] + 0.09,
        step["name"],
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
        ha="center",
        va="center",
        zorder=3
    )
    
    # Details (smaller font)
    ax.text(
        step["x"], step["y"] - 0.015,
        step["details"],
        transform=ax.transAxes,
        fontsize=7,
        ha="center",
        va="center",
        style="italic",
        color="#555",
        zorder=3
    )

# Draw arrows between boxes
arrow_props = dict(arrowstyle="-|>", lw=2.5, color="#34495e")
for i in range(len(flow_steps) - 1):
    ax.annotate(
        "",
        xy=(flow_steps[i+1]["x"] - 0.056, flow_steps[i+1]["y"]),
        xytext=(flow_steps[i]["x"] + 0.056, flow_steps[i]["y"]),
        xycoords="axes fraction",
        textcoords="axes fraction",
        arrowprops=arrow_props,
        zorder=1
    )

# Add title and remove axes
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(0, 1)
ax.axis("off")

fig.suptitle(
    "Growth Allocation Decision Framework\nData → Causal Analysis → Optimization → Deployment",
    fontsize=14,
    fontweight="bold",
    y=0.98
)

# Add key insight box at bottom
insight_text = (
    "Key Insight: Incremental LTV (causal effect on user lifetime value) ≠ ROI (value per acquisition cost).\n"
    "High-trust channels (referral) may have lower ROI but higher incremental value, justifying higher allocation."
)

fig.text(
    0.5, 0.05,
    insight_text,
    ha="center", fontsize=9, style="italic",
    bbox=dict(boxstyle="round", facecolor="#fff3cd", alpha=0.8, pad=1)
)

plt.tight_layout(rect=[0, 0.12, 1, 0.94])
plt.savefig(figures_dir / "05_executive_summary_flow.png", dpi=300, bbox_inches="tight")
print("✓ Saved: 05_executive_summary_flow.png")
plt.close()

# ============================================================================
# SUMMARY REPORT
# ============================================================================

print("\n" + "="*70)
print("VISUALIZATION GENERATION COMPLETE")
print("="*70)

print("\nGenerated Files:")
print(f"  1. 01_incremental_ltv_by_channel.png")
print(f"     → Causal LTV per user by channel (why referral > paid search)")
print(f"\n  2. 02_naive_vs_optimized_allocation.png")
print(f"     → Budget reallocation: baseline vs MILP-optimized")
print(f"\n  3. 03_spend_vs_incremental_value_saturation.png")
print(f"     → Spend vs expected value (diminishing returns, saturation)")
print(f"\n  4. 04_roi_vs_incremental_ltv_scatter.png")
print(f"     → Why ROI-based decisions mislead (4-quadrant analysis)")
print(f"\n  5. 05_executive_summary_flow.png")
print(f"     → Decision framework (storytelling, non-technical)")

print(f"\nLocation: {figures_dir.resolve()}")

# Print key metrics for reference
print("\n" + "="*70)
print("KEY METRICS")
print("="*70)

print("\nChannel Performance (Ranked by Incremental LTV):")
for idx, row in channel_summary.sort_values("incremental_ltv", ascending=False).iterrows():
    print(f"  {row['channel']:<15} Incremental LTV: ${row['incremental_ltv']:>6.2f}  |  Avg Cost: ${row['avg_cost']:.4f}")

print("\nBudget Shift (Baseline → Optimal):")
for idx, row in allocation_comparison.iterrows():
    baseline = row["spend"]
    optimal = row["optimal_spend"]
    delta = optimal - baseline
    pct_change = (delta / baseline * 100) if baseline > 0 else 0
    sign = "+" if delta > 0 else ""
    print(f"  {row['channel']:<15} ${baseline/1e3:>6.0f}k → ${optimal/1e3:>6.0f}k  ({sign}{pct_change:>6.1f}%)")

total_baseline_value = baseline_allocation["expected_incremental_value"].sum()
total_optimal_value = optimal_allocation["expected_incremental_value"].sum()
value_uplift = total_optimal_value - total_baseline_value
value_uplift_pct = (value_uplift / total_baseline_value * 100)

print(f"\nTotal Expected Value:")
print(f"  Baseline: ${total_baseline_value:>12,.0f}")
print(f"  Optimal:  ${total_optimal_value:>12,.0f}")
print(f"  Uplift:   ${value_uplift:>12,.0f} ({value_uplift_pct:+.1f}%)")

print("\n" + "="*70)
