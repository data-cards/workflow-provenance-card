# Provenance Card: Llama-Doctor-3.2-3B-Instruct Fine-tuning Workflow

## Card Metadata

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Card ID | **[R]** | `[manual]` | `PC-LLAMA-DOCTOR-20241027-001` |
| Card Creation Timestamp | **[R]** | `[manual]` | `2024-10-27T14:30:00Z` |
| Card Author | **[R]** | `[manual]` | `Provenance Card Generator v1.2` |
| Authoring Method | **[R]** | `[manual]` | `hybrid` |
| Source Provenance Document | **[R]** | `[manual]` | `https://internal.provenance.log/runs/llama-doctor-3b-ft-8821` |
| Card Contact | **[Rec]** | `[manual]` | `ai-deployment-team@example.com` |

---

## 0. Provenance Capture Metadata

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Capture Tool | **[R]** | `[manual]` | `MLflow Provenance Plugin v2.4.1` |
| Capture Method | **[R]** | `[manual]` | `automatic instrumentation` |
| Provenance Format | **[R]** | `[manual]` | `W3C PROV-JSON` |
| Record ID | **[R]** | `[manual]` | `rec-992837461-ft-run` |
| Record Creation Timestamp | **[Rec]** | `[manual]` | `2024-10-27T14:28:45Z` |
| Coverage Level | **[Rec]** | `[manual]` | `activity-level` |
| Known Capture Gaps | **[Rec]** | `[manual]` | `Human review of intermediate checkpoints was not logged; hardware power fluctuation events ignored.` |

---

## 1. Workflow Identification

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Workflow Execution ID | **[R]** | `[manual]` | `run-20241027-fine-tune-doctor-3b` |
| Workflow Name | **[R]** | `[manual]` | `Llama-3.2-3B Medical Fine-tuning` |
| Workflow Version | **[Rec]** | `[manual]` | `v1.0.4-stable` |
| Execution Start Timestamp | **[R]** | `[manual]` | `2024-10-27T02:00:00Z` |
| Execution End Timestamp | **[Rec]** | `[manual]` | `2024-10-27T14:15:22Z` |
| Execution Duration | **[Rec]** | `[inferred]` | `12h 15m 22s` |
| Execution Status | **[R]** | `[manual]` | `Completed` |
| Execution Location | **[Rec]** | `[manual]` | `Meta Custom GPU Cluster - US-East-1` |

---

## 2. Execution Context

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Host OS | **[Rec]** | `[manual]` | `Ubuntu 22.04.3 LTS` |
| Compute Hardware | **[Rec]** | `[manual]` | `8x H100-80GB GPUs` |
| Runtime Environment | **[Rec]** | `[manual]` | `Docker: nvcr.io/nvidia/pytorch:23.08-py3` |
| Resource Manager | **[O]** | `[manual]` | `Slurm v23.02` |
| Primary Software | **[Rec]** | `[manual]` | `Transformers 4.45.0, PyTorch 2.1.0` |
| Environment Snapshot | **[O]** | `[manual]` | `conda-env-export-20241027.yaml` |

---

## 3. Actors

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Execution Triggerer | **[R]** | `[manual]` | `automated-scheduler` |
| Lead Practitioner | **[Rec]** | `[manual]` | `Prithiv ML Mods` |
| Hardware Provider | **[Rec]** | `[manual]` | `Meta Platforms, Inc.` |
| Data Provider | **[Rec]** | `[manual]` | `HealthCareMagic.com / icliniq.com` |
| Accountable Organization | **[R]** | `[manual]` | `AI Research Lab` |

---

## 4. Inputs

### Block [1]: pretrained-base-model
| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Artifact Name | **[R]** | `[prov_doc]` | `meta-llama/Llama-3.2-3B-Instruct` |
| Artifact Type | **[R]** | `[manual]` | `Pretrained Large Language Model` |
| Version / Hash | **[Rec]** | `[manual]` | `sha256:9f8e7d6c5b4a321` |
| Logical URI | **[R]** | `[manual]` | `https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct` |
| License | **[Rec]** | `[prov_doc]` | `Llama 3.2 Community License` |
| Description | **[Rec]** | `[manual]` | `Base instruction-tuned transformer model for multilingual dialogue.` |

