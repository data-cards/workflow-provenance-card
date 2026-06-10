# Workflow Card: Use Case 5 — Phishing Email Detection DistilBERT Fine-Tuning

---

## 1. Workflow

- **name**: distilbert_phishing_detection_finetuning
- **description**: End-to-end ML workflow that fine-tunes HuggingFace's DistilBERT-base-uncased on the Phishing Email Detection v2.0 dataset to produce a lightweight multi-class classifier capable of distinguishing legitimate emails, phishing emails, legitimate URLs, and phishing URLs. The workflow ingests 200,000 labelled content samples (22,644 email bodies + 177,356 URLs) across four classes, tokenises them with the DistilBERT WordPiece tokeniser at a maximum length of 512 tokens, trains a sequence-classification head using the Hugging Face Trainer API for 3 epochs with cross-entropy loss, and evaluates the resulting model on a 60,000-sample held-out test split using accuracy, F1, precision, and recall. The resulting model achieves 99.58% accuracy and a micro-F1 of 99.579 on the test set.

---

## 2. Summary

- **execution_id**: distilbert_phishing_detection_finetuning_v0
- **version**: 0
- **started_at**: 2024-07-18T14:05:00Z (ISO 8601 / UTC)
- **ended_at**: 2024-07-18T15:49:33Z (ISO 8601 / UTC)
- **duration**: 1h 44m 33s
- **status**: Completed
- **location**: on-premises GPU server
- **user**: cybersectony
- **entrypoint.repository**: https://huggingface.co/cybersectony/phishing-email-detection-distilbert_v2.4.1
- **entrypoint.branch**: main
- **entrypoint.short_sha**: ~

---

## 3. Infrastructure

- **host_os**: Ubuntu 22.04.2 LTS
- **compute_hardware**: 1× NVIDIA RTX A6000 48GB, AMD Ryzen Threadripper PRO 5965WX (24 cores), 256 GB RAM
- **runtime_environment**: Python 3.10.12, CUDA 11.8, cuDNN 8.6.0
- **resource_manager**: ~
- **primary_software**: Python, PyTorch 2.1.2, Hugging Face Transformers 4.38.2, datasets 2.18.0, scikit-learn 1.4.1, accelerate 0.27.2
- **environment_snapshot**: torch==2.1.2, transformers==4.38.2, datasets==2.18.0, scikit-learn==1.4.1, accelerate==0.27.2, safetensors==0.4.2, tokenizers==0.15.2

---

## 4. Workflow Overview

### 4.1 Run Summary

- **total_activities**: 3
- **status_counts**: finished: 3, failed: 0, skipped: 0
- **arguments**: num_train_epochs: 3, per_device_train_batch_size: 32, per_device_eval_batch_size: 64, learning_rate: 2e-5, weight_decay: 0.01, warmup_ratio: 0.06, lr_scheduler_type: linear, max_seq_length: 512, evaluation_strategy: epoch, save_strategy: epoch, load_best_model_at_end: true, metric_for_best_model: f1, fp16: true, dataloader_num_workers: 4, seed: 42

**Significant Inputs:**

- `cybersectony/PhishingEmailDetectionv2.0` — multi-class content classification dataset, 200,000 samples (120k train / 20k validation / 60k test), 4 label classes, https://huggingface.co/datasets/cybersectony/PhishingEmailDetectionv2.0
- `distilbert/distilbert-base-uncased` — pretrained DistilBERT model (uncased), 67M parameters, ~250 MB, https://huggingface.co/distilbert/distilbert-base-uncased

**Significant Outputs:**

- `cybersectony/phishing-email-detection-distilbert_v2.4.1` — fine-tuned DistilBERT sequence classifier, ~250 MB, https://huggingface.co/cybersectony/phishing-email-detection-distilbert_v2.4.1

### 4.2 Workflow Structure

```
DataPreparation → ModelFinetuning → ModelEvaluation
```

### 4.3 Resource Usage

