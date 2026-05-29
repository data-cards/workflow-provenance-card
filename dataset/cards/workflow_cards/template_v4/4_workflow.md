# Provenance Card: openNemo-Cascade-2-30B-A3B Fine-tuning Workflow

## Card Metadata

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Card ID | **[R]** | `[manual]` | `PC-NEMOTRON-OPEN-20260320-004` |
| Card Creation Timestamp | **[R]** | `[manual]` | `2026-03-20T10:00:00Z` |
| Card Author | **[R]** | `[manual]` | `Provenance Card Generator v1.2` |
| Authoring Method | **[R]** | `[manual]` | `hybrid` |
| Source Provenance Document | **[R]** | `[manual]` | `https://empero.org/provenance/open-nemo-cascade-run-01` |
| Card Contact | **[Rec]** | `[manual]` | `engineering@empero.org` |

---

## 0. Provenance Capture Metadata

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Capture Tool | **[R]** | `[manual]` | `PyTorch Execution Tracker v3.1` |
| Capture Method | **[R]** | `[manual]` | `automatic instrumentation` |
| Provenance Format | **[R]** | `[manual]` | `W3C PROV-JSON` |
| Record ID | **[R]** | `[manual]` | `rec-empero-nemotron-hybrid-ft` |
| Record Creation Timestamp | **[Rec]** | `[manual]` | `2026-03-20T09:45:00Z` |
| Coverage Level | **[Rec]** | `[manual]` | `activity-level` |
| Known Capture Gaps | **[Rec]** | `[manual]` | `Custom modeling code integration (modeling_nemotron_h.py) was manually linked.` |

---

## 1. Workflow Identification

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Workflow Execution ID | **[R]** | `[manual]` | `run-20260319-opennemo-cascade` |
| Workflow Name | **[R]** | `[manual]` | `Nemotron-Cascade-2 Pure-PyTorch Adaptation & Fine-tuning` |
| Workflow Version | **[Rec]** | `[manual]` | `v2.0.0-cascaderl` |
| Execution Start Timestamp | **[R]** | `[manual]` | `2026-03-19T06:00:00Z` |
| Execution End Timestamp | **[Rec]** | `[manual]` | `2026-03-20T02:00:00Z` |
| Execution Duration | **[Rec]** | `[inferred]` | `20h 00m 00s` |
| Execution Status | **[R]** | `[manual]` | `Completed` |
| Execution Location | **[Rec]** | `[manual]` | `Empero Cloud Cluster - Region 1` |

---

## 2. Execution Context

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Host OS | **[Rec]** | `[manual]` | `Ubuntu 24.04 LTS` |
| Compute Hardware | **[Rec]** | `[manual]` | `4x NVIDIA RTX 4090 (Consumer GPU Target)` |
| Runtime Environment | **[Rec]** | `[manual]` | `Docker: open-nemo-pytorch-2.5` |
| Resource Manager | **[O]** | `[manual]` | `Kubernetes` |
| Primary Software | **[Rec]** | `[prov_doc]` | `bitsandbytes (4-bit), peft (QLoRA), torch 2.5` |
| Environment Snapshot | **[O]** | `[manual]` | `requirements_empero_cascade.txt` |

---

## 3. Actors

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Execution Triggerer | **[R]** | `[manual]` | `empero-build-system` |
| Lead Practitioner | **[Rec]** | `[prov_doc]` | `Empero AI Team` |
| Hardware Provider | **[Rec]** | `[manual]` | `Empero AI Infrastructure` |
| Data Provider | **[Rec]** | `[prov_doc]` | `NVIDIA Corporation` |
| Accountable Organization | **[R]** | `[manual]` | `Empero AI` |

---

## 4. Inputs

### Block [1]: base-weights
| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Artifact Name | **[R]** | `[prov_doc]` | `nvidia/Nemotron-Cascade-2-30B-A3B` |
| Artifact Type | **[R]** | `[manual]` | `Pretrained Hybrid Model (Mamba2/MoE/Attention)` |
| Version / Hash | **[Rec]** | `[manual]` | `sha256:nv-casc2-30b-ref` |
| Logical URI | **[R]** | `[prov_doc]` | `https://huggingface.co/nvidia/Nemotron-Cascade-2-30B-A3B` |
| License | **[Rec]** | `[prov_doc]` | `NVIDIA Open Model License` |
| Description | **[Rec]** | `[prov_doc]` | `Foundational hybrid model with 30B total / 3B active parameters.` |

