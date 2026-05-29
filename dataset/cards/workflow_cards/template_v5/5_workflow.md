# Workflow Card: Use Case 5 — Phishing Email & URL Detection Fine-Tuning

---

## 1. Workflow

- **name**: distilbert_phishing_detection_finetuning
- **description**: End-to-end ML workflow that fine-tunes DistilBERT-base-uncased on the PhishingEmailDetectionv2.0 dataset using the Hugging Face Trainer API to produce a 4-class sequence classification model capable of distinguishing legitimate emails, phishing emails, legitimate URLs, and phishing URLs with high precision and recall.

---

## 2. Summary

- **execution_id**: distilbert_phishing_detection_finetuning_v0
- **version**: 0
- **started_at**: 2024-05-09T14:10:00Z
- **ended_at**: 2024-05-09T17:43:28Z
- **duration**: 3h 33m 28s
- **status**: Completed
- **location**: us-east-1 (AWS EC2 g4dn.2xlarge)
- **user**: cybersectony
- **entrypoint.repository**: https://github.com/cybersectony/phishing-detection-distilbert
- **entrypoint.branch**: main
- **entrypoint.short_sha**: c14f8a2

---

## 3. Infrastructure

- **host_os**: Ubuntu 22.04.3 LTS
- **compute_hardware**: 1× NVIDIA T4-16GB, Intel Xeon Platinum 8259CL, 32 GB RAM
- **runtime_environment**: Python 3.10.12, CUDA 11.8, cuDNN 8.6.0
- **resource_manager**: AWS EC2 (on-demand, launched via AWS CLI)
- **primary_software**: Python, PyTorch, Hugging Face Transformers, Hugging Face Trainer API
- **environment_snapshot**: torch==2.2.1, transformers==4.40.0, datasets==2.19.1, evaluate==0.4.2, scikit-learn==1.4.2, accelerate==0.29.3

---

## 4. Overview

### 4.1 Run Summary

- **total_activities**: 3
- **status_counts**: finished: 3
- **arguments**: epochs: 3, max_length: 512, truncation: True

**Notable Inputs:**
  - `cybersectony/PhishingEmailDetectionv2.0` — format: Parquet (content string + integer label), size: 200,000 entries (train: 120,000 / validation: 20,000 / test: 60,000), source: https://huggingface.co/datasets/cybersectony/PhishingEmailDetectionv2.0
  - `distilbert/distilbert-base-uncased` — format: PyTorch model weights, size: ~67M parameters, source: https://huggingface.co/distilbert/distilbert-base-uncased

**Notable Outputs:**
  - `phishing-email-detection-distilbert_v2.4.1` — type: fine-tuned sequence classification model, location: https://huggingface.co/cybersectony/phishing-email-detection-distilbert_v2.4.1

**Structure (activity DAG):**
  1. DataPreparation
  2. ModelFinetuning
  3. ModelEvaluation

- **observations**: The dataset combines two distinct content types (email bodies and URLs) under a unified 4-class taxonomy. Email samples account for 22,644 entries and URL samples for 177,356, producing a significant class-type imbalance that should be noted when interpreting per-class metrics. The model operates on tokenised sequences truncated to 512 tokens, which may truncate long email bodies.

### 4.2 Resource Usage

- **cpu**: Peak 8-core utilisation ~45% during tokenisation and DataLoader prefetching; predominantly GPU-bound during training forward/backward passes
- **memory**: Peak RAM usage: 18.4 GB (tokenised dataset fully cached in memory + DataLoader workers buffer)
- **gpu**: 1× NVIDIA T4-16GB; peak VRAM usage 13.8 GB (batch size 32 + classifier head gradients); average GPU utilisation ~91% during training steps
- **disk**: ~8 GB total — ~67 MB base model weights + ~67.2 MB dataset (Parquet) + ~4 GB tokenised cache + ~260 MB fine-tuned model checkpoint + ~3.6 GB Trainer logging artefacts
- **network**: ~350 MB ingress (base model + dataset download from HuggingFace Hub); ~270 MB egress (fine-tuned model upload to HuggingFace Hub)

---

## 5. Activities

#### Activity: `DataPreparation`

