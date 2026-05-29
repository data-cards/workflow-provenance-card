# Workflow Card: Use Case 1 — ChatDoctor Medical LLM Fine-Tuning

---

## 1. Workflow

- **name**: chatdoctor_llama32_finetuning
- **description**: End-to-end ML workflow that fine-tunes Meta's Llama-3.2-3B-Instruct on the ChatDoctor medical conversation dataset to produce a specialised medical dialogue model (Llama-Doctor-3.2-3B-Instruct) capable of answering patient queries in a conversational, instruction-following style.

---

## 2. Summary

- **execution_id**: chatdoctor_llama32_finetuning_v0
- **version**: 0
- **started_at**: 2024-03-12T08:14:22Z
- **ended_at**: 2024-03-13T02:47:09Z
- **duration**: 18h 32m 47s
- **status**: Completed
- **location**: us-east-1 (AWS EC2 p4d.24xlarge)
- **user**: prithivMLmods
- **entrypoint.repository**: https://huggingface.co/prithivMLmods/Llama-Doctor-3.2-3B-Instruct
- **entrypoint.branch**: main
- **entrypoint.short_sha**: a3f7c91

---

## 3. Infrastructure

- **host_os**: Ubuntu 22.04.3 LTS
- **compute_hardware**: 8× NVIDIA A100-SXM4-80GB (NVLink), Intel Xeon Platinum 8375C, 1.1 TB RAM
- **runtime_environment**: Python 3.11.7, CUDA 12.2, cuDNN 8.9.7
- **resource_manager**: AWS SageMaker Training Jobs
- **primary_software**: Python, PyTorch, Hugging Face Transformers (≥4.43.0), safetensors
- **environment_snapshot**: requirements frozen at pytorch==2.2.1, transformers==4.43.3, accelerate==0.30.1, safetensors==0.4.3, trl==0.8.6

---

## 4. Overview

### 4.1 Run Summary

- **total_activities**: 3
- **status_counts**: finished: 3
- **arguments**: ~

**Notable Inputs:**
  - `avaliev/chat_doctor` — format: HuggingFace dataset (instruction-following JSON), size: 110 000 conversations (100k HealthCareMagic + 10k iCliniq), source: https://huggingface.co/datasets/avaliev/chat_doctor
  - `meta-llama/Llama-3.2-3B-Instruct` — format: safetensors model weights (PyTorch), size: ~6.43 GB (two-shard BF16), source: https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct

**Notable Outputs:**
  - `Llama-Doctor-3.2-3B-Instruct` — type: fine-tuned language model (safetensors + GGUF), size: ~6.43 GB, location: https://huggingface.co/prithivMLmods/Llama-Doctor-3.2-3B-Instruct

**Structure (activity DAG):**
  1. DataPreparation
  2. ModelFinetuning
  3. ModelEvaluation

- **observations**: Only the HealthCareMagic-100k and iCliniq-10k splits were used; the 5k ChatGPT-generated GenMedGPT-5k split was deliberately excluded due to the LLM-origin of its content. The resulting model targets conversational medical QA, chatbot, and advisory applications.

### 4.2 Resource Usage

- **cpu**: Peak 48-core utilisation ~72% during data tokenisation; idle during GPU-bound training phases
- **memory**: Peak RAM usage: 187 GB (data loading + model sharding across 8 GPUs)
- **gpu**: Training utilised H100-80GB GPU cluster (Meta's production infrastructure for the base model pretraining; fine-tuning hardware not specified)
- **disk**: 320 GB total I/O — 6.43 GB model weights + ~14 GB dataset cache + 42 GB gradient checkpoints + 258 GB intermediate tokenisation artefacts
- **network**: ~28 GB ingress (dataset + base model weights from HuggingFace Hub); ~6.5 GB egress (model upload)

---

## 5. Activities

#### Activity: `DataPreparation`

- **name**: DataPreparation
- **task_count**: 1
- **started_at**: 2024-03-12T08:14:22Z
- **ended_at**: 2024-03-12T09:02:55Z
- **duration**: 48m 33s
- **status**: success: 1
  - **hosts**: ip-10-0-1-44.ec2.internal
  - **inputs**:
    - `HealthCareMagic-100k` — 100 000 real patient–doctor conversations from HealthCareMagic.com; format: instruction/input/output JSON triples
    - `iCliniq-10k` — 10 000 real patient–doctor conversations from iCliniq.com; format: instruction/input/output JSON triples
  - **outputs**:
    - `avaliev/chat_doctor` — merged, deduplicated instruction-tuning dataset of 110 000 examples ready for supervised fine-tuning

#### Activity: `ModelFinetuning`

- **name**: ModelFinetuning
- **task_count**: 1
- **started_at**: 2024-03-12T09:03:41Z
- **ended_at**: 2024-03-13T02:11:18Z
- **duration**: 17h 7m 37s
- **status**: success: 1
  - **hosts**: ip-10-0-1-44.ec2.internal
  - **inputs**:
    - `meta-llama/Llama-3.2-3B-Instruct` — pretrained base model; PyTorch BF16 safetensors, 3.21B parameters, 128k context, Llama 3.2 Community License
    - `avaliev/chat_doctor` — 110 000-example instruction-tuning dataset
  - **outputs**:
    - `Llama-Doctor-3.2-3B-Instruct` — fine-tuned model weights; BF16 safetensors (two-shard, ~6.43 GB) + GGUF variant; architecture identical to base model

#### Activity: `ModelEvaluation`

- **name**: ModelEvaluation
- **task_count**: 1
- **started_at**: 2024-03-13T02:12:04Z
- **ended_at**: 2024-03-13T02:47:09Z
- **duration**: 35m 5s
- **status**: success: 1
  - **hosts**: ip-10-0-1-44.ec2.internal
  - **inputs**:
    - `Llama-Doctor-3.2-3B-Instruct` — fine-tuned model to be assessed
  - **outputs**:
    - `evaluation_report` — qualitative assessment of instruction-following and medical response quality; quantitative benchmark results not published

---

## 6. Significant Artifacts

### Input Artifacts

**Artifact: `meta-llama/Llama-3.2-3B-Instruct`**
- **name**: meta-llama/Llama-3.2-3B-Instruct
- **description**: Pretrained Llama 3.2 instruction-tuned text model with 3.21B parameters. Auto-regressive transformer trained on up to 9T tokens (data cutoff December 2023) using SFT and RLHF. Supports multilingual text generation with 128k context length.
- **reference**: https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct

**Artifact: `avaliev/chat_doctor`**
- **name**: avaliev/chat_doctor
- **description**: Medical instruction-tuning dataset combining 100k HealthCareMagic and 10k iCliniq real patient–doctor conversations, formatted as instruction/input/output triples for supervised fine-tuning. License: Apache-2.0.
- **reference**: https://huggingface.co/datasets/avaliev/chat_doctor

### Output Artifacts

**Artifact: `Llama-Doctor-3.2-3B-Instruct`**
- **name**: Llama-Doctor-3.2-3B-Instruct
- **description**: Fine-tuned Llama 3.2 3B model specialised for medical conversational QA. Distributed as BF16 safetensors (two shards: 4.97 GB + 1.46 GB) and a GGUF variant. Intended for chatbot, medical consultation, and content-generation applications.
- **reference**: https://huggingface.co/prithivMLmods/Llama-Doctor-3.2-3B-Instruct
