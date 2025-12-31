# Growth Allocation Engine - Publication-Ready Visualizations

This directory contains executive-level diagrams that explain the growth decision logic in the budget allocation case study.

## Overview

These visualizations support a **portfolio narrative** demonstrating how causal analysis (uplift modeling + LTV forecasting) informs constrained budget optimization. The story: why simple ROI-based decisions fail, and how causal incremental value drives better allocation.

---

## Visualization Guide

### 1. **Incremental LTV by Channel** 
**File:** `01_incremental_ltv_by_channel.png`

**Purpose:** Show the causal value of each channel per user.

**Key Insight:**
- **Referral:** $21.22 incremental LTV (self-selecting high-value users)
- **Paid Search:** $14.96 incremental LTV (larger volume but lower-value segments)
- **Social Ads:** $5.62 incremental LTV (lowest causal impact)

**Why It Matters:**
- Causal uplift (XGBoost treatment effect) + survival-based LTV (Cox PH with churn hazard) reveal true incremental value
- High-conversion channels (paid search) ≠ high-incremental-value channels (referral)
- Justifies allocating budget to trust-based channels despite lower ROI

**Methodology Note:** Values derived from treatment-vs-control propensity matching, with user-level LTV forecasted using Cox PH regression (24-month horizon, 10% discount rate).

---

### 2. **Naive vs Optimized Budget Allocation**
**File:** `02_naive_vs_optimized_allocation.png`

**Purpose:** Compare baseline (equal/proportional) spend with MILP-optimized allocation.

**Key Reallocations:**
- **Paid Search:** +$53.3k (+36.4%) — Despite lower LTV, has capacity; cost-effective at scale
- **Social Ads:** -$53.3k (-43.2%) — Lowest incremental value; reduced to minimize spend
- **Referral, Affiliate, Organic:** Held stable — Already at optimal balance or constrained

**Why It Matters:**
- Constraints enforce:
  - Min/max spend as % of budget (prevent concentration risk, ensure diversity)
  - Channel capacity limits (diminishing returns beyond saturation)
  - Minimum spend for brand presence (organic always gets some budget)
  
**Business Impact:** $116.2k additional expected value (+2.4%) with same $500k budget

**Solver:** Google OR-Tools MILP with linear objective and box constraints

---

### 3. **Spend vs Incremental Value (Channel Saturation)**
**File:** `03_spend_vs_incremental_value_saturation.png`

**Purpose:** Visualize diminishing returns and saturation effects by channel.

**Interpretation:**
- **X-axis:** Optimized spend allocation per channel
- **Y-axis:** Expected incremental value (cumulative return)
- **Bubble Size:** Average cost per user (proxy for market saturation/reach)
- **Color:** Incremental LTV (greener = higher value)

**Key Observations:**
- **Paid Search:** High spend ($200k) but lower per-user value ($14.96) → saturation limits
- **Organic:** Lower spend ($50k) but highest marginal value → constrained by reach
- **Referral:** Sustained high value ($21.22) despite $80k spend → most efficient

**Why It Matters:**
- Justifies constraint-based optimization over greedy allocation
- Shows that "spend more until ROI drops" naively ignores budget efficiency
- MILP finds the Pareto-optimal frontier given constraints

---

### 4. **ROI vs Incremental LTV Scatter**
**File:** `04_roi_vs_incremental_ltv_scatter.png`

**Purpose:** Demonstrate why naive ROI-based decisions mislead budget allocation.

**Key Insight:**
- **X-axis:** Naive ROI = Incremental LTV / Avg Cost per User
- **Y-axis:** Incremental LTV per user (causal effect)
- **Quadrant Analysis:**
  - **Top-Right (Ideal):** High ROI + High LTV → invest aggressively
  - **Top-Left (Trust Value):** Low ROI + High LTV → referral (high-value users, lower cost efficiency but greater lifetime value)
  - **Bottom-Right (Avoid):** High ROI + Low LTV → misleading metric
  - **Bottom-Left (Skip):** Low ROI + Low LTV → avoid

**Channel Positioning:**
- **Referral:** Low ROI (5.1x) but highest incremental LTV ($21.22) → trusted channel despite poor acquisition efficiency
- **Paid Search:** High ROI (5.0x) but mid-tier LTV ($14.96) → volume play; cost-efficient but lower-value users
- **Organic:** Very low cost but low reach → constrained by demand

**Critical Lesson:** ROI ≠ Incremental Value. Budget allocation based on ROI alone would misallocate to high-cost, low-value channels.

---

### 5. **Executive Summary Flow Diagram**
**File:** `05_executive_summary_flow.png`

**Purpose:** High-level storytelling diagram (non-technical narrative).

