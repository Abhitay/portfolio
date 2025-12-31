import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from ortools.linear_solver import pywraplp

st.set_page_config(page_title="Growth Allocation Engine", layout="wide")

# ======================================================
# Load channel-level metrics (from optimization notebook)
# ======================================================
channel_summary = pd.read_csv(
    "growth_engine/datadesign/channel_summary.csv"
)
# expected columns:
# channel, incremental_ltv, avg_cost

channel_summary = channel_summary.set_index("channel")

CHANNELS = channel_summary.index.tolist()

# ======================================================
# Sidebar: Scenario Controls
# ======================================================
st.sidebar.header("Scenario Controls")

TOTAL_BUDGET = st.sidebar.slider(
    "Total Acquisition Budget ($)",
    min_value=100_000,
    max_value=2_000_000,
    value=500_000,
    step=50_000
)

# Percent-based constraints
MAX_SPEND_PCT = {
    "paid_search": 0.40,
    "social_ads": 0.30,
    "affiliate": 0.20,
    "referral": 0.16,
    "organic": 0.10,
}

MIN_SPEND_PCT = {
    "paid_search": 0.04,
    "social_ads": 0.02,
    "affiliate": 0.01,
    "referral": 0.01,
    "organic": 0.00,
}

MAX_SPEND = {c: TOTAL_BUDGET * MAX_SPEND_PCT[c] for c in CHANNELS}
MIN_SPEND = {c: TOTAL_BUDGET * MIN_SPEND_PCT[c] for c in CHANNELS}

# ======================================================
# Header
# ======================================================
st.title("Growth Allocation Engine")
st.caption(
    "Budget optimization using causal uplift, survival-based LTV, "
    "and constrained optimization"
)

# ======================================================
# 1️⃣ Feasible Baseline (Equal-Intent Strategy)
# ======================================================
equal_spend = TOTAL_BUDGET / len(CHANNELS)

baseline = pd.DataFrame({
    "channel": CHANNELS,
    "spend": equal_spend
})

# Apply min / max constraints
baseline["spend"] = baseline.apply(
    lambda r: min(
        max(r["spend"], MIN_SPEND[r["channel"]]),
        MAX_SPEND[r["channel"]]
    ),
    axis=1
)

# Reallocate remaining budget proportionally
remaining_budget = TOTAL_BUDGET - baseline["spend"].sum()

eligible = baseline[
    baseline["spend"] < baseline["channel"].map(MAX_SPEND)
].copy()

capacity = (
    eligible["channel"].map(MAX_SPEND).values
    - eligible["spend"].values
)

baseline.loc[eligible.index, "spend"] += (
    remaining_budget * capacity / capacity.sum()
)

# Compute baseline value
baseline = baseline.merge(
    channel_summary,
    left_on="channel",
    right_index=True
)

baseline["expected_incremental_value"] = (
    baseline["spend"]
    * baseline["incremental_ltv"]
    / baseline["avg_cost"]
)

baseline_total_value = baseline["expected_incremental_value"].sum()

# ======================================================
# 2️⃣ Optimized Allocation (MILP)
# ======================================================
solver = pywraplp.Solver.CreateSolver("GLOP")

x = {}
for c in CHANNELS:
    x[c] = solver.NumVar(
        MIN_SPEND[c],
        MAX_SPEND[c],
        f"spend_{c}"
    )

solver.Add(solver.Sum(x[c] for c in CHANNELS) <= TOTAL_BUDGET)

objective = solver.Objective()
for c in CHANNELS:
    value_per_dollar = (
        channel_summary.loc[c, "incremental_ltv"]
        / channel_summary.loc[c, "avg_cost"]
    )
    objective.SetCoefficient(x[c], value_per_dollar)

objective.SetMaximization()
solver.Solve()

optimal = pd.DataFrame({
    "channel": CHANNELS,
    "spend": [x[c].solution_value() for c in CHANNELS]
})

optimal = optimal.merge(
    channel_summary,
    left_on="channel",
    right_index=True
)

optimal["expected_incremental_value"] = (
    optimal["spend"]
    * optimal["incremental_ltv"]
    / optimal["avg_cost"]
)

optimal_total_value = optimal["expected_incremental_value"].sum()

# ======================================================
# 3️⃣ High-Level Metrics
# ======================================================
delta_value = optimal_total_value - baseline_total_value

col1, col2, col3 = st.columns(3)

col1.metric(
    "Baseline Expected Incremental LTV",
    f"${baseline_total_value:,.0f}"
)

col2.metric(
    "Optimized Expected Incremental LTV",
    f"${optimal_total_value:,.0f}"
)

col3.metric(
    "Incremental Lift",
    f"${delta_value:,.0f}",
    delta=f"{delta_value / baseline_total_value:.1%}"
)

st.markdown("---")


# ======================================================
# 4️⃣ Before vs After Spend
# ======================================================
st.subheader("Before vs After Budget Allocation")

fig, ax = plt.subplots(figsize=(9, 5))

ax.bar(
    baseline["channel"],
    baseline["spend"],
    label="Baseline",
    alpha=0.6
)

ax.bar(
    optimal["channel"],
    optimal["spend"],
    label="Optimized",
    alpha=0.85
)

ax.set_ylabel("Spend ($)")
ax.set_xlabel("Channel")
ax.legend()

st.pyplot(fig)

# ======================================================
# 5️⃣ Before vs After Value
# ======================================================
st.subheader("Expected Incremental Value by Channel")

fig, ax = plt.subplots(figsize=(9, 5))

ax.bar(
    baseline["channel"],
    baseline["expected_incremental_value"],
    label="Baseline",
    alpha=0.6
)

ax.bar(
    optimal["channel"],
    optimal["expected_incremental_value"],
    label="Optimized",
    alpha=0.85
)

ax.set_ylabel("Expected Incremental LTV ($)")
ax.set_xlabel("Channel")
ax.legend()

st.pyplot(fig)

# ======================================================
# 6️⃣ Channel-Level Comparison Table
# ======================================================
st.subheader("Channel-Level Comparison")

comparison = baseline.merge(
    optimal,
    on="channel",
    suffixes=("_baseline", "_optimized")
)

comparison["value_lift"] = (
    comparison["expected_incremental_value_optimized"]
    - comparison["expected_incremental_value_baseline"]
)

st.dataframe(
    comparison[[
        "channel",
        "spend_baseline",
        "spend_optimized",
        "expected_incremental_value_baseline",
        "expected_incremental_value_optimized",
        "value_lift"
    ]].sort_values("value_lift", ascending=False),
)

# ======================================================
# 7️⃣ Policy Explanation Layer
# ======================================================
st.subheader("Policy Explanation")

def explain_policy(row):
    if row["spend_optimized"] > row["spend_baseline"] * 1.2:
        return "Spend increased due to strong incremental LTV per dollar and superior retention."
    elif row["spend_optimized"] < row["spend_baseline"] * 0.8:
        return "Spend reduced due to weak incremental value despite surface-level conversions."
    else:
        return "Spend remained stable as incremental value was consistent with baseline performance."

for _, r in comparison.iterrows():
    st.write(f"**{r['channel']}** — {explain_policy(r)}")

# ======================================================
# Footer
# ======================================================
st.caption(
    "Baseline and optimized policies are evaluated under identical "
    "budget and channel-capacity constraints."
)
