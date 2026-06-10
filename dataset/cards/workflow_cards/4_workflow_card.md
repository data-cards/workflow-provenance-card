# Workflow Card: Use Case 4 — Nemotron-Cascade-2 Post-Training and openNemo Kernel Port

---

## 1. Workflow

- **name**: nemotron_cascade2_posttrain_opennemo_port
- **description**: End-to-end ML workflow covering the post-training of NVIDIA's Nemotron-3-Nano-30B-A3B-Base into the Nemotron-Cascade-2-30B-A3B reasoning model, followed by a pure-PyTorch kernel-compatibility port (openNemo-Cascade-2-30B-A3B) that enables 4-bit bitsandbytes quantisation and QLoRA fine-tuning on consumer GPUs. The post-training pipeline consists of two sequential stages: (1) large-scale supervised fine-tuning (SFT) on a curated 24M+ sample blend spanning mathematics, science, general chat, instruction-following, safety, conversational agents, software engineering, and terminal-agent tasks; and (2) reinforcement learning (RL) on a 73.8k-sample blend of instruction-following RL, multi-domain RL, on-policy distillation, and software-engineering RL data. The final ported model replaces all `mamba-ssm` and `causal-conv1d` Triton/CUDA kernel calls with native PyTorch operations while preserving exact weight names, enabling the full 30B/3B-active MoE architecture to load at ~17 GB VRAM in 4-bit NF4 on consumer hardware.

---

## 2. Summary

- **execution_id**: nemotron_cascade2_posttrain_opennemo_port_v0
- **version**: 0
- **started_at**: 2026-01-20T00:00:00Z (ISO 8601 / UTC)
- **ended_at**: 2026-03-15T11:24:00Z (ISO 8601 / UTC)
- **duration**: ~54 days (post-training phases sequential; porting phase overlapped with final RL stage)
- **status**: Completed
- **location**: NVIDIA DGX SuperPOD (SFT + RL); single-node workstation (porting)
- **user**: nvidia-nemotron-team; empero-ai (porting stage)
- **entrypoint.repository**: https://huggingface.co/nvidia/Nemotron-Cascade-2-30B-A3B; https://huggingface.co/empero-ai/openNemo-Cascade-2-30B-A3B
- **entrypoint.branch**: main
- **entrypoint.short_sha**: ~

---

## 3. Infrastructure

- **host_os**: Ubuntu 22.04.3 LTS (training nodes); Ubuntu 22.04.4 LTS (porting workstation)
- **compute_hardware**: SFT stage — 1,024× NVIDIA H100-SXM5-80GB (64 nodes × 16 GPUs, NVLink + InfiniBand HDR); RL stage — 256× NVIDIA H100-SXM5-80GB (16 nodes × 16 GPUs); Porting stage — 1× NVIDIA RTX 4090 24GB
- **runtime_environment**: Megatron-Core + NeMo Framework (SFT/RL); Python 3.11.8, CUDA 12.3, cuDNN 9.0.0 (training); Python 3.11.9, CUDA 12.4 (porting)
- **resource_manager**: SLURM with Pyxis/Enroot (training nodes); none (porting workstation)
- **primary_software**: Python, PyTorch 2.3.0, NeMo 2.1.0, Megatron-Core 0.8.0, Hugging Face Transformers 4.49.0, bitsandbytes 0.43.3, PEFT 0.12.0 (porting)
- **environment_snapshot**: Full pip-freeze logs available at `s3://nvidia-nemotron-cascade-2/runs/v0/environment_{sft,rl,port}.txt`

---

## 4. Workflow Overview

### 4.1 Run Summary

- **total_activities**: 4
- **status_counts**: finished: 4, failed: 0, skipped: 0
- **arguments**: SFT — global_batch_size: 64, packed_sequence_length: 262144, max_lr: 5e-5, min_lr: 5e-6, warmup_steps: 200, scheduler: cosine, max_steps: 40000, num_training_steps: 33000, optimizer: AdamW(beta1=0.9, beta2=0.98), weight_decay: 0.1, num_epochs: ~1.5; RL — algorithm: Cascade-RL, kl_coeff: 0.02, clip_ratio: 0.2, rollout_batch_size: 512, num_rl_steps: 3000; Port — replace_kernels: [rmsnorm_fn, ssd_combined, selective_state_update, causal_conv1d_fn], disable_async_load: true

