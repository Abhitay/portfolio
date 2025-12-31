# Growth Allocation Engine - Complete Documentation Index

## 📂 Project Structure

```
growth_engine/
├── figures/                              # 5 VISUALIZATIONS + DOCUMENTATION
│   ├── 01_incremental_ltv_by_channel.png              (163 KB)
│   ├── 02_naive_vs_optimized_allocation.png           (230 KB)
│   ├── 03_spend_vs_incremental_value_saturation.png   (302 KB)
│   ├── 04_roi_vs_incremental_ltv_scatter.png          (363 KB)
│   ├── 05_executive_summary_flow.png                  (300 KB)
│   ├── README.md                         # Technical methodology guide
│   └── QUICK_REFERENCE.txt               # One-page visual index
│
├── datadesign/                           # DATA FILES
│   ├── channel_summary.csv               # Aggregated channel metrics
│   ├── baseline_allocation.csv           # Baseline budget scenario
│   ├── optimal_allocation.csv            # MILP-optimized allocation
│   ├── incremental_ltv_results.csv       # Causal LTV per channel
│   ├── uplift_results.csv                # Per-user treatment effects
│   ├── revenue.csv, churn.csv, users.csv # Raw data (pre-modeled)
│   └── data_creation.ipynb               # Data generation notebook
│
├── uplift.ipynb                          # XGBoost treatment effect modeling
├── ltv_forecast.ipynb                    # Cox PH survival-based LTV
├── optimization.ipynb                    # MILP budget optimization
├── dashboard.py                          # Streamlit interactive app
├── generate_visualizations.py            # Script to regenerate plots
│
├── INSIGHTS_AND_NARRATIVE.md             # 📖 BUSINESS NARRATIVE
│   └── Problem → Solution → Results → Recommendations
│
└── VISUALIZATION_DELIVERY_SUMMARY.md     # ✅ PROJECT STATUS & GUIDE
    └── What was delivered, how to use it, next steps
```

---

## 🎯 Quick Start: What to Read First

### For Executive / Decision-Maker (15 min)
1. Read: [VISUALIZATION_DELIVERY_SUMMARY.md](VISUALIZATION_DELIVERY_SUMMARY.md) - **Project Status**
2. View: `figures/05_executive_summary_flow.png` - **Decision Framework**
3. View: `figures/01_incremental_ltv_by_channel.png` - **Channel Value Ranking**
4. View: `figures/02_naive_vs_optimized_allocation.png` - **Budget Reallocation**
5. Read: [INSIGHTS_AND_NARRATIVE.md](INSIGHTS_AND_NARRATIVE.md) - **"Key Insights" section**

**Key Message:** Same $500k budget, +$116k additional value (+2.4%) via causal analysis.

---

### For Analytics / Data Science Team (45 min)
1. Read: [figures/README.md](figures/README.md) - **Technical Methodology**
2. Review: All 5 visualizations - **Detailed Interpretation**
3. Read: [INSIGHTS_AND_NARRATIVE.md](INSIGHTS_AND_NARRATIVE.md) - **Full Business Context**
4. Examine: `generate_visualizations.py` - **Reproducibility**
5. Reference: Notebooks (`uplift.ipynb`, `ltv_forecast.ipynb`, `optimization.ipynb`) - **Methodology**

**Key Message:** XGBoost uplift + Cox PH LTV + MILP optimization yields 2.4% better allocation.

---

### For Portfolio / Case Study (1-2 hours)
1. Review: [VISUALIZATION_DELIVERY_SUMMARY.md](VISUALIZATION_DELIVERY_SUMMARY.md) - **Deliverables Overview**
2. Read: [INSIGHTS_AND_NARRATIVE.md](INSIGHTS_AND_NARRATIVE.md) - **Full Narrative**
3. View: All 5 visualizations (in order) - **Story Arc**
4. Reference: [figures/README.md](figures/README.md) - **Methodology Details**
5. Read: [figures/QUICK_REFERENCE.txt](figures/QUICK_REFERENCE.txt) - **Interpretation Guide**
6. Copy: Python script & CSVs to reproduce - **Reproducibility**

**Key Message:** Causal budget allocation outperforms naive ROI-based decisions by 2-3%.

---

## 📊 The 5 Visualizations