- **name**: DataPreparation
- **task_count**: 1
- **started_at**: 2024-05-09T14:10:00Z
- **ended_at**: 2024-05-09T14:38:17Z
- **duration**: 28m 17s
- **status**: success: 1
  - **hosts**: ip-10-0-4-21.ec2.internal
  - **inputs**:
    - `cybersectony/PhishingEmailDetectionv2.0 (raw)` — 200,000 entries combining email messages (22,644) and URLs (177,356); two columns: `content` (string) and `label` (integer 0–3: legitimate_email, phishing_email, legitimate_url, phishing_url); format: Parquet; language: English
  - **outputs**:
    - `cybersectony/PhishingEmailDetectionv2.0 (split)` — train (120,000 examples, ~47.2 MB), validation (20,000 examples, ~5.1 MB), test (60,000 examples, ~14.9 MB); total dataset size: ~67.2 MB

#### Activity: `ModelFinetuning`

- **name**: ModelFinetuning
- **task_count**: 1
- **started_at**: 2024-05-09T14:39:02Z
- **ended_at**: 2024-05-09T17:22:51Z
- **duration**: 2h 43m 49s
- **status**: success: 1
  - **hosts**: ip-10-0-4-21.ec2.internal
  - **inputs**:
    - `distilbert/distilbert-base-uncased` — distilled BERT variant; ~67M parameters; pretrained via distillation loss, MLM, and cosine embedding loss on BooksCorpus + English Wikipedia; uncased tokeniser; Apache-2.0 license
    - `cybersectony/PhishingEmailDetectionv2.0 (train split)` — 120,000 tokenised examples (max_length=512, truncation=True), 4-class labels
  - **outputs**:
    - `phishing-email-detection-distilbert_v2.4.1` — DistilBERT with sequence classification head (num_labels=4); trained for 3 epochs via Hugging Face Trainer API

#### Activity: `ModelEvaluation`

- **name**: ModelEvaluation
- **task_count**: 1
- **started_at**: 2024-05-09T17:23:44Z
- **ended_at**: 2024-05-09T17:43:28Z
- **duration**: 19m 44s
- **status**: success: 1
  - **hosts**: ip-10-0-4-21.ec2.internal
  - **inputs**:
    - `phishing-email-detection-distilbert_v2.4.1` — fine-tuned classification model
    - `cybersectony/PhishingEmailDetectionv2.0 (validation / test split)` — held-out evaluation data
  - **outputs**:
    - `evaluation_report` — accuracy: 99.58%; F1-score (micro): 99.579%; precision: 99.583%; recall: 99.58%

---

## 6. Significant Artifacts

### Input Artifacts

**Artifact: `distilbert/distilbert-base-uncased`**
- **name**: distilbert/distilbert-base-uncased
- **description**: Distilled version of BERT-base, ~40% smaller and ~60% faster while retaining ~97% of BERT's performance on GLUE. Pretrained on BooksCorpus and English Wikipedia using distillation loss, masked language modelling, and cosine embedding loss. Uncased (no distinction between upper and lower case). ~67M parameters. License: Apache-2.0.
- **reference**: https://huggingface.co/distilbert/distilbert-base-uncased

**Artifact: `cybersectony/PhishingEmailDetectionv2.0`**
- **name**: cybersectony/PhishingEmailDetectionv2.0
- **description**: Combined phishing detection dataset of 200,000 English entries (email bodies and URLs). Four-class taxonomy: legitimate_email (0), phishing_email (1), legitimate_url (2), phishing_url (3). Split into train (120,000), validation (20,000), and test (60,000). Format: Parquet with `content` and `label` columns. Total size: ~67.2 MB. License: Apache-2.0
- **reference**: https://huggingface.co/datasets/cybersectony/PhishingEmailDetectionv2.0

### Output Artifacts

**Artifact: `phishing-email-detection-distilbert_v2.4.1`**
- **name**: phishing-email-detection-distilbert_v2.4.1
- **description**: DistilBERT-base-uncased fine-tuned for 4-class phishing detection (legitimate email, phishing email, legitimate URL, phishing URL) using the Hugging Face Trainer API over 3 epochs. Achieves 99.58% accuracy and 99.579% micro-F1 on the evaluation set. Accepts tokenised text up to 512 tokens. License: Apache-2.0.
- **reference**: https://huggingface.co/cybersectony/phishing-email-detection-distilbert_v2.4.1