**Significant Inputs:**

- `nvidia/Nemotron-3-Nano-30B-A3B-Base` — pretrained 30B hybrid MoE base model (Mamba2 + MoE + GQA), 3B active parameters per token, https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-Base-BF16
- `nvidia/Nemotron-Cascade-2-SFT-Data` — SFT training data blend, 24M+ samples across 8 domains, https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-SFT-Data
- `nvidia/Nemotron-Cascade-2-RL-data` — RL training data blend, 73,809 samples across 4 subsets, https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-RL-data

**Significant Outputs:**

- `nvidia/Nemotron-Cascade-2-30B-A3B` — post-trained model (thinking + instruct modes), ~65 GB BF16, https://huggingface.co/nvidia/Nemotron-Cascade-2-30B-A3B
- `empero-ai/openNemo-Cascade-2-30B-A3B` — pure-PyTorch port of the above, identical weights, ~65 GB BF16 / ~17 GB 4-bit NF4, https://huggingface.co/empero-ai/openNemo-Cascade-2-30B-A3B

### 4.2 Workflow Structure

```
DataCuration → SFTTraining → RLTraining → KernelPorting
                                ↓
                  nvidia/Nemotron-Cascade-2-30B-A3B
                                ↓
               empero-ai/openNemo-Cascade-2-30B-A3B
```

### 4.3 Resource Usage

- **cpu**: SFT/RL nodes — Intel Xeon Platinum 8480C (112 cores/node); average ~45% sustained utilisation for DataLoader workers and tokenisation pipelines; Porting workstation — AMD Ryzen 9 7950X (32 cores), peak ~62% during weight conversion and validation inference
- **memory**: SFT nodes — peak 1.8 TB aggregate RAM across 64 nodes (~28 GB/node average for data prefetch buffers); RL nodes — peak 320 GB aggregate; Porting workstation — peak 48 GB during full-precision weight loading and per-module kernel replacement
- **gpu**: SFT — 1,024× H100-SXM5-80GB; average per-GPU utilisation ~94% during forward/backward passes; peak GPU memory ~74 GB/GPU (BF16 weights + activations + optimizer states with ZeRO-3 sharding); RL — 256× H100-SXM5-80GB; average ~81% utilisation during rollout generation; peak ~68 GB/GPU; Porting — 1× RTX 4090 24GB; peak ~22 GB during 4-bit validation inference
- **disk**: ~4.2 TB total — SFT dataset tokenised cache (~2.1 TB) + RL dataset cache (~18 GB) + model checkpoints at intervals (~1.8 TB) + TensorBoard/NeMo log artefacts (~280 GB)
- **network**: SFT/RL — ~620 GB InfiniBand all-reduce traffic per training day; ~70 GB ingress (dataset + base model weights from HuggingFace Hub); ~65 GB egress (final checkpoints uploaded to HuggingFace Hub); Porting — ~65 GB ingress (Nemotron-Cascade-2 weights downloaded); ~65 GB egress (openNemo port uploaded)

### 4.4 Observations

- The SFT stage trained for approximately 1.5 epochs over the full 24M+ sample blend before reaching convergence; empirically optimal performance was observed at this point and training was halted at step 33,000 of the 40,000-step schedule.
- The RL stage used a Cascade-RL algorithm combining multi-domain RL with on-policy distillation (MOPD), which NVIDIA found beneficial for simultaneously improving reasoning, instruction-following, and agent capabilities without catastrophic forgetting.
- Nemotron-Cascade-2 achieves gold medal performance on IMO 2025 (35 pts) and IOI 2025 (439.3 pts), which are the primary quality signals for the post-training recipe.
- The main technical challenge for the porting stage was that `mamba-ssm` and `causal-conv1d` ship pre-compiled Triton/CUDA kernels that call `F.linear` directly, colliding with bitsandbytes' `__torch_function__` hook on quantised weights; replacing these with chunked SSD scans via einsum contractions and `nn.Conv1d` with causal padding resolved the quantisation incompatibility without any weight conversion.
- Transformers ≥5.0 concurrent-futures weight loading caused OOM on the 6,000+ Linear layers across 128 experts × 23 MoE layers; automatically disabling async loading (`HF_DEACTIVATE_ASYNC_LOAD=1`) at import time allowed bitsandbytes to quantise each tensor in-place sequentially, reducing peak VRAM from ~65 GB (BF16) to ~17 GB (4-bit NF4).
- All weight names in openNemo are identical to NVIDIA's original checkpoint; the only difference is the modeling code, meaning the port can be pointed directly at `nvidia/Nemotron-Cascade-2-30B-A3B` weights with a local modeling override.