| # | File | Type | Key Message | Audience |
|---|------|------|---|---|
| 1 | `01_incremental_ltv_by_channel.png` | Bar | Why referral > paid search on LTV | Exec, Technical |
| 2 | `02_naive_vs_optimized_allocation.png` | Grouped Bar | Where $53k moves and why | Exec, Stakeholder |
| 3 | `03_spend_vs_incremental_value_saturation.png` | Bubble | Saturation justifies constraints | Technical |
| 4 | `04_roi_vs_incremental_ltv_scatter.png` | Scatter | Why ROI-based decisions fail | Data, Blog |
| 5 | `05_executive_summary_flow.png` | Flow | Data → Causal → Optimization → Decision | All Levels |

**Use these visualizations for:**
- Portfolio case study (1, 2, 5 featured; 3, 4 appendix)
- Blog post / LinkedIn (focus on 4, support with 2)
- Board presentation (2 + 5 + 2-minute oral)
- Pitch deck (5 + 1 + 2)
- Internal training (all 5 in order)

---

## 🔑 Key Results Summary

### Channel Performance (Ranked by Incremental LTV)

| Channel | Incremental LTV | Avg Cost | ROI | Optimal Spend | Expected Value |
|---------|---|---|---|---|---|
| **Referral** | $21.22 | $1.00 | 21.2x | $80k | $1.69M |
| **Paid Search** | $14.96 | $3.00 | 5.0x | $200k | $0.99M |
| **Affiliate** | $10.56 | $2.50 | 4.2x | $100k | $0.42M |
| **Organic** | $6.94 | $0.20 | 34.7x | $50k | $1.73M |
| **Social Ads** | $5.62 | $2.00 | 2.8x | $70k | $0.23M |

### Budget Reallocation

```
Paid Search:   $147k → $200k  (+$53k, +36%)   Invest more
Social Ads:    $123k → $70k   (-$53k, -43%)   Reduce
Referral:      $80k  → $80k   (no change)     Hold
Affiliate:     $100k → $100k  (no change)     Stable
Organic:       $50k  → $50k   (no change)     Hold
```

### Total Impact

- **Baseline Expected Value:** $4.93M
- **Optimized Expected Value:** $5.04M
- **Uplift:** +$116k (+2.4%)
- **Same Budget:** $500k
- **Payback:** Incremental value / budget = 23.2% annualized

---

## 📚 Documentation Map

### For Understanding *What* We Did
→ Read: [VISUALIZATION_DELIVERY_SUMMARY.md](VISUALIZATION_DELIVERY_SUMMARY.md)
- Project status ✅
- What was delivered
- Quality checklist
- How to use deliverables

### For Understanding *Why* We Did It
→ Read: [INSIGHTS_AND_NARRATIVE.md](INSIGHTS_AND_NARRATIVE.md)
- Problem: ROI-based allocation fails
- Insight: Incremental LTV > ROI
- Solution: Causal analysis + MILP
- Results: +$116k value
- Recommendations: Next steps

### For Understanding *How* We Did It
→ Read: [figures/README.md](figures/README.md)
- Causal uplift estimation (XGBoost)
- LTV forecasting (Cox PH)
- Budget optimization (MILP)
- Data sources & preprocessing
- Methodology limitations

### For Quick Reference
→ Read: [figures/QUICK_REFERENCE.txt](figures/QUICK_REFERENCE.txt)
- One-page visual index
- Interpretation guide per diagram
- Use cases & audiences
- Storytelling framework
- Assumptions & limitations

### For Reproducibility
→ Run: `generate_visualizations.py`
- Reads CSVs (no model retraining)
- Generates 5 PNG files (300 DPI)
- Summary statistics printed
- Takes <10 seconds

---

## 🎬 How to Present This

### Elevator Pitch (2 min)
> "Our growth team allocates budget by ROI. But incremental LTV tells a different story. Referral users are worth $21; paid search users, $15. Rebalancing saves $53k from low-value social ads and invests in paid search. Result: same budget, +$116k additional lifetime value. That's a 2.4% free uplift."

### 5-Minute Pitch
Use: Diagram 5 → Diagram 1 → Diagram 2

> "Here's our decision framework [5]. We model causal incremental value—not ROI. [1] Here's where budget moves [2]. Why? Because causal analysis reveals user quality differences ROI can't see."

### 30-Minute Technical Deep-Dive
Use: All diagrams + [figures/README.md](figures/README.md)

1. Problem: ROI hides quality → Diagram 4
2. Solution: Causal modeling → Diagram 5
3. Methodology: Uplift + LTV + MILP → [figures/README.md](figures/README.md)
4. Results: Reallocation → Diagram 2
5. Saturation & constraints → Diagram 3
6. Recommendations → [INSIGHTS_AND_NARRATIVE.md](INSIGHTS_AND_NARRATIVE.md)

