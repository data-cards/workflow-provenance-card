---
license: apache-2.0
datasets:
- ai4privacy/pii-masking-200k
language:
- en
metrics:
- precision
- recall
- f1
- exact_match
base_model:
- meta-llama/Llama-3.2-3B-Instruct
pipeline_tag: text-generation
library_name: transformers
---



# Llama-3.2-3B PII Redactor (LoRA)

This is a LoRA adapter on top of `meta-llama/Llama-3.2-3B-Instruct` that **redacts PII** in a piece of text by replacing detected spans with placeholders like `[FIRSTNAME]`, `[EMAIL]`, `[IPV4]`. The model returns the original text with only those spans replaced.

**Base model:** `meta-llama/Llama-3.2-3B-Instruct` <br/>
**Method:** QLoRA on a 4-bit base, LoRA rank 16 <br/>
**Data:** [`ai4privacy/pii-masking-200k`](https://huggingface.co/datasets/ai4privacy/pii-masking-200k) (English subset)<br/>
**Output contract:** The final answer is wrapped inside `<safe> ... </safe>`

## Why I trained this

I wanted a small and practical redactor that works offline and keeps the input wording intact. The goal was to have the model find PII and map it to a clear placeholder taxonomy without changing the rest of the text.

## Quick start

```python
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
import torch

base_id = "meta-llama/Llama-3.2-3B-Instruct"
adapter_id = "<your-username>/<your-repo-name>"  # replace with your repo

bnb = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

tok = AutoTokenizer.from_pretrained(base_id, use_fast=False)
base = AutoModelForCausalLM.from_pretrained(
    base_id,
    quantization_config=bnb,
    torch_dtype=torch.float16,
    attn_implementation="eager",  # friendly for older GPUs
)

model = PeftModel.from_pretrained(base, adapter_id)
model.eval(); model.config.use_cache = True

SAFE_OPEN, SAFE_CLOSE = "<safe>", "</safe>"
START, END, EOT = "<|start_header_id|>", "<|end_header_id|>", "<|eot_id|>"
BOS = tok.bos_token or "<|begin_of_text|>"

SYSTEM_RULE = (
    "You are a redactor. Return the EXACT input text with only PII spans replaced by dataset placeholders. "
    "Do NOT change any other words, punctuation, or casing. If unsure, keep. "
    "Wrap the final output inside <safe> and </safe>."
)

def build_prompt(user_text: str) -> str:
    return (
        f"{BOS}"
        f"{START}system{END}
{SYSTEM_RULE}
{EOT}"
        f"{START}user{END}
{user_text}
{EOT}"
        f"{START}assistant{END}
{SAFE_OPEN}"
    )

@torch.no_grad()
def redact_safe(text: str, max_new_tokens=96) -> str:
    prompt = build_prompt(text)
    inputs = tok(prompt, return_tensors="pt").to(model.device)
    out = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,                 # deterministic
        eos_token_id=tok.eos_token_id,
        pad_token_id=tok.pad_token_id,
    )
    decoded = tok.decode(out[0], skip_special_tokens=True)
    s = decoded.rfind(SAFE_OPEN)
    s = s + len(SAFE_OPEN) if s != -1 else 0
    e = decoded.find(SAFE_CLOSE, s)
    return decoded[s:e if e != -1 else None].strip()

print(redact_safe("Hi, I am John Doe. Email john@example.com and call +1 415 555 0199."))
```

## Results 
Evaluated on 300 random test samples:

* Exact match: ~0.67
* Placeholder micro-F1: ~ 0.90 (P~ 0.91, R~ 0.90)
* Formatting errors: ~ 0.00

These are strict metrics. Exact match drops when multiple placeholder choices are possible, while micro-F1 reflects span quality.

## Training set-up

* 4-bit load with bitsandbytes, LoRA rank 16, alpha 32, dropout 0.05
* Sequence length 320 to 512
* Batch size 1 with gradient accumulation 16
* Learning rate 2e-4, cosine schedule, warmup 3 percent
* Loss computed only on the assistant span between `<safe>` and `</safe>`

## Intended use

* Redacting PII in English text to placeholder labels for downstream processing or audit.
* Keep the non-PII text unchanged as much as possible.

## Limitations

* Placeholder choices can differ in close cases, for example `[DOB]` vs `[DATE]`.
* Non-English text is not covered here.
* Very long inputs should be chunked before redaction.

## License

Follow the licence of the base model for usage terms. The adapter is shared for research and practical use. Please ensure you handle personal data responsibly.