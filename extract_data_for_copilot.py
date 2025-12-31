"""
Extract key data and metrics from the product_sense project for the ai-insights-copilot.html case study.
This script computes metrics from the CSVs without requiring Jupyter notebook execution.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'

# Read data
users = pd.read_csv('product_sense/data_design/users.csv', parse_dates=['signup_date'])
events = pd.read_csv('product_sense/data_design/events.csv', parse_dates=['event_time', 'first_seen'])
features = pd.read_csv('product_sense/data_design/features.csv', parse_dates=['launch_date'])
calendar = pd.read_csv('product_sense/data_design/calendar_effects.csv', parse_dates=['date'])

print("Data loaded successfully")
print(f"Users: {len(users)}")
print(f"Events: {len(events)}")
print(f"Features: {len(features)}")

# Extract key information from features
feature_launch = features.loc[0, 'launch_date']
feature_name = features.loc[0, 'feature_name']
print(f"Feature: {feature_name}, Launch date: {feature_launch}")

# === KEY METRICS ===

# 1. Overall engagement drop
events['date'] = events['event_time'].dt.date
events['date_dt'] = pd.to_datetime(events['date'])

# Pre and post feature launch
pre_launch = events[events['event_time'] < feature_launch]
post_launch = events[events['event_time'] >= feature_launch]

# Compute ESAU (Engaged Sessions per Active User)
def compute_esau(df):
    """Compute average ESAU across all days"""
    daily_sessions = df.groupby('date').size()
    daily_active_users = df.groupby('date')['user_id'].nunique()
    return (daily_sessions / daily_active_users).mean()

esau_pre = compute_esau(pre_launch)
esau_post = compute_esau(post_launch)
esau_drop_pct = ((esau_post - esau_pre) / esau_pre) * 100

print(f"\nEngagement Drop Analysis:")
print(f"ESAU Pre-launch: {esau_pre:.4f}")
print(f"ESAU Post-launch: {esau_post:.4f}")
print(f"Drop: {esau_drop_pct:.1f}%")

# 2. Exposed vs Non-exposed
esau_exposed = compute_esau(events[events['feature_exposed'] == 1])
esau_not_exposed = compute_esau(events[events['feature_exposed'] == 0])

print(f"\nFeature Exposure Analysis:")
print(f"ESAU Exposed: {esau_exposed:.4f}")
print(f"ESAU Not Exposed: {esau_not_exposed:.4f}")
print(f"Difference: {((esau_exposed - esau_not_exposed) / esau_not_exposed) * 100:.1f}%")

# 3. Naive t-test comparison
from scipy.stats import ttest_ind

def daily_esau(df):
    """Return daily ESAU values"""
    daily_sessions = df.groupby('date').size()
    daily_active_users = df.groupby('date')['user_id'].nunique()
    return (daily_sessions / daily_active_users)

esau_daily_pre = daily_esau(pre_launch)
esau_daily_post = daily_esau(post_launch)

t_stat, p_value = ttest_ind(esau_daily_pre, esau_daily_post, equal_var=False)
print(f"\nNaive T-Test (Pre vs Post):")
print(f"T-statistic: {t_stat:.4f}, P-value: {p_value:.4f}")

# 4. Cohort analysis
users_with_cohort = users.merge(
    events[['user_id', 'feature_exposed']].drop_duplicates(),
    on='user_id'
)

print(f"\nCohort Quality Analysis:")
cohort_dist_pre = users[users['signup_date'] < feature_launch]['cohort_quality'].value_counts(normalize=True)
cohort_dist_post = users[users['signup_date'] >= feature_launch]['cohort_quality'].value_counts(normalize=True)

print(f"Pre-launch high-quality cohort: {cohort_dist_pre.get('high', 0):.1%}")
print(f"Post-launch high-quality cohort: {cohort_dist_post.get('high', 0):.1%}")

# 5. Calendar effects impact
calendar['date_dt'] = pd.to_datetime(calendar['date'])
events_with_calendar = events.merge(calendar, on=['date_dt', 'date'], how='left')
events_with_calendar['engagement_multiplier'] = events_with_calendar['engagement_multiplier'].fillna(1.0)

holiday_events = events_with_calendar[events_with_calendar['is_holiday'] == True]
non_holiday_events = events_with_calendar[events_with_calendar['is_holiday'] == False]

esau_holiday = compute_esau(holiday_events) if len(holiday_events) > 0 else 0
esau_non_holiday = compute_esau(non_holiday_events) if len(non_holiday_events) > 0 else esau_pre

holiday_impact = ((esau_non_holiday - esau_holiday) / esau_non_holiday) * 100 if esau_non_holiday > 0 else 0
print(f"\nSeasonal/Holiday Analysis:")
print(f"ESAU on non-holidays: {esau_non_holiday:.4f}")
print(f"ESAU on holidays: {esau_holiday:.4f}")
print(f"Holiday impact: ~{holiday_impact:.1f}%")

# 6. DiD Analysis
events['post'] = (events['event_time'] >= feature_launch).astype(int)
events['treated'] = events['feature_exposed']

daily_group_metrics = (
    events
    .groupby(['date', 'treated', 'post'])
    .agg(
        sessions=('user_id', 'count'),
        active_users=('user_id', 'nunique')
    )
    .reset_index()
)
daily_group_metrics['esau'] = daily_group_metrics['sessions'] / daily_group_metrics['active_users']

pre_treated = daily_group_metrics.query('treated == 1 and post == 0')['esau'].mean()
post_treated = daily_group_metrics.query('treated == 1 and post == 1')['esau'].mean()
pre_control = daily_group_metrics.query('treated == 0 and post == 0')['esau'].mean()
post_control = daily_group_metrics.query('treated == 0 and post == 1')['esau'].mean()

did_estimate = (post_treated - pre_treated) - (post_control - pre_control)

print(f"\nDifference-in-Differences Analysis:")
print(f"Treated (Exposed) Pre: {pre_treated:.4f}, Post: {post_treated:.4f}")
print(f"Control (Not Exposed) Pre: {pre_control:.4f}, Post: {post_control:.4f}")
print(f"DiD Estimate: {did_estimate:.4f}")
print(f"DiD % Change: {(did_estimate / pre_treated) * 100:.1f}%")

# === VISUALIZATIONS ===

os.makedirs('docs/assets', exist_ok=True)

# Plot 1: Daily Sessions and ESAU Over Time
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Daily Sessions
daily_sessions = events.groupby('date_dt').size()
ax1.plot(daily_sessions.index, daily_sessions.values, linewidth=2, color='#2563eb', marker='o', markersize=4)
ax1.axvline(pd.to_datetime(feature_launch), color='red', linestyle='--', linewidth=2, label=f'{feature_name} Launch')
ax1.set_ylabel('Daily Sessions', fontsize=12, fontweight='bold')
ax1.set_title('Daily Sessions Over Time (Executive View)', fontsize=14, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Daily ESAU
daily_esau_vals = daily_esau(events)
ax2.plot(daily_esau_vals.index, daily_esau_vals.values, linewidth=2, color='#10b981', marker='s', markersize=4)
ax2.axvline(pd.to_datetime(feature_launch), color='red', linestyle='--', linewidth=2, label=f'{feature_name} Launch')
ax2.set_ylabel('ESAU (Sessions/User)', fontsize=12, fontweight='bold')
ax2.set_xlabel('Date', fontsize=12, fontweight='bold')
ax2.set_title('Engaged Sessions per Active User (Executive View)', fontsize=14, fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('docs/assets/daily_sessions_esau.png', dpi=150, bbox_inches='tight')
print("✓ Saved: docs/assets/daily_sessions_esau.png")
plt.close()

# Plot 2: Feature Exposure Impact (Naive)
fig, ax = plt.subplots(figsize=(10, 6))
categories = ['Exposed to Feature', 'Not Exposed']
esau_values = [esau_exposed, esau_not_exposed]
colors = ['#ef4444', '#6b7280']

bars = ax.bar(categories, esau_values, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5, width=0.6)

for bar, val in zip(bars, esau_values):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{val:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=12)

ax.set_ylabel('ESAU (Sessions/User)', fontsize=12, fontweight='bold')
ax.set_title('Feature Exposure Impact (Naive Comparison)\nWithout Causal Correction', fontsize=14, fontweight='bold')
ax.set_ylim(0, max(esau_values) * 1.2)
ax.grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('docs/assets/naive_feature_impact.png', dpi=150, bbox_inches='tight')
print("✓ Saved: docs/assets/naive_feature_impact.png")
plt.close()

# Plot 3: Pre vs Post Period Comparison
fig, ax = plt.subplots(figsize=(10, 6))
periods = ['Pre-Launch', 'Post-Launch']
esau_periods = [esau_pre, esau_post]
colors_period = ['#10b981', '#ef4444']

bars = ax.bar(periods, esau_periods, color=colors_period, alpha=0.7, edgecolor='black', linewidth=1.5, width=0.6)

for bar, val in zip(bars, esau_periods):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{val:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=12)

# Add drop annotation
drop_text = f'{esau_drop_pct:.1f}% Drop'
ax.text(0.5, max(esau_periods) * 0.5, drop_text, ha='center', va='center', 
        fontsize=16, fontweight='bold', color='red', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

ax.set_ylabel('ESAU (Sessions/User)', fontsize=12, fontweight='bold')
ax.set_title('The Engagement Drop: Before vs After Feature Launch', fontsize=14, fontweight='bold')
ax.set_ylim(0, max(esau_periods) * 1.3)
ax.grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('docs/assets/esau_drop.png', dpi=150, bbox_inches='tight')
print("✓ Saved: docs/assets/esau_drop.png")
plt.close()

# Plot 4: DiD Visualization
fig, ax = plt.subplots(figsize=(10, 6))

# Pre-post periods
periods_did = ['Pre-Launch', 'Post-Launch']
treated_esau = [pre_treated, post_treated]
control_esau = [pre_control, post_control]

x = np.arange(len(periods_did))
width = 0.35

bars1 = ax.bar(x - width/2, treated_esau, width, label='Exposed to Feature', color='#f59e0b', alpha=0.8, edgecolor='black')
bars2 = ax.bar(x + width/2, control_esau, width, label='Not Exposed', color='#6b7280', alpha=0.8, edgecolor='black')

ax.set_ylabel('ESAU (Sessions/User)', fontsize=12, fontweight='bold')
ax.set_title('Difference-in-Differences: Treated vs Control Groups', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(periods_did)
ax.legend(fontsize=11)
ax.grid(True, axis='y', alpha=0.3)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('docs/assets/did_analysis.png', dpi=150, bbox_inches='tight')
print("✓ Saved: docs/assets/did_analysis.png")
plt.close()

# Plot 5: Cohort Quality Shift
fig, ax = plt.subplots(figsize=(10, 6))

cohort_types = ['High Quality', 'Low Quality']
pre_pct = [cohort_dist_pre.get('high', 0) * 100, cohort_dist_pre.get('low', 0) * 100]
post_pct = [cohort_dist_post.get('high', 0) * 100, cohort_dist_post.get('low', 0) * 100]

x = np.arange(len(cohort_types))
width = 0.35

bars1 = ax.bar(x - width/2, pre_pct, width, label='Pre-Launch', color='#3b82f6', alpha=0.8, edgecolor='black')
bars2 = ax.bar(x + width/2, post_pct, width, label='Post-Launch', color='#ef4444', alpha=0.8, edgecolor='black')

ax.set_ylabel('% of Cohort', fontsize=12, fontweight='bold')
ax.set_title('Cohort Quality Shift: Higher Proportion of Low-Quality Users Post-Launch', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(cohort_types)
ax.legend(fontsize=11)
ax.set_ylim(0, 100)
ax.grid(True, axis='y', alpha=0.3)

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('docs/assets/cohort_shift.png', dpi=150, bbox_inches='tight')
print("✓ Saved: docs/assets/cohort_shift.png")
plt.close()

# === EXPORT DATA FOR HTML ===

output_data = {
    'engagement_drop_pct': round(esau_drop_pct, 1),
    'esau_pre': round(esau_pre, 4),
    'esau_post': round(esau_post, 4),
    'esau_exposed': round(esau_exposed, 4),
    'esau_not_exposed': round(esau_not_exposed, 4),
    'pre_treated': round(pre_treated, 4),
    'post_treated': round(post_treated, 4),
    'pre_control': round(pre_control, 4),
    'post_control': round(post_control, 4),
    'did_estimate': round(did_estimate, 4),
    'did_pct': round((did_estimate / pre_treated) * 100, 1) if pre_treated > 0 else 0,
    'feature_launch': feature_launch.strftime('%Y-%m-%d'),
    'feature_name': feature_name,
    'total_users': len(users),
    'total_events': len(events),
    'pre_launch_events': len(pre_launch),
    'post_launch_events': len(post_launch),
    'pre_cohort_high': round(cohort_dist_pre.get('high', 0) * 100, 1),
    'post_cohort_high': round(cohort_dist_post.get('high', 0) * 100, 1),
    't_stat': round(t_stat, 4),
    'p_value': round(p_value, 4)
}

with open('docs/assets/data_for_copilot.json', 'w') as f:
    json.dump(output_data, f, indent=2)

print("\n✓ All data extracted and visualizations generated!")
print(f"\nKey Metrics Summary:")
for key, value in output_data.items():
    print(f"  {key}: {value}")
