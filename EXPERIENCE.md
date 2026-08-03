# Abhitay Shinde — Experience Reference
Source of truth for resume/application generation. New York, NY.
abhitayshinde@gmail.com · (646) 225-0802 · linkedin.com/in/abhitay · github.com/Abhitay · scholar.google.com (user f0wnYuYAAAAJ)

## Summary
Data scientist blending generative AI, machine learning, and experimentation/causal inference to drive product and business decisions. Focus: causal inference, experimentation, GenAI personalization/agents, growth optimization, fintech & product analytics.

## Professional Experience

**Data Scientist — Customer Acquisition**, Ask2AI, New York, NY — Feb 2026–Present
Stack: Feature Engineering, Causal Inference, Polars
- Corrected selection bias in the scoring model via a feature engineering + causal inference pipeline (Python, Polars) integrating 11 source systems into a unified 30M-customer dataset.
- Scored rejected-applicant population at 0.86 held-out AUC using gradient-boosted models within a Double Machine Learning framework to correct selection bias in approved-only training data.
- Expanded approvable population 15% at flat expected default by handing corrected scores to credit policy.

**Data Scientist Contract — Generative AI & Personalization**, Julius Baer, New York, NY — Jun 2025–Sep 2025
Stack: Agentic LangGraph, LLM-as-a-Judge, RAG
- Replaced analyst-and-copywriter handoff for client-facing investment documents via an agentic LangGraph system retrieving client holdings, stated preferences, and live market news into one generated draft.
- Automated compliance review at 86% agreement with human reviewers, building an LLM-as-a-judge critic that scored drafts against the firm's rubric and regenerated failures until they passed.
- Cut content selection time for relationship managers 35% by shipping a chat interface with human-in-the-loop revision.
- Surfaced a 25% engagement lift via exploratory analysis (Python, SQL) against matched controls.

**Data Scientist Co-op — Customer Acquisition**, Ask2AI, New York, NY — Jan 2025–May 2025
Stack: Uplift Modeling, DiD, Mixed-Integer Optimization
- Improved cross-channel ROI attribution 22% and identified optimal credit limit thresholds via uplift models + difference-in-differences designs isolating incremental campaign impact from last-touch bias.
- Lifted customer LTV 12% and cut churn 25% by pairing uplift modeling with mixed-integer optimization to reallocate acquisition budget across channels.

**Data Scientist Capstone — Customer Analytics & Segmentation**, TD Bank, New York, NY — Jan 2025–May 2025
Stack: Customer Analytics, Fraud Detection, XGBoost
- Raised fraud model precision-recall AUC from 0.20 to 0.67 training XGBoost with SHAP on 100M transactions.
- Validated fraud-detection strategy for senior leadership by quantifying incremental catch rate against a holdout.
- Shaped segmentation and AML strategy by clustering customers on transaction behavior; delivered automated risk-tier reporting.

**Teaching Assistant — Algorithms to Data Science**, Columbia University, New York, NY — Sep 2024–Jan 2025
Stack: Student Mentorship, Experiment Design
- Mentored 250+ MS students on ML algorithms, analytical reasoning, experiment design, and inference.
- Designed case studies/assignments on A/B test design, modeling, and data-driven decision-making.

### Earlier Experience & Internships

**Data Science Intern — Operational Analytics**, Navin Fluorine International Limited, Mumbai, IN — May 2023–Nov 2023
- Reduced equipment downtime 35% and cut ingestion latency 40% via a predictive pipeline (XGBoost, Airflow).
- Lifted recall 15% and shortened repair cycles deploying anomaly detection (XGBoost, Isolation Forest).

**Founding IT Intern — Acquisition & Retention Analytics**, E-Revbay Pvt. Ltd., Mumbai, IN — Dec 2021–May 2022
- Increased qualified customer leads 50%/quarter leading acquisition analytics pipelines (Equifax data, SQL, Python).
- Eliminated 25% of manager intervention time via real-time dashboards and root-cause pipelines (Tableau).

**Artificial Intelligence Intern**, Verzeo, Remote — Jun 2021–Aug 2021
- Improved model accuracy 17% on tabular diamond classification via data cleaning/feature engineering.
- Built CNN-based flower image recognition, 85% accuracy, cutting error rates 15%.

## Education

**M.S. Data Science**, Columbia University, New York, NY — Sep 2024–Dec 2025, GPA 3.7/4.0
Coursework: Agentic AI, Fintech & Data Economy (PhD elective), Big Data Analytics, Statistics, Applied Machine Learning

**B.Tech Honors, Computer Engineering (Data Science/Analytics)**, NMIMS University, Mumbai, India — Jun 2020–May 2024, GPA 3.9/4.0

## Selected Projects (Portfolio Case Studies)