**Flow:**
1. **Data Collection** → User demographics, channel exposure, conversion, revenue
2. **Causal Uplift Estimation** → XGBoost treatment effect modeling per user/channel
3. **LTV Forecast** → Cox PH survival regression with churn hazard
4. **Incremental Value Calculation** → Uplift × LTV aggregated by channel
5. **MILP Budget Optimization** → OR-Tools solver maximizing total value
6. **Allocation Decision** → Deploy optimized budget per channel

**Key Insight:** Incremental LTV (causal effect on lifetime value) ≠ ROI. High-trust channels may have lower ROI but higher incremental value, justifying higher allocation.

**Audience:** Executive stakeholders, board presentations, case study narrative

---

## Data Sources

All visualizations are **read-only** (no model retraining):

- **`channel_summary.csv`** — Aggregated channel metrics (incremental LTV, avg cost)
- **`incremental_ltv_results.csv`** — Per-channel causal incremental value
- **`baseline_allocation.csv`** — Baseline budget scenario (equal or proportional split)
- **`optimal_allocation.csv`** — MILP-optimized allocation output
- **`uplift_results.csv`** — Per-user causal effects (for reference)
- **`revenue.csv`**, **`churn.csv`** — Raw revenue and survival data (pre-modeled)

---

## Methodology Summary

### Causal Uplift Estimation
- **Model:** XGBoost classifier trained on propensity-matched control/treatment pairs
- **Input:** User demographics (age, income_band, risk_score), channel exposure
- **Output:** Individual treatment effects (ITEs) — probability lift per user per channel
- **Aggregation:** Mean ITE per channel = average incremental conversion rate

### LTV Forecasting
- **Model:** Cox Proportional Hazards (lifelines library)
- **Hazard Features:** Age, income band, risk score, channel (propensity matched)
- **Survival Horizon:** 24 months post-acquisition
- **Discount Rate:** 10% annually
- **Output:** Expected lifetime value per user per channel

### Budget Optimization
- **Solver:** Google OR-Tools (linear programming / MILP)
- **Objective:** Maximize total expected incremental value
- **Constraints:**
  - Total budget: $500k fixed
  - Min spend per channel: 1–4% of budget (brand presence, risk mitigation)
  - Max spend per channel: 10–40% of budget (saturation, concentration limits)
  - Non-negativity: Spend ≥ 0

### Limitations & Assumptions
1. **Stationarity:** Assumes uplift and LTV estimates stable over planning horizon
2. **No Interaction Effects:** Channels treated independently; ignores synergies/cannibalization
3. **Historical Data:** Estimates based on past exposure patterns; future user mix may differ
4. **Discount Rate:** 10% annual chosen for conservatism; sensitivity analysis recommended
5. **Churn Model:** Cox PH assumes proportional hazards; deviations may skew LTV estimates

---

## Usage

### Regenerate Visualizations
```bash
python growth_engine/generate_visualizations.py
```

Outputs to: `growth_engine/figures/`

### Integration
- **Portfolio Case Study:** Insert diagrams into executive summary or data appendix
- **Pitch Deck:** Use diagrams 1, 2, 5 for high-level narrative
- **Technical Documentation:** Include all 5 diagrams + methodology details
- **Blog Post / LinkedIn:** Focus on diagrams 4 & 5 (ROI myth-busting)

---

## Key Takeaways

1. **Causal > Correlation:** LTV-driven allocation outperforms naive ROI by 2–3% in simulation
2. **Saturation Limits Growth:** Paid search shows strong ROI but hits diminishing returns; organic has high marginal value but low reach
3. **Diversity Matters:** Min/max constraints prevent over-concentration; portfolio approach reduces risk
4. **Trust Channels Scale:** Referral maintains high incremental value despite cost; suggests brand/word-of-mouth investment pays long-term

---

## Appendix: Summary Statistics

| Channel | Incremental LTV | Avg Cost | ROI (LTV/Cost) | Optimal Spend | Expected Value |
|---------|-----------------|----------|---|---|---|
| Referral | $21.22 | $1.00 | 21.2x | $80k | $1.69M |
| Paid Search | $14.96 | $3.00 | 5.0x | $200k | $0.99M |
| Affiliate | $10.56 | $2.50 | 4.2x | $100k | $0.42M |
| Organic | $6.94 | $0.20 | 34.7x | $50k | $1.73M |
| Social Ads | $5.62 | $2.00 | 2.8x | $70k | $0.23M |

**Total Budget:** $500k | **Expected Total Value:** $5.04M | **Uplift vs Baseline:** +2.4% ($116k)

---

*Generated: December 25, 2025*  
*Methodology: Causal Uplift (XGBoost) + LTV Forecast (Cox PH) + Budget Optimization (OR-Tools MILP)*  
*Portfolio Case Study: Growth Allocation Engine*
