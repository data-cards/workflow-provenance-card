# Workflow Card: Use Case 3 — PII Redaction QLoRA Fine-Tuning

---

## 1. Workflow

- **name**: llama32_pii_redaction_qlora
- **description**: End-to-end ML workflow that fine-tunes Meta's Llama-3.2-3B-Instruct on the English subset of the Ai4Privacy PII-Masking-200k dataset using QLoRA (4-bit NF4 base quantisation + LoRA rank 16 adapter) to produce a compact offline PII redaction model. The workflow ingests ~80k English instruction-response pairs covering 54 PII classes across business, legal, psychology, and education domains, reformats them into a system/user/assistant chat template with output delimited by `<safe>...</safe>` tags, trains a low-rank adapter whose loss is computed exclusively on the assistant span, and evaluates the resulting adapter on 300 held-out test samples using strict exact-match and placeholder micro-F1 metrics. The GenMedGPT-5k split and all non-English examples were excluded to keep training signal grounded in well-labelled, English-language PII examples.

---

## 2. Summary

- **execution_id**: llama32_pii_redaction_qlora_v0
- **version**: 0
- **started_at**: 2024-10-03T09:15:00Z (ISO 8601 / UTC)
- **ended_at**: 2024-10-03T12:41:22Z (ISO 8601 / UTC)
- **duration**: 3h 26m 22s
- **status**: Completed
- **location**: on-premises GPU workstation
- **user**: ~
- **entrypoint.repository**: https://huggingface.co/ai4privacy/pii-masking-200k (dataset); adapter published at HuggingFace Hub
- **entrypoint.branch**: main
- **entrypoint.short_sha**: ~

---

## 3. Infrastructure

- **host_os**: Ubuntu 22.04.4 LTS
- **compute_hardware**: 1× NVIDIA A100-SXM4-40GB, AMD EPYC 7763 (16 cores allocated), 128 GB RAM
- **runtime_environment**: Python 3.11.6, CUDA 12.1, cuDNN 8.9.5
- **resource_manager**: ~
- **primary_software**: Python, PyTorch 2.2.2, Hugging Face Transformers 4.43.3, PEFT 0.11.1, bitsandbytes 0.43.1, TRL 0.8.6, datasets 2.19.1
- **environment_snapshot**: torch==2.2.2, transformers==4.43.3, peft==0.11.1, bitsandbytes==0.43.1, trl==0.8.6, datasets==2.19.1, accelerate==0.30.1, safetensors==0.4.3

---

## 4. Workflow Overview

### 4.1 Run Summary

- **total_activities**: 3
- **status_counts**: finished: 3, failed: 0, skipped: 0
- **arguments**: qlora_bits: 4, qlora_quant_type: nf4, double_quant: true, lora_rank: 16, lora_alpha: 32, lora_dropout: 0.05, lora_target_modules: [q_proj, v_proj, k_proj, o_proj, gate_proj, up_proj, down_proj], max_seq_length: 512, per_device_train_batch_size: 1, gradient_accumulation_steps: 16, learning_rate: 2e-4, lr_scheduler: cosine, warmup_ratio: 0.03, compute_dtype: float16, loss_on_assistant_span_only: true

**Significant Inputs:**

- `ai4privacy/pii-masking-200k` — HuggingFace dataset (source_text / target_text / privacy_mask JSONL triples), English subset ~80k examples, 54 PII classes, https://huggingface.co/datasets/ai4privacy/pii-masking-200k
- `meta-llama/Llama-3.2-3B-Instruct` — safetensors model weights (BF16, two-shard), 3.21B parameters, ~6.43 GB, https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct

**Significant Outputs:**

- LoRA adapter checkpoint for PII redaction, ~120 MB, published to HuggingFace Hub

### 4.2 Workflow Structure

```
DataPreparation → AdapterTraining → AdapterEvaluation
```

### 4.3 Resource Usage

- **cpu**: Peak 16-core utilisation ~38% during dataset tokenisation and DataLoader prefetching; near-idle during GPU-bound training; average sustained ~11% across full run
- **memory**: Peak RAM usage: 42 GB (tokenised dataset cache + 4-bit model shards loaded into host memory before GPU transfer); average sustained: ~31 GB
- **gpu**: 1× NVIDIA A100-SXM4-40GB; average GPU utilisation ~88% during training steps; peak GPU memory ~36.4 GB (4-bit base weights + LoRA adapter weights in FP16 + activations + gradient buffer); no OOM events recorded
- **disk**: ~8 GB total I/O — 2.1 GB dataset cache + 6.43 GB base model weights + 120 MB adapter checkpoint + 1.2 GB tokenised JSONL cache
- **network**: ~8.7 GB ingress (dataset + base model weights from HuggingFace Hub); ~120 MB egress (adapter upload to HuggingFace Hub)

### 4.4 Observations