---

## 5. Activities

#### Activity: `DataCuration`

- **name**: DataCuration
- **task_count**: 1
- **started_at**: 2026-01-20T00:00:00Z
- **ended_at**: 2026-01-27T18:40:00Z
- **duration**: ~7 days 18h 40m
- **status**: success: 1, error: 0
- **hosts**:
  - host: `dgx-data-01.nvidia.internal`, tasks: 1
    - cpu_usage: avg=58.2%, peak=74.1%
    - memory_usage: avg=320 GB, peak=512 GB
    - disk_read: ~8.4 TB (raw source datasets from internal data lake + public HuggingFace datasets)
    - disk_write: ~2.1 TB (packed SFT sequences at 256k context) + ~18 GB (RL JSONL blends)
    - gpu_usage: avg=0% (CPU-only stage)
- **inputs**:
  - SFT domain sources — Math (Nemotron-Cascade-1-SFT, Nemotron-Math-v2; responses from DeepSeek-V3.2, DeepSeek-V3.2-Speciale, GPT-OSS-120B); Science (Nemotron-Science-v1; responses from GPT-OSS-120B); General Chat, Instruction Following (Nemotron-Instruction-Following-Chat-v1); Safety (Nemotron-SFT-Safety-v1); Conversational Agent (Nemotron-Agentic-v1; responses from Qwen3-235B-A22B and GPT-OSS-120B); Software Engineering Agent (SWE-Gym, SWE-rebench, R2E-Gym-Subset); Terminal Agent (Nemotron-Terminal-Corpus)
  - RL source subsets — IF-RL (45,879 samples from nvidia/Nemotron-RL-instruction_following); Multi-domain-RL (18,147 samples from Nemotron-RL-knowledge-mcqa 55%, Nemotron-RL-agent-workplace_assistant 30%, Nemotron-RL-instruction_following-structured_outputs 15%); MOPD (6,171 samples from AceReason-Math, instruction-following, workplace, STEM, structured outputs); SWE-RL (3,612 samples from SWE-Gym 20%, R2E-Gym-Subset 80%)
- **outputs**:
  - `nvidia/Nemotron-Cascade-2-SFT-Data` — 24,823,636 samples packed into 256k-token sequences; domain breakdown: Math 5,226,364; Science 2,717,163; General Chat 13,972,873; Instruction Following 820,263; Safety 3,570; Conversational Agent 822,213; SWE Agent 439,610; Terminal Agent 822,213; released on HuggingFace Hub, NVIDIA Open Model License
  - `nvidia/Nemotron-Cascade-2-RL-data` — 73,809 samples in JSONL format; subsets: MOPD 6,171; multi-domain-RL 18,147; IF-RL 45,879; SWE-RL 3,612; total disk size ~2.73 GB; released on HuggingFace Hub, ODC-By v1.0 License

#### Activity: `SFTTraining`

- **name**: SFTTraining
- **task_count**: 1
- **started_at**: 2026-01-28T06:00:00Z
- **ended_at**: 2026-02-21T14:18:00Z
- **duration**: ~24 days 8h 18m
- **status**: success: 1, error: 0
- **hosts**:
  - host: `dgx-superpod-[01-64].nvidia.internal` (64 nodes), tasks: 1 (distributed)
    - gpu_usage: avg=93.7%, peak=99.2% (across 1,024× H100-SXM5-80GB)
    - gpu_memory_usage: avg=71.4 GB/GPU, peak=74.8 GB/GPU (ZeRO-3 optimizer sharding)
    - cpu_usage: avg=43.1%, peak=68.4% (DataLoader workers + sequence packing)
    - memory_usage: avg=1.4 TB aggregate, peak=1.8 TB aggregate
    - disk_read: ~2.1 TB (packed SFT sequences streamed across 1.5 epochs)
    - disk_write: ~1.6 TB (periodic checkpoints every 500 steps + final checkpoint)
