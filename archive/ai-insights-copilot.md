# Was the Feed Update the Culprit? Root Cause Analysis & Targeted Fix

Deciding whether to rollback a major feed update or apply a focused fix that preserves long-term value.

## TL;DR

An investigation of a post-launch engagement decline after a major feed update in a consumer product. Initial analysis with aggregate metrics, t-tests, and a naive Difference-in-Differences strongly suggested the feature caused the drop, but deeper analysis correcting for selection bias and cohort shifts showed the feature's impact was real yet not the primary driver. Final decision: do not roll back the feature, apply a targeted fix and monitor cohort-normalized engagement.

## Contents

- Introduction

- What We Compared

- Why ESAU Misleads

- Data

- Standard Analysis

- Why It Was Risky

- Agentic Investigation

- Counterfactual Approach

- Results

- Segment Insights

- Key Findings

## Introduction

The product is a B2C, feed-based application where user engagement directly impacts retention and long-term revenue. Engagement is closely monitored by leadership and often used as an early warning signal for product regressions.

Shortly after the gradual rollout of a new feed experience, leadership observed a sustained decline in engagement. The timing raised immediate concern that the feature had negatively impacted user behavior. The decision at stake was whether to rollback the feature, pause further rollout, or continue with targeted iteration.

![Daily ESAU trend showing post-launch decline](figures/esau_trend.png)

Figure 1: Daily Engaged Sessions per Active User (ESAU). Engagement trends downward after feature rollout, triggering executive concern.

## What We Compared

The engagement drop did not affect all users equally. Understanding who moved the metric was the first priority.

#### High-intent users

Returning users with strong baseline engagement and repeat usage.

Small in number, disproportionate impact on ESAU.

#### Low-intent users

Newly acquired or low-commitment users with volatile engagement.

High volume, unstable behavior.

#### Lifecycle stage

New vs returning users exhibit fundamentally different engagement dynamics.

Aggregates mask these differences.

A shift in cohort mix alone can move ESAU materially, even if the product experience is unchanged. Any analysis that ignores this risks blaming the wrong cause.

## Why ESAU Misleads

ESAU is a useful signal, but only when the population underneath it is stable.

#### Why ESAU is attractive

- Normalizes for DAU growth

- Captures per-user engagement intensity

- Moves quickly after product changes

Implicit assumption: the user mix is comparable over time.

#### Where it breaks

- Influx of low-intent users dilutes averages

- Returning users churn more slowly but move the metric more

- Lifecycle effects masquerade as product regressions

The metric reacts, but not always to the right cause.

#### How ESAU should be used

As a diagnostic signal, not a decision trigger.

- Segmented by cohort quality

- Anchored to returning users

- Interpreted alongside acquisition mix

ESAU was telling the truth: just not the truth leadership thought it was.

## Data

To determine whether the feed update caused the drop, the analysis required visibility into baseline quality, feature exposure, and post-launch behavior.

#### User-level context

User records capture who users were before the rollout.

- Signup timing and acquisition channel

- Cohort quality classification

- Returning vs new user status

This answers: what kind of users are we observing?

#### Behavioral outcomes

Event-level data tracks actual engagement over time.

- Session starts and counts

- Feature exposure flags

- Pre vs post indicators

This answers: how behavior changed after exposure.

Feature exposure was correlated with baseline engagement, and total sessions continued to grow even as ESAU declined, a classic signal of cohort-driven metric movement.

Because baseline quality and post-launch behavior were observable separately, the analysis could isolate product impact from population drift.

## Standard Analysis

The initial evidence appeared to point clearly toward a rollback.

Following the conventional analytics playbook, the analysis began with aggregate comparisons that most teams rely on under time pressure.

#### Step 1: Pre / post comparison

ESAU was compared before and after the feed rollout across the full user base.

Fast, intuitive, and commonly used in production monitoring.

#### Step 2: Treated vs control trends

Users exposed to the new feed were compared against non-exposed users over the same time window.

Assumes exposure is exogenous.

#### Step 3: Difference-in-Differences

A DiD model estimated the interaction between feature exposure and the post-launch period.

Statistically rigorous, if assumptions hold.

All three views told the same story.

![Pre vs post ESAU](figures/pre_post_esau.png)

ESAU declined immediately following rollout, suggesting a negative feature impact.

![Naive treated vs control trend](figures/naive_treated_control_trend.png)