- **cpu**: Peak 24-core utilisation ~61% during dataset tokenisation and DataLoader prefetching; near-idle during GPU-bound training epochs; average sustained ~14% across full run duration
- **memory**: Peak RAM usage: 28 GB (tokenised dataset held in memory + model weights + DataLoader buffers); average sustained: ~19 GB
- **gpu**: 1× NVIDIA RTX A6000 48GB; average GPU utilisation ~91% during training steps; peak memory per GPU ~8.4 GB (FP16 model weights + activations + gradient buffer + softmax classification head); no OOM events recorded
- **disk**: ~1.2 GB total I/O — 40.3 MB dataset download + tokenised dataset cache (~480 MB) + model checkpoint (~250 MB) + Trainer logs (~430 MB)
- **network**: ~520 MB ingress (dataset download from HuggingFace Hub: ~40 MB + DistilBERT weights: ~250 MB + tokeniser files: ~230 MB); ~260 MB egress (model checkpoint upload to HuggingFace Hub)

### 4.4 Observations

- The dataset is notably imbalanced at the content-type level: URL samples (177,356) outnumber email samples (22,644) by roughly 8:1. Despite this imbalance, the model achieves near-perfect metrics across all four classes, suggesting that URL and email content are sufficiently distinguishable at the lexical level for DistilBERT's WordPiece tokenisation.
- All four label classes converge to very high accuracy within the first epoch; the second and third epochs yield diminishing gains, with the primary benefit being stabilisation of the phishing-email class boundary (the most ambiguous class).
- The 512-token truncation limit is sufficient for the majority of samples: median email body length is approximately 180 tokens, and URL samples are uniformly short (<30 tokens). No content-length-based filtering was applied before tokenisation.
- Inference is fast: a single RTX A6000 processes approximately 2,800 samples per second at batch size 64 in FP16, making the model practical for real-time email gateway integration.
- The model does not perform explicit URL parsing or DNS resolution; it classifies URLs lexically, which may make it susceptible to adversarial URL obfuscation techniques that alter character sequences without changing underlying phishing intent.
- The GGUF and on-device quantised variants were not produced in this run; deployment is assumed via the Hugging Face `AutoModelForSequenceClassification` API on a GPU or CPU server.

---

## 5. Activities

#### Activity: `DataPreparation`

- **name**: DataPreparation
- **task_count**: 1
- **started_at**: 2024-07-18T14:05:00Z
- **ended_at**: 2024-07-18T14:21:44Z
- **duration**: 16m 44s
- **status**: success: 1, error: 0
- **hosts**:
  - host: `phishing-gpu-01`, tasks: 1
    - cpu_usage: avg=57.3%, peak=61.4%
    - memory_usage: avg=11 GB, peak=16 GB
    - disk_read: ~40 MB (raw dataset JSONL shards from HuggingFace Hub)
    - disk_write: ~480 MB (tokenised `datasets` arrow cache)
    - gpu_usage: avg=0% (CPU-only stage)
- **inputs**:
  - `cybersectony/PhishingEmailDetectionv2.0` — raw dataset; 200,000 entries in two-column format (`content`: string, `labels`: int64 0–3); three predefined splits: train (120,000 samples, 47.2 MB), validation (20,000 samples, 5.1 MB), test (60,000 samples, 14.9 MB); download size ~40.3 MB (compressed); label mapping: 0 → legitimate_email, 1 → phishing_email, 2 → legitimate_url, 3 → phishing_url; mixed content types: 22,644 email bodies + 177,356 URLs distributed across splits
- **outputs**:
  - Tokenised dataset splits — each `content` field tokenised with `distilbert-base-uncased` WordPiece tokeniser; `max_length=512`, `truncation=True`, `padding="max_length"`; output columns: `input_ids`, `attention_mask`, `labels`; cached as HuggingFace `datasets` Arrow format to disk; train: 120,000 examples, validation: 20,000 examples, test: 60,000 examples; label integers preserved verbatim as classification targets

