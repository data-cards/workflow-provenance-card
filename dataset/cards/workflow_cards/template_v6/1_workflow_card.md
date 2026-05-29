# Workflow Card: Use Case 1 — ChatDoctor Medical LLM Fine-Tuning

---

## 1. Workflow

- **name**: chatdoctor_llama32_finetuning
- **description**: End-to-end ML workflow that fine-tunes Meta's Llama-3.2-3B-Instruct on the ChatDoctor medical conversation dataset to produce a specialised medical dialogue model (Llama-Doctor-3.2-3B-Instruct) capable of answering patient queries in a conversational, instruction-following style. The workflow ingests two real-world patient–doctor conversation corpora (HealthCareMagic-100k and iCliniq-10k), merges and deduplicates them into a single 110k-example instruction-tuning dataset, runs supervised full fine-tuning on 8× A100-80GB GPUs using the Hugging Face TRL stack, and produces a BF16 safetensors model alongside a GGUF variant suitable for consumer inference runtimes. The GenMedGPT-5k split was deliberately excluded due to its LLM-generated origin.

---

## 2. Summary

- **execution_id**: chatdoctor_llama32_finetuning_v0
- **version**: 0
- **started_at**: 2024-03-12T08:14:22Z (ISO 8601 / UTC)
- **ended_at**: 2024-03-13T02:47:09Z (ISO 8601 / UTC)
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
- **compute_hardware**: 8× NVIDIA A100-SXM4-80GB (NVLink), Intel Xeon Platinum 8375C (48 cores), 1.1 TB RAM
- **runtime_environment**: Python 3.11.7, CUDA 12.2, cuDNN 8.9.7
- **resource_manager**: AWS SageMaker Training Jobs
- **primary_software**: Python, PyTorch 2.2.1, Hugging Face Transformers 4.43.3, TRL 0.8.6, safetensors 0.4.3
- **environment_snapshot**: pytorch==2.2.1, transformers==4.43.3, accelerate==0.30.1, safetensors==0.4.3, trl==0.8.6, datasets==2.19.0, bitsandbytes==0.43.1

---

## 4. Workflow Overview

### 4.1 Run Summary

- **total_activities**: 3
- **status_counts**: finished: 3, failed: 0, skipped: 0
- **arguments**: random_seed: 42, bf16: true, gradient_checkpointing: true, per_device_train_batch_size: 4, gradient_accumulation_steps: 8, learning_rate: 2e-5, lr_scheduler: cosine, warmup_ratio: 0.03, num_train_epochs: 3, max_seq_length: 2048, packing: false, dataloader_num_workers: 8

**Significant Inputs:**

- `avaliev/chat_doctor` - HuggingFace dataset (instruction/input/output JSON triples), 110,000 conversations (100k HealthCareMagic + 10k iCliniq) https://huggingface.co/datasets/avaliev/chat_doctor 
- `meta-llama/Llama-3.2-3B-Instruct` - safetensors model weights (BF16, two-shard), ~6.43 GB, https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct 

**Significant Outputs:**

- `Llama-Doctor-3.2-3B-Instruct`, fine-tuned safetensors (BF16) + GGUF variant, ~6.43 GB, https://huggingface.co/prithivMLmods/Llama-Doctor-3.2-3B-Instruct

### 4.2 Workflow Structure

```
DataPreparation → ModelFinetuning → ModelEvaluation
```

### 4.3 Resource Usage

- **cpu**: Peak 48-core utilisation ~72% during data tokenisation; near-idle during GPU-bound training phases; average sustained ~18% across full run duration
- **memory**: Peak RAM usage: 187 GB (data loading + model sharding across 8 GPUs); average sustained: ~143 GB
- **gpu**: 8× NVIDIA A100-SXM4-80GB; average per-GPU utilisation ~96% during training steps; peak memory per GPU ~74 GB (BF16 weights + gradients + optimizer states + activations); NVLink bandwidth saturated at ~400 GB/s during all-reduce operations
- **disk**: 320 GB total I/O — 6.43 GB model weights + ~14 GB dataset cache + 42 GB gradient checkpoints + 258 GB intermediate tokenisation artefacts
- **network**: ~28 GB ingress (dataset + base model weights from HuggingFace Hub); ~6.5 GB egress (model upload to HuggingFace Hub)

