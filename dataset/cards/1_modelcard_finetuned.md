---
license: llama3.2
datasets:
- avaliev/chat_doctor
language:
- en
base_model:
- meta-llama/Llama-3.2-3B-Instruct
pipeline_tag: text-generation
library_name: transformers
tags:
- Llama-3.2
- 3B
- Llama-Doctor
- Instruct
- Llama-Cpp
- meta
- pytorch
- safetensors
- Doctor-Llama
---

## Llama-Doctor-3.2-3B-Instruct Modelfile

The **Llama-Doctor-3.2-3B-Instruct** model is designed for **text generation** tasks, particularly in contexts where instruction-following capabilities are needed. This model is a fine-tuned version of the base **Llama-3.2-3B-Instruct** model and is optimized for understanding and responding to user-provided instructions or prompts. The model has been trained on a specialized dataset, **avaliev/chat_doctor**, to enhance its performance in providing conversational or advisory responses, especially in medical or technical fields.

| File Name          { Chat Doctor }                    | Size       | Description                          | Upload Status  |
|----------------------------------------|------------|--------------------------------------|----------------|
| `.gitattributes`                       | 1.57 kB    | Git attributes file                  | Uploaded       |
| `README.md`                            | 263 Bytes  | README file                          | Uploaded       |
| `config.json`                          | 1.03 kB    | Model configuration                  | Uploaded       |
| `generation_config.json`               | 248 Bytes  | Generation configuration             | Uploaded       |
| `pytorch_model-00001-of-00002.bin`     | 4.97 GB    | PyTorch model file (part 1 of 2)     | Uploaded (LFS) |
| `pytorch_model-00002-of-00002.bin`     | 1.46 GB    | PyTorch model file (part 2 of 2)     | Uploaded (LFS) |
| `pytorch_model.bin.index.json`         | 21.2 kB    | Index for PyTorch model              | Uploaded       |
| `special_tokens_map.json`              | 477 Bytes  | Special tokens map                   | Uploaded       |
| `tokenizer.json`                       | 17.2 MB    | Tokenizer file                       | Uploaded (LFS) |
| `tokenizer_config.json`                | 57.4 kB    | Tokenizer configuration              | Uploaded       |

| Model Type | Size | Context Length | Link |
|------------|------|----------------|------|
| GGUF | 3B | - | [🤗 Llama-Doctor-3.2-3B-Instruct-GGUF](https://huggingface.co/prithivMLmods/Llama-Doctor-3.2-3B-Instruct-GGUF) |

### Key Use Cases:
1. **Conversational AI**: Engage in dialogue, answering questions, or providing responses based on user instructions.
2. **Text Generation**: Generate content, summaries, explanations, or solutions to problems based on given prompts.
3. **Instruction Following**: Understand and execute instructions, potentially in complex or specialized domains like medical, technical, or academic fields.

The model leverages a **PyTorch-based architecture** and comes with various files such as configuration files, tokenizer files, and special tokens maps to facilitate smooth deployment and interaction.

### Intended Applications:
- **Chatbots** for customer support or virtual assistants.
- **Medical Consultation Tools** for generating advice or answering medical queries (given its training on the **chat_doctor** dataset).
- **Content Creation** tools, helping generate text based on specific instructions.
- **Problem-solving Assistants** that offer explanations or answers to user queries, particularly in instructional contexts.