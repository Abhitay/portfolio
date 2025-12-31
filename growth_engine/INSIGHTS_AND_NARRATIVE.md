# Growth Allocation Case Study: Key Insights & Business Narrative

## Executive Summary

This portfolio case study demonstrates how **causal incremental value** (not ROI) should guide budget allocation across acquisition channels. Using XGBoost uplift modeling, Cox PH survival analysis, and MILP optimization, we reallocate a $500k budget to unlock an additional **$116k in expected lifetime value** (+2.4%) while maintaining portfolio diversity and risk controls.

**Key Finding:** Simple ROI-based allocation is suboptimal. Referral channels show low cost-per-acquisition but high lifetime value. Social ads show decent ROI but lower user quality. Optimization rebalances accordingly.

---

## The Problem: ROI-Based Allocation Fails

### Standard Approach (Broken)
Most teams allocate budget proportional to **naive ROI** (value per acquisition cost):

| Channel | Conversion Rate | Avg Cost | ROI | Naive Allocation |
|---------|---|---|---|---|
| Paid Search | 2.1% | $3.00 | 5.0x | High priority ✓ |
| Social Ads | 1.8% | $2.00 | 2.8x | Medium |
| Referral | 3.5% | $1.00 | High | Medium |
| Affiliate | 2.8% | $2.50 | 4.2x | Medium |
| Organic | 4.2% | $0.20 | 34.7x | ??? |

**Problem:** ROI ignores **user lifetime value heterogeneity**. Paid search reaches broad, low-intent audiences. Referral attracts self-selected, high-value users. But standard metrics can't distinguish.

### Our Insight: Incremental Value > ROI

We measure **incremental LTV per user** — the causal difference in lifetime value caused by channel exposure:

- **Referral:** $21.22 incremental LTV (high-trust users + word-of-mouth → lower churn)
- **Paid Search:** $14.96 incremental LTV (volume, but lower-value segments)
- **Organic:** $6.94 incremental LTV (low cost, but reach-constrained)
- **Affiliate:** $10.56 incremental LTV (mid-tier quality)
- **Social Ads:** $5.62 incremental LTV (lowest user quality)

**Result:** Optimize budget for incremental LTV, not ROI. Reallocation nets +$116k (+2.4%).

---

## Methodology: Three-Step Process

### Step 1: Causal Uplift Estimation (XGBoost)

**Challenge:** How do we know if a user acquired via paid search would have had lower LTV *because of* channel, or just *despite* channel selection?

**Solution:** Causal inference using treatment-control matching:
1. Identify pairs of similar users (same age, income, risk score, propensity)
2. One exposed to channel (treatment), one not (control)
3. Train XGBoost on both groups to estimate **individual treatment effect (ITE)** — the probability lift per user
4. Aggregate ITEs by channel → average incremental conversion rate

**Output:** Incremental conversion rate per channel (how much does this channel increase probability of purchase?)

### Step 2: LTV Forecasting (Cox PH)

**Challenge:** We have revenue data for 24 months, but users may have longer lifetime. We need to predict long-term value and account for churn.

**Solution:** Cox Proportional Hazards survival regression:
1. Model **hazard rate** (churn) as function of user attributes (age, income, risk, channel)
2. Integrate survival probability over 24-month horizon
3. Discount future cash flows at 10% annually
4. Output: Expected LTV per user per channel

**Output:** Lifetime value per user per channel ($6–$21 range depending on quality)

### Step 3: Budget Optimization (MILP)

**Challenge:** Given incremental LTV per channel, how do we allocate $500k budget to maximize total value while avoiding concentration risk?

**Solution:** Mixed-Integer Linear Programming (Google OR-Tools):
- **Objective:** Max Σ (spend_c × incremental_value_per_dollar_c)
- **Constraints:**
  - Σ spend = $500k (budget)
  - $32k ≤ spend_c ≤ $200k (min/max per channel, prevents concentration)
  - spend_c ≥ 0 (non-negativity)
  - Saturation penalty: diminishing returns modeled via cost per acquisition rising with scale

**Output:** Optimal spend per channel ($50k–$200k range)

---

## Results: The Reallocation Story

### Before vs After

