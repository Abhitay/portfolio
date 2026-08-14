# When Engagement Lifts Mislead: Did the New Feed Improve Retention?

Why the initial engagement signal mattered, and how causal correction changed the decision.

## TL;DR

A new feed iteration appeared to drive a ~110–140% lift in engagement, but after correcting for selection bias with propensity score matching, 7-day retention showed no meaningful improvement: the lift came from who received the feature, not the feature itself. Final decision: do not ship.

## Contents

- Introduction

- What We Compared

- Why Metrics Mislead

- Data

- The Naive Comparison

- Why It Failed

- Method

- Results

- Recommendation

## Introduction

This case study evaluates a feed-ranking change in a generic consumer social app. The feed is a core surface for engagement and long-term retention, making even small ranking changes high-risk.

The feature introduced more aggressive personalization based on predicted relevance. Exposure was not randomized, making this an observational analysis rather than a clean A/B test.

## What We Compared

Users clustered naturally into three behavioral segments.

#### Low-engagement users

Infrequent usage, low baseline interaction

#### Normal users

Moderate engagement, majority of the base

#### Power users

Highly engaged, critical to platform health

These segments matter because engagement propensity differs sharply across them.

![User Segment Distribution](figures/feature_impact_user_segment_distribution.png)

## Why Metrics Mislead

Engagement spikes are diagnostic, not decisive. Success criteria were defined upfront.

### 7-day retention

Best proxy for habit formation and long-term value.

- Cards viewed per session

- Bounce rate

Useful for understanding behavior, not for making ship decisions.

The decision hinged on whether users returned, not whether they interacted more in a single session.

## Data

The analysis relied on two complementary datasets that together made it possible to separate user quality from feature impact.

One row per user. Used to model selection bias and long-term outcomes.

- User segment (low / normal / power)

- Baseline engagement score (pre-exposure)

- Feature exposure flag

- 7-day retention outcome

Session-level behavioral data. Used to measure short-term engagement.

- Session start / end events

- Card view events per session

- Feature flag at time of interaction

#### Unit of analysis

Users for retention analysis; sessions for engagement diagnostics.

#### Time window

Baseline behavior measured pre-exposure, outcomes tracked over 7 days post-exposure.

#### Why this matters

Separating baseline behavior from outcomes makes causal adjustment possible.

Users exposed to the new feature had systematically higher baseline engagement, indicating strong selection bias in feature exposure.

This meant naive engagement comparisons primarily reflected who received the feature, not what the feature caused.

## The Naive Comparison

A dashboard view suggested a dramatic engagement win.

#### Average cards viewed per session

At face value, this appears to be a major engagement win. A standard dashboard would strongly suggest shipping.

![Naive Engagement Comparison](figures/feature_impact_naive_engagement_comparison.png)

Takeaway: the lift conflates user quality with feature impact.

## Why It Failed

Exposure to the new feed was non-random and strongly correlated with baseline engagement.

The comparison measured high-engagement users vs low-engagement users, not the causal effect of the feature.

Analogy: comparing basketball players to accountants and concluding basketball makes people taller.

## Method

I applied propensity score matching to approximate a randomized experiment.

#### Non-random treatment

Assignment depended on behavior.

#### Observable confounders

Segment and baseline engagement.

#### RCT approximation

Matched treated and control users.

## Results

Matching shifted the comparison onto like-for-like users.

#### 7-day retention after adjustment

Once comparable users are evaluated, the apparent engagement win disappears. The feature does not improve retention.

![7-Day Retention After Propensity Score Matching](figures/feature_impact_psm_retention_comparison.png)

Retention remains unchanged after causal adjustment.

## Recommendation