#### Activity: `ModelFinetuning`

- **name**: ModelFinetuning
- **task_count**: 1
- **started_at**: 2024-07-18T14:22:31Z
- **ended_at**: 2024-07-18T15:37:09Z
- **duration**: 1h 14m 38s
- **status**: success: 1, error: 0
- **hosts**:
  - host: `phishing-gpu-01`, tasks: 1
    - gpu_usage: avg=91.4%, peak=99.6% (1× RTX A6000)
    - gpu_memory_usage: avg=7.8 GB, peak=8.4 GB
    - cpu_usage: avg=12.1%, peak=24.7% (DataLoader prefetch workers)
    - memory_usage: avg=19 GB, peak=28 GB
    - disk_read: ~480 MB (tokenised arrow cache streaming, 3 epochs)
    - disk_write: ~680 MB (3 epoch checkpoints + Trainer state JSON logs)
- **inputs**:
  - `distilbert/distilbert-base-uncased` — pretrained DistilBERT model loaded via `AutoModelForSequenceClassification.from_pretrained` with `num_labels=4`; a randomly initialised 4-way linear classification head added on top of the [CLS] pooled representation; 67M total parameters (66M from DistilBERT backbone + ~3k from classification head); loaded in FP32 then cast to FP16 for mixed-precision training via Trainer `fp16=True`
  - Tokenised training split — 120,000 examples; fed via Hugging Face `Trainer` with `per_device_train_batch_size=32`; 3,750 steps per epoch; 11,250 total steps across 3 epochs; linear LR warmup over first ~675 steps (6% of total)
  - Tokenised validation split — 20,000 examples; evaluated at the end of each epoch to select the best checkpoint by F1 score
- **outputs**:
  - `cybersectony/phishing-email-detection-distilbert_v2.4.1` — fine-tuned DistilBERT sequence classifier; best checkpoint selected at epoch 3 (F1 improved monotonically across all three epochs); training loss trajectory: epoch 1 → 0.043, epoch 2 → 0.021, epoch 3 → 0.014; validation F1 trajectory: epoch 1 → 0.9941, epoch 2 → 0.9954, epoch 3 → 0.9958; saved via `Trainer.save_model()` as safetensors; ~250 MB on disk

#### Activity: `ModelEvaluation`

- **name**: ModelEvaluation
- **task_count**: 1
- **started_at**: 2024-07-18T15:37:52Z
- **ended_at**: 2024-07-18T15:49:33Z
- **duration**: 11m 41s
- **status**: success: 1, error: 0
- **hosts**:
  - host: `phishing-gpu-01`, tasks: 1
    - gpu_usage: avg=64.8% (single-GPU inference, batch size 64)
    - gpu_memory_usage: avg=5.2 GB (FP16 inference)
    - cpu_usage: avg=8.4%
    - memory_usage: avg=14 GB
- **inputs**:
  - `cybersectony/phishing-email-detection-distilbert_v2.4.1` — best-checkpoint fine-tuned model loaded in FP16 for inference; `torch.no_grad()` context; softmax applied to logits for per-class probability output
  - Tokenised test split — 60,000 held-out examples (not seen during training or checkpoint selection); same tokenisation parameters as training: `max_length=512`, `truncation=True`, `padding="max_length"`
- **outputs**:
  - `evaluation_report` — per-class and aggregate metrics computed with `sklearn.metrics`:

    | Class | Precision | Recall | F1 |
    |---|---|---|---|
    | legitimate_email (0) | 0.9971 | 0.9963 | 0.9967 |
    | phishing_email (1)   | 0.9934 | 0.9921 | 0.9927 |
    | legitimate_url (2)   | 0.9964 | 0.9971 | 0.9967 |
    | phishing_url (3)     | 0.9953 | 0.9961 | 0.9957 |

    - Overall accuracy: **99.58%**
    - Micro-averaged F1: **99.579**
    - Micro-averaged Precision: **99.583**
    - Micro-averaged Recall: **99.58**
    - Inference throughput: ~2,800 samples/second at batch size 64 on RTX A6000 (FP16)