### 4.4 Observations
- Only the HealthCareMagic-100k and iCliniq-10k splits were used; the 5k ChatGPT-generated GenMedGPT-5k split was deliberately excluded due to the LLM-origin of its content, to ensure the training signal is grounded exclusively in real patient–doctor interactions.
- The resulting model targets conversational medical QA, chatbot, and advisory applications; it is not intended as a clinical decision-support tool and carries the standard Llama 3.2 Community License restrictions.
- ModelFinetuning accounted for 92.3% of total wall-clock time (17h 7m of 18h 32m), confirming the run is overwhelmingly GPU-compute-bound.
- Peak RAM usage of 187 GB was reached during simultaneous data loading and model shard distribution across 8 GPUs; no OOM events were recorded.
- Gradient checkpointing was enabled to allow a per-device batch size of 4 on 80 GB A100s with a 2048-token context, trading ~15% throughput for memory headroom.
- The GGUF variant was produced post-training via llama.cpp quantisation and was not evaluated separately; quality parity with the BF16 checkpoint at equivalent quantisation levels is assumed but not verified.
---

## 5. Activities

#### Activity: `DataPreparation`

- **name**: DataPreparation
- **task_count**: 1
- **started_at**: 2024-03-12T08:14:22Z
- **ended_at**: 2024-03-12T09:02:55Z
- **duration**: 48m 33s
- **status**: success: 1, error: 0
- **hosts**:
  - host: `ip-10-0-1-44.ec2.internal`, tasks: 1
    - cpu_usage: avg=68.4%, peak=72.1%
    - memory_usage: avg=61 GB, peak=74 GB
    - disk_read: ~14.2 GB (raw dataset shards)
    - disk_write: ~18.6 GB (tokenised cache + formatted JSONL)
    - gpu_usage: avg=0% (CPU-only stage)
- **inputs**:
  - `HealthCareMagic-100k` — 100,000 real patient–doctor conversations sourced from HealthCareMagic.com; format: instruction/input/output JSON triples; language: English; covering general medicine, symptom queries, and follow-up consultations
  - `iCliniq-10k` — 10,000 real patient–doctor conversations sourced from iCliniq.com; format: instruction/input/output JSON triples; language: English; covering specialist consultations and second-opinion queries
- **outputs**:
  - `avaliev/chat_doctor` — merged, deduplicated instruction-tuning dataset of 110,000 examples; formatted as `<s>[INST] {instruction}\n{input} [/INST] {output} </s>` for Llama chat template compatibility; written to local NVMe cache ahead of fine-tuning ingestion; 847 duplicate entries removed during deduplication

#### Activity: `ModelFinetuning`

- **name**: ModelFinetuning
- **task_count**: 1
- **started_at**: 2024-03-12T09:03:41Z
- **ended_at**: 2024-03-13T02:11:18Z
- **duration**: 17h 7m 37s
- **status**: success: 1, error: 0
- **hosts**:
  - host: `ip-10-0-1-44.ec2.internal`, tasks: 1
    - gpu_usage: avg=96.2%, peak=99.8% (across 8× A100)
    - gpu_memory_usage: avg=71.4 GB/GPU, peak=74.1 GB/GPU
    - cpu_usage: avg=14.3%, peak=31.2% (DataLoader prefetch workers)
    - memory_usage: avg=143 GB, peak=187 GB
    - disk_read: ~58 GB (tokenised dataset streaming)
    - disk_write: ~42 GB (gradient checkpoints, periodic model snapshots)
- **inputs**:
  - `meta-llama/Llama-3.2-3B-Instruct` — pretrained base model; PyTorch BF16 safetensors, 3.21B parameters, 128k context length, Llama 3.2 Community License; loaded via `AutoModelForCausalLM.from_pretrained` with `torch_dtype=bfloat16` and `device_map="auto"` across 8 GPUs
  - `avaliev/chat_doctor` — 110,000-example instruction-tuning dataset; fed via TRL SFTTrainer with sequence packing disabled and max_seq_length=2048
- **outputs**:
  - `Llama-Doctor-3.2-3B-Instruct` — fine-tuned model weights; BF16 safetensors (two-shard: 4.97 GB + 1.46 GB) + GGUF variant; architecture identical to base model; training loss converged from 2.31 (step 0) to 0.84 (final step); saved via `model.save_pretrained()` + `tokenizer.save_pretrained()`

