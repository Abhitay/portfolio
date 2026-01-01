# Engagement Drop Root Cause Analysis and Feature Rollback Decision

## TL;DR

- I evaluated a post-launch engagement decline following a major feed update in a consumer product.
- Initial analysis using aggregate metrics, t-tests, and naive Difference-in-Differences strongly suggested the feature caused the drop.
- Deeper analysis correcting for selection bias and cohort shifts showed the feature impact was real but not the primary driver.
- **Final decision:** Do not rollback the feature. Apply a targeted fix and monitor cohort-normalized engagement.

---

## Product Context

The product is a B2C, feed-based application where user engagement directly impacts retention and long-term revenue. Engagement is closely monitored by leadership and often used as an early warning signal for product regressions.

Shortly after the gradual rollout of a new feed experience, leadership observed a sustained decline in engagement. The timing raised immediate concern that the feature had negatively impacted user behavior. The decision at stake was whether to rollback the feature, pause further rollout, or continue with targeted iteration.

![Daily ESAU trend showing post-launch decline](figures/esau_trend.png)

*Figure 1: Daily Engaged Sessions per Active User (ESAU). Engagement trends downward after feature rollout, triggering executive concern.*

---

## Users & Segmentation

Users are segmented along two primary dimensions:

- **Cohort quality:** high-intent vs low-intent users, based on acquisition channel and early behavior
- **Lifecycle stage:** new users vs returning users

These segments matter because engagement behavior differs materially across them. High-intent and returning users tend to have higher baseline engagement and are more sensitive to subtle product changes. A shift in cohort mix can materially move aggregate metrics even if the product itself has not regressed.

---

## Metric Design

### North Star Metric
**Engaged Sessions per Active User (ESAU)**  
Defined as total daily sessions divided by daily active users.

I chose ESAU because it normalizes for user growth and reflects per-user engagement rather than raw volume.

### Secondary Metrics
- Daily Active Users (DAU)
- Returning user share
- ESAU split by cohort quality

### Guardrails
- Stability of DAU
- Engagement trends among core (high-intent, returning) users

Optimizing the wrong metric, such as total sessions, would have masked engagement decay driven by low-quality user growth and led to incorrect product decisions.

---

## Data Snapshot

The analysis uses four primary datasets:

- `users.csv`: user attributes and cohort assignment  
- `events.csv`: session-level engagement events  
- `features.csv`: feature rollout timing and exposure  
- `calendar_effects.csv`: seasonality indicators  

### Users (sample)

| user_id | signup_date | country | cohort_quality | acquisition_channel |
|--------:|------------|---------|----------------|---------------------|
| 1 | 2025-10-22 | US | high | referral |
| 2 | 2025-09-15 | US | high | referral |
| 3 | 2025-11-11 | US | low | paid |
| 4 | 2025-10-31 | US | low | affiliate |
| 5 | 2025-09-21 | US | high | organic |

### Events (sample)

| user_id | event_time | event_name | feature_exposed | is_returning | post |
|--------:|-----------|------------|-----------------|--------------|------|
| 1 | 2025-10-22 18:11 | session_start | 0 | false | 0 |
| 1 | 2025-10-27 22:08 | session_start | 1 | false | 1 |
| 2 | 2025-09-18 14:32 | session_start | 0 | true | 0 |

Early inspection already surfaced two warning signs:
- Feature exposure was correlated with baseline engagement
- Aggregate session counts continued to grow while ESAU declined

---

## The Standard Analysis (What Most Teams Would Do)

I started with the standard playbook most teams would follow:

1. Compare ESAU before vs after feature launch
2. Run t-tests on pre/post periods and exposed vs non-exposed users
3. Apply Difference-in-Differences using feature exposure as treatment

The results looked compelling. ESAU dropped from **1.79 to 1.76**, a **~1.45% decline**, immediately after launch.

![Pre vs post ESAU comparison](figures/pre_post_esau.png)

*Figure 2: Average ESAU before and after feature rollout. The post-launch drop makes a rollback appear justified.*

Plotting ESAU trends for treated and control users further reinforced this conclusion.

![Naive treated vs control ESAU trends](figures/naive_treated_control_trend.png)

*Figure 3: Naive treated vs control comparison suggests a feature-driven divergence after rollout.*

The conclusion seemed obvious: the feature hurt engagement.

---

## Why That Analysis Was Misleading

The flaw was not in the math, but in the assumptions.

Feature exposure was **endogenous**. Higher-engagement users were more likely to be exposed, and cohort composition shifted materially during the post period. At the same time, the post-launch window included seasonality and natural engagement decay.

In plain terms, the analysis compared groups that were never comparable and attributed all change to the most visible event. Statistical significance masked a fundamentally biased comparison.

---

## My Approach (Correct Methodology)

I reframed the problem around a simpler question:

*What would engagement have looked like for exposed users if they had not been exposed?*

To approximate that counterfactual, I:

- Built pre-treatment user features using only behavior before rollout
- Estimated propensity scores for feature exposure
- Matched treated and control users to correct selection bias
- Re-evaluated engagement on the matched population
- Aggregated outcomes over the full post window to avoid unstable daily ratios

Before matching, I validated that sufficient overlap existed between treated and control users.

![Propensity score overlap](figures/propensity_overlap.png)

*Figure 4: Density-based propensity score overlap shows treated users have comparable controls after adjusting for baseline behavior.*

---

## Results (Corrected View)

From leadership’s perspective, the headline metric showed a **~1.45% daily ESAU decline**.

After correcting for selection bias:
- Treated users accumulated **~14.8% fewer sessions** than matched controls over the entire post period
- The interaction effect was real, but not large enough to explain the aggregate daily decline

The corrected view showed the feature contributed to the drop, but was not the dominant driver.

---

## Segment-Level Insights

Breaking results down by segment revealed meaningful heterogeneity:

- **Low-intent cohorts:** engagement decline driven primarily by acquisition mix changes
- **High-intent, returning users:** small but consistent interaction effect from the new feed
- **New users:** minimal sensitivity to the feature

The risk was localized friction among core users, not broad engagement collapse.

---

## Key Findings & Inference

1. Aggregate engagement declines can be driven by cohort shifts rather than product regressions.
2. Feature exposure was non-random, invalidating naive causal comparisons.
3. Correcting for selection bias materially reduced the estimated feature impact.
4. The feature interaction effect was real but economically modest.
5. Rolling back the feature would not have recovered the observed engagement loss.

---

## What Would Have Gone Wrong Without This Analysis

Without correcting for bias, the team would likely have rolled back the feature. That decision would have:
- Failed to restore engagement
- Wasted engineering effort
- Disrupted the product roadmap
- Reinforced distrust in experimentation results

Meanwhile, the real drivers—seasonality and cohort quality—would have remained unaddressed.

---

## Recommendation & Next Steps

**Final decision:** Do not rollback the feature.

**Reasoning:**
- ~0.5% of the decline driven by seasonality
- ~0.8% driven by cohort quality shift
- ~0.15% attributable to a feature interaction bug

**Next steps:**
- Patch the returning-user interaction issue
- Monitor cohort-normalized ESAU weekly
- Re-evaluate after two weeks before considering broader changes

---

## Key Takeaway

Strong product data science is not about finding statistically significant effects, but about preventing confident decisions based on the wrong comparison.
