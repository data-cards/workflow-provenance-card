# Provenance Card: Llama-3.2-3B PII Redactor Fine-tuning Workflow

## Card Metadata

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Card ID | **[R]** | `[manual]` | `PC-LLAMA-PII-20241027-003` |
| Card Creation Timestamp | **[R]** | `[manual]` | `2024-10-27T18:00:00Z` |
| Card Author | **[R]** | `[manual]` | `Provenance Card Generator v1.2` |
| Authoring Method | **[R]** | `[manual]` | `hybrid` |
| Source Provenance Document | **[R]** | `[manual]` | `https://internal.privacy-lab.ai/runs/pii-redactor-3b-qlora-441` |
| Card Contact | **[Rec]** | `[manual]` | `research-ops@ai4privacy.org` |

---

## 0. Provenance Capture Metadata

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Capture Tool | **[R]** | `[manual]` | `Weights & Biases (W&B) + PEFT Logger` |
| Capture Method | **[R]** | `[manual]` | `automatic instrumentation` |
| Provenance Format | **[R]** | `[manual]` | `W3C PROV-JSON` |
| Record ID | **[R]** | `[manual]` | `rec-pii-redact-200k-llama32` |
| Record Creation Timestamp | **[Rec]** | `[manual]` | `2024-10-27T17:50:00Z` |
| Coverage Level | **[Rec]** | `[manual]` | `activity-level` |
| Known Capture Gaps | **[Rec]** | `[manual]` | `Specific hardware temperature/throttling logs were not attached to the record.` |

---

## 1. Workflow Identification

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Workflow Execution ID | **[R]** | `[manual]` | `run-pii-redactor-qlora-20241027` |
| Workflow Name | **[R]** | `[manual]` | `Llama-3.2-3B PII Redactor QLoRA Fine-tuning` |
| Workflow Version | **[Rec]** | `[manual]` | `v1.2.0-redaction` |
| Execution Start Timestamp | **[R]** | `[manual]` | `2024-10-27T08:00:00Z` |
| Execution End Timestamp | **[Rec]** | `[manual]` | `2024-10-27T17:45:00Z` |
| Execution Duration | **[Rec]** | `[inferred]` | `9h 45m 00s` |
| Execution Status | **[R]** | `[manual]` | `Completed` |
| Execution Location | **[Rec]** | `[manual]` | `Private Cloud - Cluster-B (NVIDIA)` |

---

## 2. Execution Context

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Host OS | **[Rec]** | `[manual]` | `Debian 12` |
| Compute Hardware | **[Rec]** | `[manual]` | `2x NVIDIA RTX 4090 (24GB)` |
| Runtime Environment | **[Rec]** | `[manual]` | `Python 3.11 / CUDA 12.1` |
| Resource Manager | **[O]** | `[manual]` | `Docker Engine` |
| Primary Software | **[Rec]** | `[prov_doc]` | `Transformers, PEFT, BitsAndBytes` |
| Environment Snapshot | **[O]** | `[manual]` | `pip-freeze-pii-redactor.txt` |

---

## 3. Actors

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Execution Triggerer | **[R]** | `[manual]` | `ai4privacy-dev-01` |
| Lead Practitioner | **[Rec]** | `[manual]` | `AI4Privacy Team` |
| Hardware Provider | **[Rec]** | `[manual]` | `Internal Lab Resources` |
| Data Provider | **[Rec]** | `[prov_doc]` | `AI4Privacy Community / AISuisse SA` |
| Accountable Organization | **[R]** | `[manual]` | `AI4Privacy` |

---

## 4. Inputs

### Block [1]: base-model
| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Artifact Name | **[R]** | `[prov_doc]` | `meta-llama/Llama-3.2-3B-Instruct` |
| Artifact Type | **[R]** | `[manual]` | `Pretrained Large Language Model` |
| Version / Hash | **[Rec]** | `[manual]` | `sha256:llama32-3b-inst-ref` |
| Logical URI | **[R]** | `[prov_doc]` | `https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct` |
| License | **[Rec]** | `[prov_doc]` | `Llama 3.2 Community License` |
| Description | **[Rec]** | `[prov_doc]` | `Base instruction-tuned model used for text generation and processing.` |