### Blog Post / LinkedIn Article
Focus: Diagram 4 + narrative

> "Why Traditional Growth Metrics Fail: The ROI Paradox"
> 
> "Organic channels show 34x ROI but $6.94 lifetime value. Referral shows 21x ROI and $21.22 lifetime value. This paradox reveals why ROI-based budget allocation systematically underfunds high-value channels. Here's what we did instead... [Diagram 4] [Diagram 2]"

---

## 🚀 Next Steps

### This Week
- [ ] Review visualizations with stakeholders
- [ ] Gather feedback on messaging & clarity
- [ ] Integrate into case study / presentation

### Next 2 Weeks
- [ ] Create 1-page executive summary
- [ ] Draft blog post (focus on Diagram 4)
- [ ] Present to leadership for approval

### This Month
- [ ] Implement reallocation in test markets
- [ ] Set up monitoring dashboard
- [ ] Design post-implementation analysis

### Quarterly
- [ ] Retrain uplift & LTV models
- [ ] Regenerate visualizations with new data
- [ ] Update narrative with actual results

---

## 🔧 Technical Details

### Reproducibility
```bash
cd /Users/abhitay/Developer/portfolio/abhitay-portfolio
python growth_engine/generate_visualizations.py
# Outputs: growth_engine/figures/*.png (300 DPI, publication-ready)
```

### Dependencies
- pandas >= 1.0
- numpy >= 1.19
- matplotlib >= 3.3
- seaborn >= 0.11

### Data Sources (No Model Retraining)
- All visualizations read from CSV files in `datadesign/`
- No data cleaning or transformation
- Reproducible anywhere with Python 3.8+

---

## ✅ Quality Checklist

- ✅ **Publication-ready:** 300 DPI (print quality)
- ✅ **Accessible design:** Color-blind friendly, high contrast
- ✅ **Clear labeling:** All axes, titles, footnotes
- ✅ **Executive-readable:** Jargon minimal, storytelling focused
- ✅ **Reproducible:** Python script provided
- ✅ **Non-invasive:** No model changes; data-only visualizations
- ✅ **Business-focused:** Each plot supports a growth decision
- ✅ **Well-documented:** 4 supporting documents provided

---

## 📞 Questions?

**What are these visualizations for?**
→ Portfolio case study demonstrating causal budget allocation

**Can I modify them?**
→ Edit `generate_visualizations.py` and regenerate

**How do I incorporate them into my case study?**
→ See "How to Present This" section above + [VISUALIZATION_DELIVERY_SUMMARY.md](VISUALIZATION_DELIVERY_SUMMARY.md)

**Do they require retraining models?**
→ No. All plots read from CSVs; no model changes

**What's the main insight?**
→ Causal incremental LTV (uplift + survival) beats naive ROI for budget allocation

---

## 📄 File Manifest

**Visualizations (5 files, 1.3 MB):**
- `figures/01_incremental_ltv_by_channel.png`
- `figures/02_naive_vs_optimized_allocation.png`
- `figures/03_spend_vs_incremental_value_saturation.png`
- `figures/04_roi_vs_incremental_ltv_scatter.png`
- `figures/05_executive_summary_flow.png`

**Documentation (4 files, 65 KB):**
- `figures/README.md` — Technical methodology
- `figures/QUICK_REFERENCE.txt` — One-page visual guide
- `INSIGHTS_AND_NARRATIVE.md` — Business narrative
- `VISUALIZATION_DELIVERY_SUMMARY.md` — Project status

**Scripts (1 file, 19 KB):**
- `generate_visualizations.py` — Visualization generator

**Data (pre-existing in `datadesign/`):**
- CSVs for all visualizations (no changes made)

---

## 🎓 Learning Outcomes

By reviewing these artifacts, stakeholders will understand:

1. **Why causal analysis matters**
   - Uplift + LTV > ROI for allocation decisions
   - Correlation hides user quality heterogeneity

2. **What optimization solves**
   - MILP finds Pareto frontier subject to constraints
   - Portfolio approach beats single-channel bets

3. **How to think about channels**
   - Saturation is real (can't scale infinitely)
   - Trust channels > volume channels on lifetime basis

4. **How to allocate budget**
   - Incremental value-driven, not conversion-driven
   - Constraints prevent concentration risk & ensure resilience

---

**Project:** Growth Allocation Engine  
**Status:** ✅ Complete  
**Deliverables:** 5 visualizations + 4 documentation files  
**Quality:** Portfolio-ready (300 DPI, publication quality)  
**Reproducibility:** Python script provided  
**Date:** December 25, 2025

---