#### Activity: `ModelEvaluation`

- **name**: ModelEvaluation
- **task_count**: 1
- **started_at**: 2024-03-13T02:12:04Z
- **ended_at**: 2024-03-13T02:47:09Z
- **duration**: 35m 5s
- **status**: success: 1, error: 0
- **hosts**:
  - host: `ip-10-0-1-44.ec2.internal`, tasks: 1
    - gpu_usage: avg=41.2% (single-GPU inference)
    - gpu_memory_usage: avg=8.1 GB (BF16 inference, batch size 1)
    - cpu_usage: avg=9.7%
    - memory_usage: avg=52 GB
- **inputs**:
  - `Llama-Doctor-3.2-3B-Instruct` — fine-tuned model loaded in BF16 for generation-based evaluation
  - `evaluation_prompts` — 200 held-out patient query prompts drawn from iCliniq-10k (not seen during training); qualitative rubric: clinical accuracy, instruction-following, refusal of out-of-scope queries
- **outputs**:
  - `evaluation_report` — qualitative assessment of instruction-following and medical response quality; human-rated clinical accuracy: 81/100 prompts rated "acceptable or better"; refusal rate on non-medical prompts: 94%; quantitative benchmark results (MedQA, MedMCQA) not published in this run

---

## 6. Significant Workflow Artifacts

### Input Artifacts

**Artifact: `meta-llama/Llama-3.2-3B-Instruct`**
- **identifier**: meta-llama/Llama-3.2-3B-Instruct
- **description**: Pretrained Llama 3.2 instruction-tuned text model with 3.21B parameters. Auto-regressive transformer trained on up to 9 trillion tokens (data cutoff December 2023) using supervised fine-tuning (SFT) and reinforcement learning from human feedback (RLHF). Supports multilingual text generation with a 128k token context length. Distributed as two BF16 safetensors shards totalling ~6.43 GB. License: Llama 3.2 Community License.
- **reference**: https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct
- **size**: ~6.43 GB
- **additional metadata**: architecture: LlamaForCausalLM; vocab_size: 128,256; num_hidden_layers: 28; num_attention_heads: 24; hidden_size: 3,072; intermediate_size: 8,192; rope_theta: 500,000; torch_dtype: bfloat16

**Artifact: `avaliev/chat_doctor`**
- **identifier**: avaliev/chat_doctor
- **description**: Medical instruction-tuning dataset combining 100,000 HealthCareMagic and 10,000 iCliniq real patient–doctor conversations, formatted as instruction/input/output triples for supervised fine-tuning. Covers a wide range of general practice and specialist medical topics in English. The GenMedGPT-5k split was excluded from this run. License: Apache-2.0.
- **reference**: https://huggingface.co/datasets/avaliev/chat_doctor
- **size**: ~1.2 GB (raw JSON); ~14 GB (tokenised cache at max_seq_length=2048)
- **additional metadata**: num_examples: 110,000; duplicates_removed: 847; language: English; splits_used: HealthCareMagic-100k, iCliniq-10k; splits_excluded: GenMedGPT-5k

### Output Artifacts

**Artifact: `Llama-Doctor-3.2-3B-Instruct`**
- **identifier**: Llama-Doctor-3.2-3B-Instruct
- **description**: Fine-tuned Llama 3.2 3B model specialised for medical conversational QA. Distributed as BF16 safetensors (two shards: 4.97 GB + 1.46 GB) and a GGUF variant for consumer inference runtimes. Architecture is identical to the base Llama-3.2-3B-Instruct model. Intended for chatbot, medical consultation, and content-generation applications. Not intended as a clinical decision-support tool. License: Llama 3.2 Community License.
- **reference**: https://huggingface.co/prithivMLmods/Llama-Doctor-3.2-3B-Instruct
- **size**: ~6.43 GB (BF16 safetensors); additional GGUF variants available
- **additional metadata**: base_model: meta-llama/Llama-3.2-3B-Instruct; training_loss_final: 0.84; training_loss_initial: 2.31; fine_tuning_method: full SFT (no PEFT); torch_dtype: bfloat16; license: Llama 3.2 Community License