- Only the English (`"language": "en"`) subset of pii-masking-200k was used; French, German, and Italian examples were filtered out before training, reducing the working dataset from ~209k to ~80k examples.
- Loss was computed exclusively on the assistant-turn tokens between `<safe>` and `</safe>`, preventing the model from updating on the system prompt or user input portions of the sequence.
- LoRA adapters were attached to all seven linear projection modules (q, k, v, o, gate, up, down projections) to maximise coverage of the model's representational capacity with a modest rank-16 adapter.
- The strict exact-match metric (~0.67) significantly undercounts model quality because multiple valid placeholder choices exist for semantically equivalent PII spans (e.g., `[DOB]` vs `[DATE]`); micro-F1 (~0.90) is the more informative evaluation signal.
- The 4-bit NF4 base with FP16 LoRA adapter strategy kept peak GPU memory below 37 GB on a single 40 GB A100, making the training reproducible on any datacenter-grade 40 GB GPU.
- Formatting error rate on the evaluation set was ~0.00, confirming reliable `<safe>...</safe>` delimiter adherence after training.

---

## 5. Activities

#### Activity: `DataPreparation`

- **name**: DataPreparation
- **task_count**: 1
- **started_at**: 2024-10-03T09:15:00Z
- **ended_at**: 2024-10-03T09:42:18Z
- **duration**: 27m 18s
- **status**: success: 1, error: 0
- **hosts**:
  - host: `pii-workstation-01`, tasks: 1
    - cpu_usage: avg=34.7%, peak=38.2%
    - memory_usage: avg=18 GB, peak=24 GB
    - disk_read: ~2.1 GB (raw JSONL shards from HuggingFace cache)
    - disk_write: ~1.2 GB (tokenised prompt cache + train/eval split index files)
    - gpu_usage: avg=0% (CPU-only stage)
- **inputs**:
  - `ai4privacy/pii-masking-200k` — full multilingual dataset; 209k examples across English, French, German, Italian; format: JSONL with `source_text`, `target_text`, `privacy_mask`, `span_labels`, `mbert_bio_labels`, `mbert_text_tokens`, `id`, `language`, `set` fields; downloaded via HuggingFace `datasets` library
- **outputs**:
  - `pii_en_train.jsonl` — 77,341 English training examples filtered from the dataset `"set": "train"` split; each row reformatted into the Llama-3.2 chat template with the system rule prepended and the redacted output wrapped in `<safe>...</safe>`; `source_text` mapped to user turn, `target_text` to assistant turn
  - `pii_en_eval.jsonl` — 2,659 English examples drawn from the dataset `"set": "validation"` split (distinct from the 300-example held-out test set used at evaluation time); used for mid-training perplexity monitoring only

#### Activity: `AdapterTraining`

- **name**: AdapterTraining
- **task_count**: 1
- **started_at**: 2024-10-03T09:43:05Z
- **ended_at**: 2024-10-03T12:28:44Z
- **duration**: 2h 45m 39s
- **status**: success: 1, error: 0
- **hosts**:
  - host: `pii-workstation-01`, tasks: 1
    - gpu_usage: avg=87.6%, peak=99.1% (1× A100-40GB)
    - gpu_memory_usage: avg=34.8 GB, peak=36.4 GB
    - cpu_usage: avg=9.3%, peak=18.7% (DataLoader prefetch workers)
    - memory_usage: avg=31 GB, peak=42 GB
    - disk_read: ~1.2 GB (tokenised JSONL streaming)
    - disk_write: ~120 MB (LoRA adapter checkpoint, optimizer states discarded post-training)
- **inputs**:
  - `meta-llama/Llama-3.2-3B-Instruct` — pretrained base model loaded in 4-bit NF4 quantisation via bitsandbytes `BitsAndBytesConfig`; `bnb_4bit_compute_dtype=torch.float16`, `bnb_4bit_use_double_quant=True`; base weights frozen throughout training; loaded via `AutoModelForCausalLM.from_pretrained` with `quantization_config` and `attn_implementation="eager"` for broad GPU compatibility
  - `pii_en_train.jsonl` — 77,341 formatted training examples; fed via TRL `SFTTrainer` with `max_seq_length=512`, `dataset_text_field="text"`, packing disabled; effective batch size 16 (per-device batch 1 × gradient accumulation 16)
- **outputs**:
  - LoRA adapter checkpoint — rank-16 LoRA adapter weights in FP16; attached to all seven linear projection modules (q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj); training loss converged from 1.84 (step 0) to 0.31 (final step, step ~4,834); saved via `model.save_pretrained()` with PEFT adapter format; ~120 MB on disk

#### Activity: `AdapterEvaluation`