### Block [2]: rl-dataset
| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Artifact Name | **[R]** | `[prov_doc]` | `nvidia/Nemotron-Cascade-2-RL-data` |
| Artifact Type | **[R]** | `[manual]` | `RL Training Mixture` |
| Version / Hash | **[Rec]** | `[manual]` | `sha256:nv-rl-blend-2026` |
| Logical URI | **[R]** | `[prov_doc]` | `https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-RL-data` |
| License | **[Rec]** | `[prov_doc]` | `ODC-By` |
| Description | **[Rec]** | `[prov_doc]` | `Curated blend including IF-RL, Multi-domain-RL, and SWE-RL.` |

---

## 5. Execution Record

### Block [1]: qlora-adaptation
| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Activity Name | **[R]** | `[manual]` | `pytorch-native-qlora-adaptation` |
| Activity Type | **[R]** | `[manual]` | `4-bit Quantization & QLoRA Fine-tuning` |
| Start Timestamp | **[Rec]** | `[manual]` | `2026-03-19T06:30:00Z` |
| End Timestamp | **[Rec]** | `[manual]` | `2026-03-20T01:30:00Z` |
| Inputs Consumed | **[R]** | `[manual]` | `base-weights, rl-dataset` |
| Outputs Produced | **[R]** | `[manual]` | `openNemo-weights-bin` |
| Parameters | **[Rec]** | `[manual]` | `batch: 64, len: 256k, precision: 4-bit, dropout: 0.05` |

---

## 6. Outputs

### Block [1]: openNemo-weights-bin
| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Artifact Name | **[R]** | `[prov_doc]` | `openNemo-Cascade-2-30B-A3B` |
| Artifact Type | **[R]** | `[manual]` | `Fine-tuned Hybrid Model (Pure PyTorch)` |
| Version / Hash | **[Rec]** | `[manual]` | `sha256:empero-nemo-v1` |
| Logical URI | **[R]** | `[manual]` | `https://huggingface.co/empero/openNemo-Cascade-2-30B-A3B` |
| License | **[Rec]** | `[prov_doc]` | `NVIDIA Open Model License` |
| Content Summary | **[O]** | `[prov_doc]` | `Drop-in replacement weights for Nemotron-Cascade-2 using native PyTorch ops.` |

---

## 8. Execution Quality

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Status | **[R]** | `[manual]` | `Success` |
| Success Criteria | **[R]** | `[manual]` | `Loss parity with original NVIDIA training logs; successful 4-bit loading.` |
| Errors / Warnings | **[Rec]** | `[manual]` | `None; external CUDA kernels successfully bypassed.` |
| Quality Metrics | **[Rec]** | `[manual]` | `Training Loss: ~1.2 (final); Perplexity: Consistent with base model.` |
| Validation Method | **[Rec]** | `[manual]` | `Tested on internal reasoning and coding benchmarks.` |

---

## 9. Provenance Record Quality

| Field | Ann. | Source | Value |
|-------|------|--------|-------|
| Capture Completeness | **[R]** | `[manual]` | `0.96 (High)` |
| Unlogged Activities | **[Rec]** | `[manual]` | `Creation of the openNemo.jpg promotional asset was not part of the workflow.` |
| Unlogged Inputs / Outputs | **[Rec]** | `[manual]` | `Intermediate Optimizer states (AdamW) were not persisted to the final card.` |
| Reproducibility | **[Rec]** | `[manual]` | `Fully reproducible on consumer hardware using bitsandbytes and the provided modelling code.` |

---

## Coverage Statistics

| Section | Total Fields | Filled | Missing | Fill % |
|---------|-------------|--------|---------|--------|
| Card Metadata | 6 | 6 | 0 | 100% |
| §0 Provenance Capture Metadata | 8 | 8 | 0 | 100% |
| §1 Workflow Identification | 8 | 8 | 0 | 100% |
| §2 Execution Context | 7 | 6 | 1 | 85.7% |
| §3 Actors | 6 | 5 | 1 | 83.3% |
| §4 Inputs (6 fields × 2 blocks) | 12 | 12 | 0 | 100% |
| §5 Execution Record (7 fields × 1 block) | 7 | 7 | 0 | 100% |
| §6 Outputs (7 fields × 1 block) | 7 | 6 | 1 | 85.7% |
| §8 Execution Quality | 6 | 5 | 1 | 83.3% |
| §9 Provenance Record Quality | 4 | 4 | 0 | 100% |