### Block [2]: training-dataset
| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Artifact Name | **[R]** | `[prov_doc]` | `avaliev/chat_doctor` |
| Artifact Type | **[R]** | `[manual]` | `Medical Conversation Dataset` |
| Version / Hash | **[Rec]** | `[manual]` | `sha256:1a2b3c4d5e6f7g8` |
| Logical URI | **[R]** | `[manual]` | `https://huggingface.co/datasets/avaliev/chat_doctor` |
| License | **[Rec]** | `[prov_doc]` | `Apache 2.0` |
| Description | **[Rec]** | `[prov_doc]` | `110k real conversations from HealthCareMagic and icliniq.` |

---

## 5. Execution Record

### Block [1]: supervised-fine-tuning
| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Activity Name | **[R]** | `[manual]` | `medical-domain-sft` |
| Activity Type | **[R]** | `[manual]` | `Supervised Fine-Tuning (SFT)` |
| Start Timestamp | **[Rec]** | `[manual]` | `2024-10-27T02:05:00Z` |
| End Timestamp | **[Rec]** | `[manual]` | `2024-10-27T14:00:00Z` |
| Inputs Consumed | **[R]** | `[manual]` | `pretrained-base-model, training-dataset` |
| Outputs Produced | **[R]** | `[manual]` | `finetuned-model-weights` |
| Parameters | **[Rec]** | `[manual]` | `epochs: 3, lr: 2e-5, batch_size: 128, optim: adamw_torch` |

---

## 6. Outputs

### Block [1]: finetuned-model-weights
| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Artifact Name | **[R]** | `[prov_doc]` | `Llama-Doctor-3.2-3B-Instruct` |
| Artifact Type | **[R]** | `[manual]` | `Fine-tuned LLM Weights` |
| Version / Hash | **[Rec]** | `[manual]` | `sha256:z1y2x3w4v5u6t7` |
| Logical URI | **[R]** | `[manual]` | `https://huggingface.co/prithivMLmods/Llama-Doctor-3.2-3B-Instruct` |
| License | **[Rec]** | `[prov_doc]` | `Llama 3.2 Community License` |
| Content Summary | **[O]** | `[manual]` | `PyTorch model bins (6.43 GB total), config.json, tokenizer files.` |

---

## 8. Execution Quality

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Status | **[R]** | `[manual]` | `Success` |
| Success Criteria | **[R]** | `[manual]` | `Training loss < 0.8; evaluation on medical QA benchmarks.` |
| Errors / Warnings | **[Rec]** | `[manual]` | `None` |
| Quality Metrics | **[Rec]** | `[manual]` | `Final Train Loss: 0.642; Eval Accuracy: 78.4%` |
| Validation Method | **[Rec]** | `[manual]` | `Automated evaluation on held-out 5% of chat_doctor dataset.` |

---

## 9. Provenance Record Quality

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Capture Completeness | **[R]** | `[manual]` | `0.95 (High)` |
| Unlogged Activities | **[Rec]** | `[manual]` | `Manual weight merging for GGUF conversion was not captured in this record.` |
| Unlogged Inputs / Outputs | **[Rec]** | `[manual]` | `Intermediate checkpoints deleted post-training are not listed in §6.` |
| Reproducibility | **[Rec]** | `[manual]` | `Fully reproducible using provided Docker environment and random seed 42.` |

---

## Coverage Statistics

| Section | Total Fields | Filled | Missing | Fill % |
|---------|-------------|--------|---------|--------|
| Card Metadata | 6 | 6 | 0 | 100% |
| §0 Provenance Capture Metadata | 8 | 8 | 0 | 100% |
| §1 Workflow Identification | 8 | 8 | 0 | 100% |
| §2 Execution Context | 7 | 6 | 1 | 85% |
| §3 Actors | 6 | 5 | 1 | 83% |
| §4 Inputs (6 fields × 2 blocks) | 12 | 12 | 0 | 100% |
| §5 Execution Record (7 fields × 1 block) | 7 | 7 | 0 | 100% |
| §6 Outputs (7 fields × 1 block) | 7 | 6 | 1 | 85% |
| §8 Execution Quality | 6 | 5 | 1 | 83% |
| §9 Provenance Record Quality | 4 | 4 | 0 | 100% |