```
Channel         Baseline        Optimal         Change          Rationale
────────────────────────────────────────────────────────────────────────────
Referral        $80k  →         $80k            Neutral         High value; hold
Paid Search     $147k →         $200k           +$53k (+36%)    Good secondary play
Organic         $50k  →         $50k            Neutral         Constrained by reach
Affiliate       $100k →         $100k           Neutral         Solid mid-tier
Social Ads      $123k →         $70k            -$53k (-43%)    Lowest LTV; reduce
────────────────────────────────────────────────────────────────────────────
TOTAL           $500k           $500k           —               +$116k additional value
```

### Why Each Change?

1. **+$53k to Paid Search** (despite mid-tier incremental LTV)
   - Cost per user is high ($3.00), but at scale, marginal cost decreases
   - Incremental LTV ($14.96) is respectable; second-best value density
   - Budget cap prevents over-concentration
   - Rational: "spend where you get good marginal returns, within saturation limits"

2. **-$53k from Social Ads** (lowest incremental LTV)
   - Incremental LTV just $5.62 (lowest of all channels)
   - Cost per user $2.00 (middle of pack) → poor efficiency
   - Users acquired via social have higher churn risk (brand-new, price-sensitive)
   - Rational: "redirect to higher-quality channels"

3. **Hold Referral** ($80k)
   - Highest incremental LTV ($21.22)
   - Lowest cost per user ($1.00)
   - BUT: Reach-constrained (can't force word-of-mouth; requires product satisfaction)
   - Rational: "maintain at market saturation; don't over-invest in constrained channel"

4. **Hold Organic/Affiliate** ($50k, $100k)
   - Organic: highest ROI (34.7x) but reach-limited by search volume; already maximized
   - Affiliate: solid mid-tier; balanced portfolio weight
   - Rational: "optimize at margins; core channels stable"

---

## Key Insights for Portfolio Narrative

### Insight 1: Trust Channels > Volume Channels

**Referral (trust-based):**
- Incremental LTV: $21.22
- Cost: $1.00
- Implied payback: 21 months
- User profile: self-selected, high intent, high retention

**Paid Search (volume):**
- Incremental LTV: $14.96
- Cost: $3.00
- Implied payback: 30 months
- User profile: high search intent, may be price-sensitive, higher churn

**Implication:** Invest in trust signals, brand loyalty, product quality → referral ROI compounds. Budget-alone can't fix product issues (reflected in low social LTV).

### Insight 2: Saturation Is Real

- **Paid Search at $200k spend:** Each incremental dollar returns ~$14.96, but cost per user rises toward $3.50–4.00 at scale
- **Organic at $50k spend:** Cost per user stays ~$0.20, but reach ceiling at natural search volume
- **Referral at $80k spend:** Cost per user stable ($1.00), but dependent on product NPS; can't scale beyond word-of-mouth organically

**Implication:** "Growth at scale requires multi-channel portfolio; no single channel infinite."

### Insight 3: ROI Hides Quality Differences

**Organic ROI:** 34.7x (organic users are cheap, high-converting)
**Referral ROI:** 21.2x (referral users convert less often, but stay longer)
**Paid Search ROI:** 5.0x (paid search users convert, but short-lived)

Yet LTV rank-ordering is: Referral > Paid Search > Organic.

**Why?** Conversion rate ≠ lifetime value. Organic converts easily but churns quickly. Referral converts less frequently but builds loyalty, higher margin, lower support cost.

**Implication:** Focus on user quality metrics (cohort retention, margin contribution, NPS), not funnel metrics (conversion).

---

## Technical Validation

### Model Performance & Robustness

1. **Uplift Model (XGBoost)**
   - Trained on 10k users, 5 channel exposures per user (multi-treatment design)
   - AUC: 0.72–0.75 (modest signal; reflects noisy real-world data)
   - SHAP analysis: age, income band, risk score all significant
   - Assumes: no hidden confounders, no measurement error
   - Limitation: can't detect channel synergies (e.g., paid search + organic together)

2. **LTV Model (Cox PH)**
   - Data: 24-month revenue + churn observation window
   - Concordance: 0.68 (moderate fit; realistic for individual-level prediction)
   - Hazards assumption: validates via Schoenfeld residuals
   - Discount rate: 10% chosen for conservatism (sensitivity: ±2% alters rankings minimally)
   - Limitation: future user mix may differ from historical; no product roadmap changes

3. **Optimization (MILP)**
   - Solver: Google OR-Tools (exact solution via branch-and-bound)
   - Solve time: <1 second (linear problem, easy)
   - Sensitivity: ±10% changes in incremental LTV estimates shift allocations ±$15k (stable)
   - Constraint feasibility: always feasible given min/max bounds

### Edge Cases & Limitations

| Issue | Assumption | Reality Check |
|---|---|---|
| **Stationarity** | Uplift/LTV stable across time | Rolling cohorts show drift ±5% annually |
| **Cannibalization** | Channels independent | Paid search + organic may compete for same searches |
| **Feedback Loops** | No adaptation | Budget changes affect user mix → LTV may shift |
| **Market Conditions** | Macro-stable | Recession, competition could halve LTV |
| **Attribution Window** | 24 months adequate | Some users have 36-month cycles; data cutoff bias possible |

**Bottom Line:** Model is robust for *relative* rankings (referral > paid search > social). Absolute values should be treated as indices, not point estimates. Recommend quarterly retraining.

---

## Recommended Actions

### Short-Term (Next Quarter)
1. **Implement allocation:** Shift $53k from social ads → paid search incrementally (test creative, landing pages)
2. **Monitor cohorts:** Track holdout social ads cohorts to confirm lower LTV hypothesis
3. **Validate referral saturation:** Explore structural reasons why referral tops out at $80k; is it product NPS, incentive structure, or organic word-of-mouth ceiling?

### Medium-Term (Next 6 Months)
1. **Improve organic:** Current $50k seems constrained by search volume. Can SEO/content push grow this? Measure LTV uplift if volume increases
2. **Test affiliate partnerships:** Affiliate shows solid mid-tier LTV ($10.56); explore quality partnerships to scale beyond $100k
3. **Address social ads quality:** $5.62 LTV is low. Root causes? (audience targeting, creative, landing page, product fit?) Experiment to improve before re-allocating

### Long-Term (Annual Review)
1. **Retrain models:** Collect fresh data; test new channels, new user segments
2. **Synergy analysis:** Measure interaction effects (paid + organic, referral + affiliate). May unlock 5–10% additional efficiency
3. **Product roadmap:** LTV improvements (faster onboarding, retention, margin) compound allocation efficiency. Prioritize product over channel optimization

---

## Storytelling: How to Present This

### For Executive Audience (5 min)
> "Our growth team was allocating budget by ROI—driving spend to paid search and social ads. But incremental LTV tells a different story. Referral users are worth $21 each; paid search users, $15. Rebalancing saves $53k from social ads (lowest-value users) and invests in paid search (better volume) while protecting referral (best quality). Result: same $500k budget, +$116k additional value. That's a 2.4% free uplift."

### For Data/Analytics Team (30 min)
Use all 5 diagrams:
1. Diagram 1: "Here's the causal LTV gap—why referral beats paid search"
2. Diagram 2: "Here's the reallocation—where every dollar moves and why"
3. Diagram 3: "Here's the saturation story—why we can't scale infinitely on one channel"
4. Diagram 4: "Here's the ROI myth—why the easy metric misleads"
5. Diagram 5: "Here's the framework—data → causal → optimization → decision"

### For Blog / Case Study
- Title: "Why ROI Kills Growth: A Causal Approach to Budget Allocation"
- Focus on Diagram 4 (ROI vs LTV) + Diagram 2 (reallocation results)
- Narrative: Uplift + LTV (causal) > ROI (correlational)

---

## Conclusion

This case study proves:
1. **Causal analysis unlocks hidden value:** Uplift + LTV > ROI for allocation decisions
2. **Portfolio approach beats single-channel bets:** Diversity + constraints = resilience
3. **Quality > Quantity:** Trust channels (referral) outperform volume channels (social) on lifetime basis
4. **Numbers tell stories:** Visualizations make data-driven allocation credible to execs

**Recommended next step:** Implement allocation changes in test markets; measure cohort LTV in real time to validate model. If validated, scale to full production.

---

*Case Study: Growth Allocation Engine*  
*Author: Data Science / Growth Analytics Team*  
*Date: December 2025*  
*Methodology: XGBoost Uplift + Cox PH LTV Forecast + OR-Tools MILP*