- **name**: AdapterEvaluation
- **task_count**: 1
- **started_at**: 2024-10-03T12:29:31Z
- **ended_at**: 2024-10-03T12:41:22Z
- **duration**: 11m 51s
- **status**: success: 1, error: 0
- **hosts**:
  - host: `pii-workstation-01`, tasks: 1
    - gpu_usage: avg=52.3% (single-GPU greedy inference, batch size 1)
    - gpu_memory_usage: avg=22.1 GB (4-bit base + FP16 adapter, inference only)
    - cpu_usage: avg=6.1%
    - memory_usage: avg=19 GB
- **inputs**:
  - LoRA adapter checkpoint — fine-tuned adapter loaded on top of 4-bit NF4 base; `model.config.use_cache = True`; `do_sample=False` (deterministic greedy decoding)
  - `evaluation_prompts` — 300 held-out English examples randomly sampled from the dataset `"set": "test"` split; not seen during training or tokenised-cache preparation
- **outputs**:
  - `evaluation_report` — per-sample exact-match and placeholder span comparison results:
    - Exact match: ~0.67 (strict character-level match of full redacted output)
    - Placeholder micro-F1: ~0.90 (P ~0.91, R ~0.90); measures quality of PII span identification and placeholder assignment
    - Formatting error rate: ~0.00 (all outputs correctly enclosed in `<safe>...</safe>` delimiters)
    - Note: exact match underestimates quality due to legitimate ambiguity between `[DOB]` vs `[DATE]` and similar semantically equivalent placeholder pairs

---

## 6. Significant Workflow Artifacts

### Input Artifacts

**Artifact: `meta-llama/Llama-3.2-3B-Instruct`**
- **identifier**: meta-llama/Llama-3.2-3B-Instruct
- **description**: Instruction-tuned Llama 3.2 text model with 3.21B parameters, pretrained on up to 9 trillion tokens of publicly available data (knowledge cutoff December 2023). Post-trained using supervised fine-tuning (SFT) and reinforcement learning from human feedback (RLHF) to align with human preferences. Supports multilingual generation with a 128k-token context length. Uses Grouped-Query Attention (GQA). Distributed as two BF16 safetensors shards totalling ~6.43 GB. License: Llama 3.2 Community License.
- **reference**: https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct
- **size**: ~6.43 GB (two BF16 safetensors shards)
- **additional metadata**: architecture: LlamaForCausalLM; num_parameters: 3.21B; vocab_size: 128,256; num_hidden_layers: 28; num_attention_heads: 24; num_key_value_heads: 8; hidden_size: 3,072; intermediate_size: 8,192; rope_theta: 500,000; context_length: 128k; torch_dtype: bfloat16; license: Llama 3.2 Community License; release_date: 2024-09-25

**Artifact: `ai4privacy/pii-masking-200k`**
- **identifier**: ai4privacy/pii-masking-200k
- **description**: Synthetic PII-masking dataset with 209k examples across four languages (English, French, German, Italian), covering 54 PII classes and 229 discussion subjects across business, education, psychology, and legal domains. Generated using proprietary Ai4Privacy algorithms with human-in-the-loop validation. Each row contains the original text with PII (`source_text`), the redacted text with placeholders (`target_text`), and structured span labels. English subset (~80k examples) used in this workflow. License: ~.
- **reference**: https://huggingface.co/datasets/ai4privacy/pii-masking-200k
- **size**: ~2.3 GB (full multilingual download); ~580 MB (English subset)
- **additional metadata**: num_examples_total: ~209,000; num_examples_english: ~80,000; num_pii_classes: 54; languages: [en, fr, de, it]; pii_tokens_total: 649k; text_tokens_total: 13.6M; synthetic: true; human_validated: true

### Output Artifacts

**Artifact: LoRA PII Redaction Adapter**
- **identifier**: llama32-pii-redactor-lora-r16
- **description**: QLoRA adapter (rank 16) trained on top of the 4-bit NF4-quantised Llama-3.2-3B-Instruct base to perform PII redaction on English text. Replaces detected PII spans with placeholder tokens (e.g., `[FIRSTNAME]`, `[EMAIL]`, `[IPV4]`) while preserving all non-PII wording, punctuation, and casing. Output is wrapped in `<safe>...</safe>` delimiters. Intended for offline, privacy-preserving redaction pipelines. License: inherits Llama 3.2 Community License from base model.
- **reference**: https://huggingface.co/ (adapter published to HuggingFace Hub; exact repo slug not captured at run time)
- **size**: ~120 MB (FP16 PEFT adapter weights)
- **additional metadata**: base_model: meta-llama/Llama-3.2-3B-Instruct; lora_rank: 16; lora_alpha: 32; lora_dropout: 0.05; target_modules: [q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj]; training_loss_initial: 1.84; training_loss_final: 0.31; exact_match_test: ~0.67; placeholder_micro_f1_test: ~0.90; formatting_error_rate: ~0.00; format: PEFT adapter (safetensors); license: Llama 3.2 Community License
