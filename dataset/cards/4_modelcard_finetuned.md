---
license: other
license_name: nvidia-open-model-license
license_link: https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/
pipeline_tag: text-generation
datasets:
- nvidia/Nemotron-Cascade-2-SFT-Data
- nvidia/Nemotron-Cascade-2-RL-data
language:
- en
- es
- fr
- de
- it
- ja
library_name: transformers
tags:
- nvidia
- pytorch
- mamba2
- moe
- mixture-of-experts
- hybrid
- reasoning
- qlora
- bitsandbytes
- 4bit
base_model:
- nvidia/Nemotron-Cascade-2-30B-A3B
---
# openNemo-Cascade-2-30B-A3B

![openNemo](openNemo.jpg)

**Pure-PyTorch drop-in replacement for NVIDIA's [Nemotron-Cascade-2-30B-A3B](https://huggingface.co/nvidia/Nemotron-Cascade-2-30B-A3B).**

Removes all external CUDA kernel dependencies (`mamba-ssm`, `causal-conv1d`) and replaces them with native PyTorch operations, making the model fully compatible with **bitsandbytes 4-bit quantization** and **QLoRA fine-tuning** on consumer GPUs.

30B total parameters, 3B active per token. Loads in **17 GB VRAM** with 4-bit quantization.

By **[Empero AI](https://empero.org)**

---

## Why?

NVIDIA's Nemotron-Cascade-2 is a 30B MoE reasoning model that achieves gold medal performance on IMO 2025 and IOI 2025. But the original implementation depends on `mamba-ssm` and `causal-conv1d`, which ship pre-compiled Triton/CUDA kernels that:

- **Break bitsandbytes quantization** — the kernels call `F.linear` directly, colliding with bnb's `__torch_function__` hook on quantized weights
- **Require specific CUDA versions** — kernel compilation failures are common on consumer setups
- **Prevent QLoRA training** — you can't fine-tune what you can't quantize

openNemo Cascade fixes all of that. Same weights, same architecture, pure PyTorch.

## What Changed

| Component | Original (NVIDIA) | openNemo Cascade |
|---|---|---|
| `rmsnorm_fn` | `mamba_ssm.ops.triton.layer_norm` | Pure PyTorch group-wise RMSNorm + SiLU gating |
| `ssd_combined` | `mamba_ssm.ops.triton.ssd_combined` | Chunked SSD scan with einsum contractions |
| `selective_state_update` | `mamba_ssm.ops.triton.selective_state_update` | Pure PyTorch SSM step |
| `causal_conv1d_fn` | `causal_conv1d` package | `nn.Conv1d` with causal padding |
| Forward routing | Fast path (kernels) vs slow path | Optimized torch path only |
| `.model` accessor | Only `.backbone` | `.model` property alias (PEFT/LoRA compatible) |
| Async weight loading | OOM on large MoE models | Auto-disabled for safe 4-bit loading |

**All weight names are preserved** — loads NVIDIA's original checkpoint directly with zero conversion.

## Quickstart

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    "empero-ai/openNemo-Cascade-2-30B-A3B",
    quantization_config=bnb_config,
    trust_remote_code=True,
    device_map="auto",
)

tokenizer = AutoTokenizer.from_pretrained("empero-ai/openNemo-Cascade-2-30B-A3B")

# Thinking mode (reasoning)
messages = [{"role": "user", "content": "Prove that the sum of the first n odd numbers equals n²."}]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)

