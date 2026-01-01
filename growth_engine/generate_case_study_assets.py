import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = "growth_engine"
DATA_DIR = os.path.join(BASE_DIR, "datadesign")
FIG_DIR = os.path.join(BASE_DIR, "figures")

os.makedirs(FIG_DIR, exist_ok=True)

# -----------------------------
# Load Data
# -----------------------------
users = pd.read_csv(os.path.join(DATA_DIR, "users.csv"))
events = None
if os.path.exists(os.path.join(DATA_DIR, "events.csv")):
    events = pd.read_csv(os.path.join(DATA_DIR, "events.csv"))

channel_summary = pd.read_csv(os.path.join(DATA_DIR, "channel_summary.csv"))
baseline_alloc = pd.read_csv(os.path.join(DATA_DIR, "baseline_allocation.csv"))
optimal_alloc = pd.read_csv(os.path.join(DATA_DIR, "optimal_allocation.csv"))

# -----------------------------
# Derived Metrics
# -----------------------------
channel_summary["roi"] = (
    channel_summary["incremental_ltv"] / channel_summary["avg_cost"]
)

baseline_total = baseline_alloc["expected_incremental_value"].sum()
optimal_total = optimal_alloc["expected_incremental_value"].sum()

delta_value = optimal_total - baseline_total
delta_pct = delta_value / baseline_total * 100

# -----------------------------
# Print Numbers for Case Study
# -----------------------------
print("\n=== VALUE SUMMARY ===")
print(f"Baseline Expected Value: ${baseline_total:,.0f}")
print(f"Optimized Expected Value: ${optimal_total:,.0f}")
print(f"Incremental Gain: ${delta_value:,.0f} ({delta_pct:.2f}%)")

print("\n=== USERS HEAD ===")
print(users.head())

if events is not None:
    print("\n=== EVENTS HEAD ===")
    print(events.head())

print("\n=== SEGMENT DISTRIBUTION ===")
print(
    users["engagement_segment"]
    .value_counts(normalize=True)
    .mul(100)
    .round(1)
)

# -----------------------------
# FIGURE 1: Incremental LTV by Channel
# -----------------------------
plt.figure(figsize=(8, 5))
channel_summary.sort_values("incremental_ltv").plot(
    kind="barh",
    x="channel",
    y="incremental_ltv",
    legend=False
)
plt.title("Incremental LTV by Acquisition Channel")
plt.xlabel("Incremental LTV per User ($)")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "01_incremental_ltv_by_channel.png"))
plt.close()

# -----------------------------
# FIGURE 2: ROI vs Incremental LTV
# -----------------------------
plt.figure(figsize=(7, 6))
plt.scatter(
    channel_summary["roi"],
    channel_summary["incremental_ltv"],
    s=120
)

for _, row in channel_summary.iterrows():
    plt.text(
        row["roi"] + 0.02,
        row["incremental_ltv"],
        row["channel"]
    )

plt.xlabel("Naive ROI (Incremental LTV / Cost)")
plt.ylabel("Incremental LTV per User ($)")
plt.title("ROI vs Incremental LTV")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "04_roi_vs_incremental_ltv_scatter.png"))
plt.close()

# -----------------------------
# FIGURE 3: Spend vs Incremental Value (Saturation)
# -----------------------------
merged = optimal_alloc.merge(
    channel_summary,
    on="channel",
    how="left"
)

plt.figure(figsize=(8, 6))
plt.scatter(
    merged["optimal_spend"],
    merged["expected_incremental_value"],
    s=merged["avg_cost"] * 80,
    c=merged["incremental_ltv"],
    cmap="viridis"
)

for _, row in merged.iterrows():
    plt.text(
        row["optimal_spend"] * 1.01,
        row["expected_incremental_value"],
        row["channel"]
    )

plt.xlabel("Spend ($)")
plt.ylabel("Expected Incremental Value ($)")
plt.title("Spend vs Incremental Value (Channel Saturation)")
plt.colorbar(label="Incremental LTV")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "03_spend_vs_incremental_value_saturation.png"))
plt.close()

# -----------------------------
# FIGURE 4: Baseline vs Optimized Allocation
# -----------------------------
alloc_compare = baseline_alloc.merge(
    optimal_alloc,
    on="channel",
    suffixes=("_baseline", "_optimal")
)

x = np.arange(len(alloc_compare))
width = 0.35

plt.figure(figsize=(9, 5))
plt.bar(x - width/2, alloc_compare["spend"], width, label="Baseline")
plt.bar(x + width/2, alloc_compare["optimal_spend"], width, label="Optimized")

plt.xticks(x, alloc_compare["channel"], rotation=20)
plt.ylabel("Spend ($)")
plt.title("Baseline vs Optimized Budget Allocation")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "02_naive_vs_optimized_allocation.png"))
plt.close()

# -----------------------------
# FIGURE 5: Executive Summary Flow
# -----------------------------
plt.figure(figsize=(10, 3))
plt.axis("off")

steps = [
    "User + Channel Data",
    "Causal Uplift\nEstimation",
    "LTV\nForecasting",
    "Incremental Value\nCalculation",
    "MILP Budget\nOptimization",
    "Allocation\nDecision"
]

for i, step in enumerate(steps):
    plt.text(i, 0.5, step, ha="center", va="center", bbox=dict(boxstyle="round"))

for i in range(len(steps) - 1):
    plt.arrow(i + 0.25, 0.5, 0.5, 0, head_width=0.03)

plt.xlim(-0.5, len(steps))
plt.title("Growth Allocation Decision Framework")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "05_executive_summary_flow.png"))
plt.close()

print("\nAll figures saved to growth_engine/figures/")