**Hybrid RAG Retrieval + Automated Evaluation Harness** — RAG, Hybrid Search, Reranking, LLM-as-Judge
Support bot answering from product manuals (exact error codes + vague queries): dense vectors + BM25 merged via reciprocal rank fusion, cross-encoder reranked, every sentence citation-checked. A companion system mines its own chat logs, judges answers, clusters failure modes, and emits a regression suite.
Results: reranking lifts recall@10 0.78→0.94, nDCG@10 0.55→0.75 (36 hand-verified questions); 94% of sentences grounded (123/131); eval generator finds 14% failure rate (mostly one mode: assuming an appliance on ambiguous questions); 87% agreement with human judge.

**Human-Gated Agent for Refund Automation** — Agents, Tool Calling, Human-in-the-Loop, Pydantic
Customer-service agent that looks up orders, reads refund policy, and issues refunds through typed/validated tools; money-moving actions pause for explicit human approval; every step logged with run_id for replay.
Results: 100% task success, 100% tool-call accuracy, 100% of high-risk actions gated on a 4-task fixture; one policy-ineligible refund stopped at approval boundary; $0.0006/task.

**Semantic Caching for LLM Cost & Latency** — LLMOps, Semantic Cache, Embeddings, FAISS
Compared exact-match vs. semantic caching against a no-cache baseline for hit rate, latency, and calls avoided; scored false-hit rate against Stack Exchange human-confirmed duplicates; operating point chosen from a swept curve against a stated false-hit budget.
Results: semantic caching lifts hit rate to 0.724 (vs. 0.691 exact-match), false hits held to 1.35% (2% budget), 3.5× latency improvement, on 3,316 real questions.

**Fine-Tuned, Guarded Text-to-SQL Copilot** — LoRA, Fine-Tuning, Guardrails, Text-to-SQL
LoRA adapters on 4-bit quantized Qwen2.5-Coder-1.5B, running locally via MLX on Apple silicon (peak memory 1.1GB, 16GB M1 Pro) instead of a rented GPU. Every query parsed to AST, allowed only as single SELECT on approved tables (keyword blocklist tried first, shown to fail). Confidence gate calibrated via measured ECE; low-confidence queries route to a human.
Results: fine-tuning lifts Spider execution accuracy 42.5%→47.5%, cuts invalid SQL 40%→36%; guarded fine-tuned model reaches 60% execution accuracy / 12% invalid SQL; guard blocks 100% of a 300-query red team vs. keyword blocklist wrong on 4/6 cases.

**IBM Agentic Library: Graph RAG for Document Q&A** — Graph RAG, Neo4j, FAISS, Retrieval
Hybrid Graph RAG system on a LangGraph-style agentic loop routing queries across vector search, structured financial tables, and graph reasoning over earnings-call documents. LLM-as-a-judge critic scores answers against a grounding rubric, regenerates failures, holds ~88% agreement with human reviewers.
Results: critic loop lifts grounded-answer rate 62% (first pass) → 91%; numeric reasoning remains hardest failure mode.

**Product Analytics Suite** — Causal Inference, Experimentation, PSM, Uplift Modeling
Three connected studies for product decisions: whether a feature truly worked, where growth budget pays off, and what caused a metric to drop (PSM/DiD, uplift/media mix modeling, root-cause DiD/cohort analysis).

**M(iche)Langelo: Analysis on AI-Generated Art** — CLIP, BLIP, Vision, AI Detection
Production-style Reddit pipeline scanning art posts to flag AI-generated images, identify likely source model, and describe style. Combines CLIP (style), BLIP (captions), SuSy (source detection); transfer-learned 3-class SuSy head (authentic, MidJourney, DALL-E 3).
Results: stronger MidJourney/DALL-E detection under real-world domain shift, with interpretability preserved via multimodal outputs.

## Publications & Media

**Media**: 1st place (of 750 teams, 19 countries, 1,311 participants), "Hackathon on Plastic-Free Rivers with AI," REVA University + Kyndryl, Sep 2023 — INR 150,000 prize for a Vision AI system detecting/classifying/segmenting river plastic from drone imagery. Featured in ThePrint (ANI PR).

**Research (Google Scholar, lead author unless noted)**:
- Predictive maintenance for metro systems — sensor-driven pipeline predicting equipment failures for targeted maintenance scheduling.
- Diabetes detection optimized for recall — model design prioritizing recall to reduce missed diagnoses.
- NLP to SQL for mobile learning — NLP-to-SQL interface for non-technical users to query student/CSV data on mobile.
- Semi-supervised disease prediction — semi-supervised methods leveraging unlabeled clinical data for robust prediction.

## Known-About / Skill Tags (from site metadata)
Causal Inference, Experimentation, A/B Testing, Machine Learning, Generative AI, Retrieval-Augmented Generation, Product Analytics, Uplift Modeling