output = model.generate(**inputs, max_new_tokens=2048, do_sample=True, temperature=1.0, top_p=0.95)
response = tokenizer.decode(output[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)
print(response)
```

No `mamba-ssm` install needed. Just `pip install transformers bitsandbytes` and go.

### Instruct Mode (non-thinking)

```python
# Set enable_thinking=False to skip the <think> reasoning chain
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
```

### QLoRA Fine-Tuning

```python
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=64,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
```

## Architecture

Nemotron-Cascade-2 is a 52-layer hybrid model with four block types defined by the pattern:

```
M E M E M * E M E M E M * E M E M E M * E M E M E M * E M E M E M * E M E M E M E M * E M E M E M E
```

- **M** — Mamba2 SSM block (23 layers) — chunked structured state-space duality
- **E** — Mixture-of-Experts block (23 layers) — 128 routed experts, top-6 selected per token
- **\*** — Grouped Query Attention block (6 layers) — sparse GQA with 32 heads, 2 KV heads
- **-** — MLP block (not used in Cascade)

| Parameter | Value |
|---|---|
| Total parameters | 30.87B |
| Active parameters per token | ~3B |
| Hidden size | 2,688 |
| MoE layers | 23 |
| Routed experts per layer | 128 |
| Experts selected per token | 6 |
| Expert intermediate size | 1,856 |
| Shared experts per layer | 1 |
| Shared expert intermediate size | 3,712 |
| Mamba2 heads | 64 |
| Mamba2 head dim | 64 |
| SSM state size | 128 |
| Attention heads | 32 (2 KV heads) |
| Max context length | 262,144 tokens |
| Vocabulary size | 131,072 |

### 4-bit Memory Usage

| Setup | VRAM |
|---|---|
| bf16 (full precision) | ~65 GB |
| 4-bit NF4 + double quant | **~17 GB** |
| 4-bit + QLoRA (r=64) | ~19 GB |

## Benchmark Results

From the [original NVIDIA technical report](https://arxiv.org/abs/2603.19220):

| Benchmark | Nemotron-Cascade-2 |
|---|---|
| **IMO 2025** | **35 pts (Gold Medal)** |
| **IOI 2025** | **439.3 (Gold Medal)** |
| AIME 2025 | 92.4 (98.6 with TIR) |
| AIME 2026 | 90.9 (95.0 with TIR) |
| HMMT Feb25 | 94.6 |
| LiveCodeBench v6 | 87.2 (88.4 with TIR) |
| ICPC World Finals 2025 | 10/12 (Gold Medal) |
| ArenaHard v2 | 83.5 |
| SWE Verified (OpenHands) | 50.2 |
| MMLU-Pro | 79.8 |
| GPQA-Diamond | 76.1 |

## Requirements

```
torch>=2.1
transformers>=4.40
bitsandbytes>=0.43  # for 4-bit quantization
peft>=0.10          # optional, for LoRA/QLoRA
```

No `mamba-ssm`. No `causal-conv1d`. No CUDA kernel compilation.

## Technical Notes

### Async Loading Fix

Transformers >=5.0 uses a concurrent-futures weight loading pipeline that materializes bf16 tensors on GPU before bitsandbytes can quantize them. With 6,000+ Linear layers across 128 experts × 23 MoE layers, this causes OOM on GPUs with less than ~65 GB VRAM. openNemo Cascade automatically sets `HF_DEACTIVATE_ASYNC_LOAD=1` at import time to force sequential loading, which lets bnb quantize each tensor in-place. This is transparent to users — just call `from_pretrained` normally.

If you want async loading back (e.g., on a large-memory server), set `HF_DEACTIVATE_ASYNC_LOAD=0` before importing the model.

### Weight Compatibility

All weight names match NVIDIA's original checkpoint exactly. This repo contains the same weights — the only difference is the modeling code. You can also point this modeling code at NVIDIA's original repo:

```python
model = AutoModelForCausalLM.from_pretrained(
    "nvidia/Nemotron-Cascade-2-30B-A3B",  # NVIDIA's weights
    quantization_config=bnb_config,
    trust_remote_code=False,  # use our local code instead
    # ... provide local model code path
)
```

## Files

| File | Description |
|---|---|
| `modeling_nemotron_h.py` | Full model implementation — Mamba2, Attention, MoE, MLP blocks |
| `configuration_nemotron_h.py` | Model config with MoE parameters |
| `__init__.py` | Module exports |

## Citation

```bibtex
@article{Nemotron_Cascade_2,
  title={Nemotron-Cascade 2: Post-Training LLMs with Cascade RL and Multi-Domain On-Policy Distillation},
  author={Yang, Zhuolin and Liu, Zihan and Chen, Yang and Dai, Wenliang and Wang, Boxin and Lin, Sheng-Chieh and Lee, Chankyu and Chen, Yangyi and Jiang, Dongfu and He, Jiafan and Pi, Renjie and Lam, Grace and Lee, Nayeon and Bukharin, Alexander and Shoeybi, Mohammad and Catanzaro, Bryan and Ping, Wei},
  year={2026}
}
```

## License

NVIDIA Open Model License — same as the base model.

## Acknowledgments

- Original model: [Nemotron-Cascade-2-30B-A3B](https://huggingface.co/nvidia/Nemotron-Cascade-2-30B-A3B) by NVIDIA 
- openNemo port: [Empero AI](https://empero.org)