Exposed users diverged downward relative to controls, reinforcing the rollback narrative.

The feed update caused the engagement drop. Rolling back would restore performance.

## Why It Was Risky

The naive analysis compared incomparable groups and attributed all change to the most visible event.

The flaw was not in the math, but in the assumptions.

Feature exposure was endogenous. Higher-engagement users were more likely to be exposed, and cohort composition shifted materially during the post period. At the same time, the post-launch window included seasonality and natural engagement decay.

In plain terms, statistical significance masked a fundamentally biased comparison.

## Agentic Investigation

Before applying deeper causal methods, the challenge was not computation, but deciding what to test and in what order under time pressure.

To avoid anchoring on the most visible explanation (the feature), I designed an agentic investigation framework that systematically evaluated competing hypotheses behind the engagement decline.

#### Hypothesis generation

- Feature regression from the new feed

- Seasonality and calendar effects

- User quality and acquisition mix shift

- Instrumentation or logging issues

Prevents premature fixation on a single narrative.

#### Agent-driven test planning

The agent ranked hypotheses by plausibility, expected impact, and cost of validation, then selected appropriate analytical tests.

- Cohort stability checks

- Pre/post balance diagnostics

- Segment-level trend analysis

- Causal estimation where warranted

#### Evidence synthesis

Results from each test were summarized and evaluated jointly rather than in isolation.

Avoids overreacting to statistically significant but economically misleading signals.

The agentic layer ensured the analysis remained hypothesis-driven rather than metric-driven, narrowing the root cause before applying Difference-in-Differences and matching.

## Counterfactual Approach

The critical question was not whether engagement changed, but what would have happened without the feed update.

Because exposure to the feature was non-random, the counterfactual could not be observed directly. The analysis therefore focused on constructing a defensible approximation using only pre-rollout information.

#### Freeze pre-treatment behavior

User features were engineered exclusively from behavior observed before the rollout.

Prevents post-treatment leakage.

#### Model exposure propensity

A propensity model estimated each user’s likelihood of receiving the new feed based on baseline engagement and lifecycle stage.

Makes selection bias explicit.

#### Match comparable users

Treated users were matched to control users with similar propensity scores.

Approximates a randomized experiment.

Engagement outcomes were then compared over the full post period, avoiding unstable daily ratios that exaggerate noise.

Matching is only valid if treated and control users overlap.

![Propensity score overlap](figures/propensity_overlap.png)

Propensity score distributions show sufficient overlap after trimming, validating the matching approach.

By comparing users who looked similar before exposure, the analysis isolated the feature’s interaction effect from cohort shifts and seasonality.

## Results

Once selection effects and cohort shifts were accounted for, the story changed.

The naive view suggested a clear regression: ESAU dropped immediately after rollout.

It attributed all movement to the feature, ignoring who entered and exited the metric.

#### Naive interpretation

- ~1.45% ESAU decline post-launch

- Statistically significant pre/post difference

- Treated users trend downward

Comparison contaminated by selection bias.

#### Bias-corrected view

- ~14.8% fewer sessions for treated users vs matched controls

- Effect real, but economically modest

- Insufficient to explain aggregate decline

Comparison now reflects like-for-like users.

The feature contributed marginally to the drop, but rolling it back would not have recovered engagement. The dominant drivers were cohort quality and seasonality.

## Segment Insights

Breaking results down by segment revealed meaningful heterogeneity:

- Low-intent cohorts: engagement decline driven primarily by acquisition mix changes

- High-intent, returning users: small but consistent interaction effect from the new feed

- New users: minimal sensitivity to the feature

The risk was localized friction among core users, not broad engagement collapse.

## Key Findings

Correcting for bias materially changed both the interpretation and the decision.

#### Aggregate metrics overstated feature impact

The observed ESAU decline was largely driven by cohort mix shifts and seasonality rather than a broad product regression.

#### Feature exposure was non-random

Higher-engagement and returning users were more likely to receive the new feed, invalidating naive treated–control comparisons.

#### The causal effect existed but was modest

After matching, the feed update showed a real interaction effect, but one too small to explain the full engagement drop.

#### Impact was concentrated in core users

The negative interaction primarily affected high-intent, returning users, while new and low-intent users showed minimal sensitivity.

Rolling back the feature would not have restored engagement. The majority of the decline was structural rather than causal, with the feature contributing a secondary, localized effect.