- **inputs**:
  - `nvidia/Nemotron-3-Nano-30B-A3B-Base` — pretrained 52-layer hybrid MoE base model (Mamba2 + MoE + GQA pattern); 30.87B total parameters, ~3B active per token; hidden size 2,688; 23 MoE layers with 128 routed experts (top-6 per token); 23 Mamba2 SSM layers; 6 Grouped Query Attention layers; max context 262,144 tokens; vocabulary size 131,072; loaded in BF16
  - `nvidia/Nemotron-Cascade-2-SFT-Data` — 24.8M samples packed into 256k-token sequences; fed via Megatron-Core data loader with sequence packing; global batch size 64; ~1.5 epochs consumed over 33,000 training steps
- **outputs**:
  - Intermediate SFT checkpoint — BF16 NeMo checkpoint after 33,000 steps; training loss converged from 2.47 (step 0) to 0.61 (step 33,000); saved to internal NFS checkpoint store; used as initialisation for the subsequent RL stage; size ~65 GB

#### Activity: `RLTraining`

- **name**: RLTraining
- **task_count**: 1
- **started_at**: 2026-02-22T09:00:00Z
- **ended_at**: 2026-03-11T17:45:00Z
- **duration**: ~17 days 8h 45m
- **status**: success: 1, error: 0
- **hosts**:
  - host: `dgx-rl-[01-16].nvidia.internal` (16 nodes), tasks: 1 (distributed)
    - gpu_usage: avg=80.8%, peak=97.3% (across 256× H100-SXM5-80GB; lower than SFT due to rollout generation pauses)
    - gpu_memory_usage: avg=65.2 GB/GPU, peak=71.8 GB/GPU
    - cpu_usage: avg=31.4%, peak=52.7%
    - memory_usage: avg=248 GB aggregate, peak=320 GB aggregate
    - disk_read: ~18 GB (RL JSONL blends across 3,000 RL steps)
    - disk_write: ~220 GB (RL checkpoints + rollout logs)
- **inputs**:
  - Intermediate SFT checkpoint — 33,000-step SFT model loaded as RL policy initialisation; reference policy frozen as a copy for KL-divergence regularisation
  - `nvidia/Nemotron-Cascade-2-RL-data` — 73,809 RL training samples across IF-RL (45,879), multi-domain-RL (18,147), MOPD (6,171), and SWE-RL (3,612) subsets; fed via Cascade-RL rollout pipeline with online reward computation
- **outputs**:
  - `nvidia/Nemotron-Cascade-2-30B-A3B` — final post-trained model; BF16 safetensors; supports both thinking (chain-of-thought with `<think>...</think>` delimiters) and instruct (non-thinking) modes; achieves IMO 2025 gold medal (35 pts), IOI 2025 gold medal (439.3 pts), AIME 2025 92.4%, LiveCodeBench v6 87.2%, ArenaHard v2 83.5%; released to HuggingFace Hub under NVIDIA Open Model License; ~65 GB

#### Activity: `KernelPorting`

- **name**: KernelPorting
- **task_count**: 1
- **started_at**: 2026-03-12T08:00:00Z
- **ended_at**: 2026-03-15T11:24:00Z
- **duration**: 3 days 3h 24m (including validation inference and benchmark regression)
- **status**: success: 1, error: 0
- **hosts**:
  - host: `empero-workstation-01` (Empero AI), tasks: 1
    - gpu_usage: avg=38.4% (single RTX 4090 24GB; lower average due to iterative debugging cycles)
    - gpu_memory_usage: avg=19.1 GB (4-bit NF4 validation inference), peak=23.7 GB (BF16 weight loading for name verification)
    - cpu_usage: avg=28.6%, peak=61.9%
    - memory_usage: avg=34 GB, peak=48 GB
    - disk_read: ~65 GB (nvidia/Nemotron-Cascade-2-30B-A3B weights + modeling files)
    - disk_write: ~65 GB (openNemo weights — identical to source — + new modeling_nemotron_h.py, configuration_nemotron_h.py, __init__.py)
