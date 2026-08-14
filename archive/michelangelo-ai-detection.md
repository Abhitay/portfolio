# M(iche)Langelo: Analysis on AI-Generated Art

End-to-end pipeline for large-scale AI-art detection, style analysis, captioning, and optional restyling.

## TL;DR

M(iche)Langelo is a production-style Reddit pipeline for monitoring and analyzing AI-generated art. It combines CLIP for style, BLIP for captions, and SuSy for source detection, with a transfer-learned 3-class SuSy head (authentic, MidJourney, DALL-E 3) that improves AI-class detection on real-world Reddit data. The result is stronger MidJourney and DALL-E detection under domain shift, with interpretability preserved through the multimodal outputs.

## Contents

- Introduction

- Related Work

- Data

- Methods

- Results

- System Overview

- Recommendation

## Introduction

The spread of high-fidelity text-to-image models raised practical trust issues for online visual ecosystems: attribution, misuse, and authenticity ambiguity. Existing detectors trained on curated benchmarks showed weak transfer to noisy social data.

The core question was whether an end-to-end, continuously evaluated system could maintain reliable detection performance on Reddit while also surfacing useful style and semantic context for human review.

Open social streams are weakly labeled and constantly shifting; single-model accuracy alone is not enough for operational trust.

## Related Work

#### Synthetic image detection

Artifact-based GAN detectors struggle on modern diffusion outputs. SuSy improves generalization but can degrade under domain shift.

#### Vision-language models

CLIP provides strong zero-shot style recognition and BLIP adds semantic captioning that improves interpretability and downstream utility.

#### System-level gap

Most studies use static datasets; few combine continuous ingestion, scalable storage, inference, and evaluation in one loop.

## Data

Data strategy focused on independent fine-tuning sets plus real-world Reddit test streams from model-specific communities.

#### Fine-tuning data

- Three target classes: authentic, MidJourney, DALL-E 3

- 1,000 images per class with 70/30 train-validation split

- Sources chosen to avoid overlap with original SuSy training data

#### Reddit test stream

- Subreddits: r/dalle2, r/midjourney, r/aiArt, r/Art

- Most recent 1,000 posts per subreddit with NSFW filtering

- Weak supervision via subreddit provenance and flair metadata

#### Observed activity rates

- r/dalle2: 1.28 posts/day

- r/midjourney: 35.71 posts/day

- r/aiArt: 111.11 posts/day

#### Frequency of AI-generated image subreddits

![Example Reddit DALL-E image 1](figures/michelangelo_reddit_dalle_sample_1.jpeg)

Figure 1: Example Reddit DALL-E image (sample 1).

![Example Reddit DALL-E image 2](figures/michelangelo_reddit_dalle_sample_2.jpeg)

Figure 2: Example Reddit DALL-E image (sample 2).

![Example Reddit DALL-E image 3](figures/michelangelo_reddit_dalle_sample_3.jpeg)

Figure 3: Example Reddit DALL-E image (sample 3) showing non-artistic variance in the test stream.

## Methods

The pipeline has two major layers: automated data engineering and multimodal inference. Airflow orchestrates Reddit collection, deduplication by submission ID, and metadata updates to BigQuery. Inference then runs CLIP (style), BLIP (caption), and SuSy (source).

#### Data pipeline

Scheduled collectors ingest new images, persist content to cloud storage, and append structured metadata tables for tracking and evaluation.

#### Transfer learning

SuSy was adapted from 6-class outputs to a 3-class projection layer, then fine-tuned end-to-end for Reddit-style domain adaptation.

#### Interpretability

Style rankings, captions, and class probabilities are surfaced together through a Gradio UI for rapid qualitative validation.

![Apache Airflow DAG diagram. Reddit posts are ingested and stored in BigQuery, then fork into three parallel inference tasks (CLIP for style classification, BLIP for captioning, and SuSy for three-class source detection) which converge into an aggregate-and-evaluate step, with an optional SDXL restyle stage.](figures/michelangelo-dag.svg)

Figure 4: the Airflow DAG, with scheduled ingestion into BigQuery, three parallel inference models, then aggregation and evaluation.

## Results

Baseline CNNs (ResNet variants) underperformed on Reddit’s diverse artistic distributions. BLIP outperformed earlier captioning attempts on semantic richness, and CLIP prompt engineering improved style ranking stability. The strongest gains came from SuSy transfer learning under domain shift.

Finetuning significantly increased AI-class detection quality on Reddit-like data, indicating that domain-adaptive heads are critical for real deployment.

![BLIP captioning examples on artistic and synthetic images](figures/michelangelo_blip_caption_results.png)

Figure 6: BLIP-generated captions showing semantically rich image descriptions used for interpretability and restyling prompts.

![Stable Diffusion XL restyling examples guided by BLIP captions](figures/michelangelo_sdxl_restyle_results.png)

Figure 8: Stable Diffusion XL image-to-image restyling guided by BLIP captions while preserving semantic structure.

## System Overview

M(iche)Langelo is implemented in Python with PyTorch, Transformers, OpenCLIP, Diffusers, PRAW, Airflow, and BigQuery. The architecture is modular, enabling continuous collection, scalable storage, and iterative model updates.

#### Continuous ingestion

Airflow + PRAW keep datasets fresh from active Reddit communities.

#### Multimodal inference

CLIP, BLIP, and SuSy provide style, semantic, and source signals in one pass.

#### Scalable analytics

BigQuery stores metadata, predictions, confidence scores, and execution traces.

#### Interactive inspection

Gradio UI enables rapid qualitative review and restyling workflows.

![Gradio interface showing image upload and analysis configuration controls](figures/michelangelo_gradio_ui_input.png)

Figure 11: Interactive analysis UI with model options and execution controls.

![Gradio output panel with BLIP caption, CLIP styles, and SuSy source probabilities](figures/michelangelo_gradio_ui_output.png)

Figure 12: Structured output panel combining caption, style ranking, and source-detection probabilities.

![BigQuery sample rows with CLIP and BLIP output columns](figures/michelangelo_bigquery_sample_rows.png)

Figure 13: BigQuery sample rows showing pipeline outputs and model predictions.

## Recommendation

### Use as real-time monitoring + analyst assist

Keep the transfer-learned SuSy pipeline in production for social streams, with recurring re-training, confidence calibration, and richer supervision signals beyond subreddit labels.

### Next Iteration Priorities

- Add watermark and metadata forensics to complement model-based detection.

- Distill inference stack for lower-latency batch throughput.

- Expand source classes beyond MidJourney and DALL-E 3.

- Automate drift reporting and threshold tuning for deployment governance.