### Block [2]: pii-dataset
| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Artifact Name | **[R]** | `[prov_doc]` | `ai4privacy/pii-masking-200k` |
| Artifact Type | **[R]** | `[manual]` | `Privacy Masking Dataset` |
| Version / Hash | **[Rec]** | `[manual]` | `sha256:pii200k-en-subset` |
| Logical URI | **[R]** | `[prov_doc]` | `https://huggingface.co/datasets/ai4privacy/pii-masking-200k` |
| License | **[Rec]** | `[prov_doc]` | `Apache-2.0` |
| Description | **[Rec]** | `[prov_doc]` | `Dataset with 54 PII classes and 200k samples (English subset used).` |

---

## 5. Execution Record

### Block [1]: qlora-finetuning
| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Activity Name | **[R]** | `[manual]` | `pii-redaction-training` |
| Activity Type | **[R]** | `[manual]` | `QLoRA Fine-tuning` |
| Start Timestamp | **[Rec]** | `[manual]` | `2024-10-27T08:10:00Z` |
| End Timestamp | **[Rec]** | `[manual]` | `2024-10-27T17:30:00Z` |
| Inputs Consumed | **[R]** | `[manual]` | `base-model, pii-dataset` |
| Outputs Produced | **[R]** | `[manual]` | `lora-adapter-weights` |
| Parameters | **[Rec]** | `[prov_doc]` | `Rank: 16, Alpha: 32, LR: 2e-4, 4-bit loading` |

---

## 6. Outputs

### Block [1]: lora-adapter-weights
| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Artifact Name | **[R]** | `[prov_doc]` | `Llama-3.2-3B PII Redactor (LoRA)` |
| Artifact Type | **[R]** | `[manual]` | `PEFT LoRA Adapter Weights` |
| Version / Hash | **[Rec]** | `[manual]` | `sha256:pii-redact-adapter-01` |
| Logical URI | **[R]** | `[manual]` | `https://huggingface.co/local/pii-redactor-adapter` |
| License | **[Rec]** | `[prov_doc]` | `Apache-2.0` |
| Content Summary | **[O]** | `[prov_doc]` | `Adapter weights for replacing PII with placeholders like [FIRSTNAME], [EMAIL].` |

---

## 8. Execution Quality

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Status | **[R]** | `[manual]` | `Success` |
| Success Criteria | **[R]** | `[manual]` | `Micro-F1 > 0.85 and 0.00 formatting errors on test set.` |
| Errors / Warnings | **[Rec]** | `[manual]` | `None` |
| Quality Metrics | **[Rec]** | `[prov_doc]` | `Exact Match: 0.67, Micro-F1: 0.90, Precision: 0.91, Recall: 0.90` |
| Validation Method | **[Rec]** | `[prov_doc]` | `Evaluated on 300 random test samples using strict span matching.` |

---

## 9. Provenance Record Quality

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Capture Completeness | **[R]** | `[manual]` | `0.94 (High)` |
| Unlogged Activities | **[Rec]** | `[manual]` | `The script used to extract the English-only subset from the 200k dataset was not logged.` |
| Unlogged Inputs / Outputs | **[Rec]** | `[manual]` | `Temporary weight shards during gradient accumulation were not recorded.` |
| Reproducibility | **[Rec]** | `[manual]` | `Reproducible using the provided LoRA hyperparameters and specific dataset version.` |

---

## Coverage Statistics

| Section | Total Fields | Filled | Missing | Fill % |
|---------|-------------|--------|---------|--------|
| Card Metadata | 8 | 6 | 2 | 75% |
| §0 Provenance Capture Metadata | 8 | 7 | 1 | 87.5% |
| §1 Workflow Identification | 8 | 8 | 0 | 100% |
| §2 Execution Context | 7 | 6 | 1 | 85.7% |
| §3 Actors | 6 | 5 | 1 | 83.3% |
| §4 Inputs (6 fields × 2 blocks) | 12 | 12 | 0 | 100% |
| §5 Execution Record (7 fields × 1 block) | 7 | 7 | 0 | 100% |
| §6 Outputs (7 fields × 1 block) | 7 | 6 | 1 | 85.7% |
| §8 Execution Quality | 6 | 5 | 1 | 83.3% |
| §9 Provenance Record Quality | 4 | 4 | 0 | 100% |