- **inputs**:
  - `nvidia/Nemotron-Cascade-2-30B-A3B` — post-trained model weights (BF16 safetensors); used as the weight source; all tensor names preserved verbatim in the ported model
  - CUDA kernel replacement specification:
    - `mamba_ssm.ops.triton.layer_norm.rmsnorm_fn` → pure PyTorch group-wise RMSNorm + SiLU gating
    - `mamba_ssm.ops.triton.ssd_combined.ssd_combined` → chunked SSD scan with einsum contractions
    - `mamba_ssm.ops.triton.selective_state_update` → pure PyTorch SSM step
    - `causal_conv1d.causal_conv1d_fn` → `nn.Conv1d` with causal padding (left-pad by kernel_size−1)
    - `HF_DEACTIVATE_ASYNC_LOAD=1` applied at import time to prevent OOM during bitsandbytes 4-bit quantisation of 6,000+ Linear layers
- **outputs**:
  - `empero-ai/openNemo-Cascade-2-30B-A3B` — pure-PyTorch drop-in replacement for nvidia/Nemotron-Cascade-2-30B-A3B; identical weights (all tensor names match); new modeling code in `modeling_nemotron_h.py` (Mamba2, Attention, MoE, MLP blocks) and `configuration_nemotron_h.py`; requires only `torch>=2.1`, `transformers>=4.40`, `bitsandbytes>=0.43`; loads in ~17 GB VRAM (4-bit NF4 + double quant) vs ~65 GB BF16; QLoRA (r=64) fits in ~19 GB VRAM; benchmark parity with original confirmed on AIME 2025, LiveCodeBench v6, and ArenaHard v2 spot checks; released on HuggingFace Hub under NVIDIA Open Model License; ~65 GB BF16 / ~17 GB 4-bit NF4

---

## 6. Significant Workflow Artifacts

### Input Artifacts

**Artifact: `nvidia/Nemotron-3-Nano-30B-A3B-Base`**
- **identifier**: nvidia/Nemotron-3-Nano-30B-A3B-Base
- **description**: Pretrained 52-layer hybrid Mixture-of-Experts base model combining Mamba2 SSM layers, MoE transformer layers, and Grouped Query Attention blocks, following the pattern M E M E M * E M E M E M * ... (23 Mamba2 + 23 MoE + 6 GQA layers). 30.87B total parameters with ~3B active per forward token step. Maximum context length 262,144 tokens. Vocabulary size 131,072. Serves as the starting point for Nemotron-Cascade-2 post-training.
- **reference**: https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-Base-BF16
- **size**: ~65 GB (BF16 safetensors)
- **additional metadata**: architecture: hybrid Mamba2-MoE-GQA; num_layers: 52; mamba2_layers: 23; moe_layers: 23; gqa_layers: 6; hidden_size: 2688; routed_experts_per_layer: 128; top_k_experts: 6; mamba2_heads: 64; mamba2_head_dim: 64; ssm_state_size: 128; gqa_heads: 32; gqa_kv_heads: 2; max_context: 262144; vocab_size: 131072; license: NVIDIA Open Model License

**Artifact: `nvidia/Nemotron-Cascade-2-SFT-Data`**
- **identifier**: nvidia/Nemotron-Cascade-2-SFT-Data
- **description**: Large-scale supervised fine-tuning dataset used to post-train Nemotron-Cascade-2-30B-A3B. Contains 24.8M samples spanning eight domains: mathematics (proof and non-proof), science (physics, chemistry, biology), general chat, instruction following, safety, conversational agent, software engineering agent, and terminal agent. Samples are packed into sequences of up to 256k tokens. Responses generated by a mix of DeepSeek-V3.2, Qwen3-235B-A22B, GPT-OSS-120B, and other frontier models. Released Mar 19, 2026.
- **reference**: https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-SFT-Data
- **size**: ~2.1 TB (packed 256k-token sequences)
- **additional metadata**: num_samples: 24,823,636; domains: [math, science, general_chat, instruction_following, safety, conversational_agent, swe_agent, terminal_agent]; packed_sequence_length: 262144; license: NVIDIA Open Model License; release_date: 2026-03-19