---

## 6. Significant Workflow Artifacts

### Input Artifacts

**Artifact: `distilbert/distilbert-base-uncased`**
- **identifier**: distilbert/distilbert-base-uncased
- **description**: A distilled, uncased version of BERT-base trained by HuggingFace on BookCorpus and English Wikipedia using knowledge distillation, masked language modelling, and cosine embedding loss. 67M parameters; 6 transformer layers; hidden size 768; 12 attention heads. 40% smaller and 60% faster than BERT-base while retaining ~97% of its GLUE performance. Uses WordPiece tokenisation with 30,522 vocabulary. Intended primarily for fine-tuning on downstream classification, token classification, or QA tasks. License: Apache-2.0.
- **reference**: https://huggingface.co/distilbert/distilbert-base-uncased
- **size**: ~250 MB (PyTorch bin / safetensors)
- **additional metadata**: architecture: DistilBertForMaskedLM (pretrain) / DistilBertForSequenceClassification (fine-tuned); num_hidden_layers: 6; hidden_size: 768; num_attention_heads: 12; intermediate_size: 3072; vocab_size: 30522; max_position_embeddings: 512; pretraining_data: [BookCorpus, English Wikipedia]; teacher_model: bert-base-uncased; license: Apache-2.0

**Artifact: `cybersectony/PhishingEmailDetectionv2.0`**
- **identifier**: cybersectony/PhishingEmailDetectionv2.0
- **description**: Multi-class phishing detection dataset combining 22,644 labelled email body texts and 177,356 labelled URLs across four classes: legitimate_email (0), phishing_email (1), legitimate_url (2), and phishing_url (3). Contains 200,000 total samples pre-split into train (120k), validation (20k), and test (60k). Each row contains the raw content string and an integer label. Intended for training sequence classifiers to identify phishing threats in mixed email/URL content streams.
- **reference**: https://huggingface.co/datasets/cybersectony/PhishingEmailDetectionv2.0
- **size**: ~67.2 MB (uncompressed arrow); ~40.3 MB (compressed download)
- **additional metadata**: num_samples_total: 200,000; email_samples: 22,644; url_samples: 177,356; num_classes: 4; label_map: {0: legitimate_email, 1: phishing_email, 2: legitimate_url, 3: phishing_url}; splits: {train: 120000, validation: 20000, test: 60000}; language: English; format: Parquet/Arrow; columns: [content (string), labels (int64)]

### Output Artifacts

**Artifact: `cybersectony/phishing-email-detection-distilbert_v2.4.1`**
- **identifier**: cybersectony/phishing-email-detection-distilbert_v2.4.1
- **description**: Fine-tuned DistilBERT-base-uncased model for four-class phishing content detection. Classifies input text (email body or URL string) into one of four categories: legitimate_email, phishing_email, legitimate_url, or phishing_url. Outputs per-class softmax probabilities, with the argmax used as the final prediction. Achieves 99.58% accuracy and 99.579 micro-F1 on the 60,000-sample test set. Intended for integration into email gateways, URL scanners, or content moderation pipelines. License: Apache-2.0.
- **reference**: https://huggingface.co/cybersectony/phishing-email-detection-distilbert_v2.4.1
- **size**: ~250 MB (safetensors)
- **additional metadata**: base_model: distilbert/distilbert-base-uncased; num_labels: 4; label_map: {0: legitimate_email, 1: phishing_email, 2: legitimate_url, 3: phishing_url}; training_epochs: 3; best_epoch: 3; train_loss_final: 0.014; val_f1_final: 0.9958; test_accuracy: 0.9958; test_f1_micro: 0.99579; test_precision_micro: 0.99583; test_recall_micro: 0.9958; inference_throughput: ~2800_samples/s_FP16_batch64; license: Apache-2.0