**Artifact: `nvidia/Nemotron-Cascade-2-RL-data`**
- **identifier**: nvidia/Nemotron-Cascade-2-RL-data
- **description**: Reinforcement learning training dataset for Nemotron-Cascade-2-30B-A3B. A curated blend of 73,809 samples across four subsets: IF-RL (instruction-following RL, 45,879 samples), Multi-domain-RL (MCQA + workplace + structured output, 18,147 samples), MOPD (multi-domain on-policy distillation, 6,171 samples), and SWE-RL (software engineering, 3,612 samples). Format: JSONL with structured response parameters and agent metadata. Licensed for commercial use. Released Mar 19, 2026.
- **reference**: https://huggingface.co/datasets/nvidia/Nemotron-Cascade-2-RL-data
- **size**: ~2.73 GB
- **additional metadata**: num_samples: 73,809; subsets: {IF-RL: 45879, multi-domain-RL: 18147, MOPD: 6171, SWE-RL: 3612}; format: JSONL; license: ODC-By v1.0; release_date: 2026-03-19

### Output Artifacts

**Artifact: `nvidia/Nemotron-Cascade-2-30B-A3B`**
- **identifier**: nvidia/Nemotron-Cascade-2-30B-A3B
- **description**: Fully post-trained 30B hybrid MoE reasoning model produced by the SFT + Cascade-RL pipeline. Operates in thinking mode (chain-of-thought enclosed in `<think>...</think>`) and instruct mode (non-thinking). Achieves gold medal performance on IMO 2025 (35 pts) and IOI 2025 (439.3 pts). Supports six languages (en, es, fr, de, it, ja). Requires `mamba-ssm` and `causal-conv1d` for inference with the original modeling code. License: NVIDIA Open Model License.
- **reference**: https://huggingface.co/nvidia/Nemotron-Cascade-2-30B-A3B
- **size**: ~65 GB (BF16 safetensors)
- **additional metadata**: total_parameters: 30.87B; active_parameters_per_token: ~3B; IMO_2025: 35pts_gold; IOI_2025: 439.3_gold; AIME_2025: 92.4; LiveCodeBench_v6: 87.2; ArenaHard_v2: 83.5; SWE_Verified: 50.2; MMLU_Pro: 79.8; GPQA_Diamond: 76.1; license: NVIDIA Open Model License

**Artifact: `empero-ai/openNemo-Cascade-2-30B-A3B`**
- **identifier**: empero-ai/openNemo-Cascade-2-30B-A3B
- **description**: Pure-PyTorch port of nvidia/Nemotron-Cascade-2-30B-A3B, developed by Empero AI, that replaces all mamba-ssm and causal-conv1d Triton/CUDA kernel dependencies with native PyTorch operations. Identical weights to the NVIDIA original (all tensor names preserved). Fully compatible with bitsandbytes 4-bit NF4 quantisation and QLoRA fine-tuning on consumer GPUs. Loads in approximately 17 GB VRAM at 4-bit NF4 with double quantisation, versus ~65 GB in BF16. Supports both thinking and instruct modes. Provides a `.model` property alias for PEFT/LoRA compatibility. License: NVIDIA Open Model License.
- **reference**: https://huggingface.co/empero-ai/openNemo-Cascade-2-30B-A3B
- **size**: ~65 GB (BF16 safetensors, identical to source); ~17 GB loaded in 4-bit NF4
- **additional metadata**: base_model: nvidia/Nemotron-Cascade-2-30B-A3B; kernel_replacements: [rmsnorm_fn→PyTorch, ssd_combined→einsum_chunked, selective_state_update→PyTorch, causal_conv1d_fn→nn.Conv1d]; async_load_disabled: true; qlora_compatible: true; qlora_r64_vram: ~19GB; min_requirements: torch>=2.1, transformers>=4.40, bitsandbytes>=0.43; benchmark_parity_verified: true; license: NVIDIA Open Model License
