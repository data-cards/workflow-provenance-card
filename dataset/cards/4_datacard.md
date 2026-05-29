---
license: odc-by
language:
- en
configs:
- config_name: MOPD
  data_files:
  - split: train
    path: MOPD/train.jsonl
- config_name: multi-domain-RL
  data_files:
  - split: train
    path: multi-domain-RL/train.jsonl
- config_name: IF-RL
  data_files:
  - split: train
    path: IF-RL/train.jsonl
- config_name: SWE-RL
  data_files:
  - split: train
    path: SWE-RL/train.jsonl
---

## Dataset Description:

The Nemotron-Cascade-2-RL dataset is a curated reinforcement learning (RL) dataset blend used to train Nemotron-Cascade-2-30B-A3B model. It includes instruction-following RL, multi-domain RL, on-policy distillation, and software engineering RL (SWE-RL) data.

This dataset is ready for commercial use.

The dataset contains the following subset:

### IF-RL

Contains 45,879 training samples for instruction-following RL. Our curation process mainly resolves formatting inconsistencies within the keyword arguments for certain instruction types (e.g., `count_increment_word`). 

This sub dataset is from [nvidia/Nemotron-RL-instruction_following](https://huggingface.co/datasets/nvidia/Nemotron-RL-instruction_following).

### Multi-domain-RL

Contains 18,147 training samples spanning multi-domain tasks, including Multi-choice Question Answering (MCQA), workplace assistant, and structured output for instruction following.

The datasets are from:
- [nvidia/Nemotron-RL-knowledge-mcqa](https://huggingface.co/datasets/nvidia/Nemotron-RL-knowledge-mcqa) (55%)
- [nvidia/Nemotron-RL-agent-workplace_assistant](https://huggingface.co/datasets/nvidia/Nemotron-RL-agent-workplace_assistant) (30%)
- [nvidia/Nemotron-RL-instruction_following-structured_outputs](https://huggingface.co/datasets/nvidia/Nemotron-RL-instruction_following-structured_outputs) (15%)

### Multi-domain on-policy distillation

Contains **6171** data instances, covering data sources from AceReason-Math, instruction following, structured outputs, stem MCQA, and Workplace assistant.

| Data Source            | Count |
|------------------------|------:|
| AceReason-Math         | 1853  |
| Instruction Following  | 1854  |
| Workplace              | 610   |
| STEM                   | 927   |
| Structured Outputs     | 927   | 

The datasets are from:
- [nvidia/AceReason-Math](https://huggingface.co/datasets/nvidia/AceReason-Math)
- [nvidia/Nemotron-RL-instruction_following](https://huggingface.co/datasets/nvidia/Nemotron-RL-instruction_following)
- [nvidia/Nemotron-RL-knowledge-mcqa](https://huggingface.co/datasets/nvidia/Nemotron-RL-knowledge-mcqa) 
- [nvidia/Nemotron-RL-agent-workplace_assistant](https://huggingface.co/datasets/nvidia/Nemotron-RL-agent-workplace_assistant)
- [nvidia/Nemotron-RL-instruction_following-structured_outputs](https://huggingface.co/datasets/nvidia/Nemotron-RL-instruction_following-structured_outputs)

### SWE-RL

Contains 3,612 training samples for software engineering RL workflows.

The datasets are from:
- [SWE-Gym/SWE-Gym](https://huggingface.co/datasets/SWE-Gym/SWE-Gym) (20%)
- [R2E-Gym/R2E-Gym-Subset](https://huggingface.co/datasets/R2E-Gym/R2E-Gym-Subset) (80%)


## Dataset Creation Date:

Created on: Mar 19, 2026

## License/Terms of Use:

The dataset is governed by the [Open Data Commons Attribution License (ODC-By) v1.0](https://opendatacommons.org/licenses/by/1-0/).

## Intended Usage:

This dataset is intended to be used by the community to train and evaluate RL and instruction-following models. The data may be freely used to train and evaluate.

## Dataset Characterization

**Data Collection Method**  
Hybrid: Human, Synthetic, Automated

**Labeling Method**  
Hybrid: Human, Synthetic, Automated

## Dataset Format

Modality: Text  
Format: JSONL  
Structure: Text + Metadata  

**Columns:**

- Core columns (all subsets):
  - `responses_create_params`: Input payload and generation settings
  - `agent_ref`: Agent metadata used for generation/evaluation
  - `dataset`: Dataset/source identifier (available in subsets that include dataset-level tags)
- Common additional columns (subset-dependent):
  - `prompt`, `instruction_id_list`, `kwargs`, `id`, `category`, `environment_name`, `ground_truth`
  - `pass_rate`, `pass_rate_total`, `pass_rate_passed`
  - `metadata`, `model`, `temperature` (under `responses_create_params`)

## Dataset Quantification


| Subset          | Samples |
| --------------- | ------- |
| MOPD            | 6,171   |
| multi-domain-RL | 18,147  |
| IF-RL           | 45,879  |
| SWE-RL          | 3,612   |
| Total           | 73,809  |


Total Disk Size: ~2.73 GB

## Ethical Considerations:

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications.  When downloaded or used in accordance with our terms of service, developers should work with their internal developer teams to ensure this dataset meets requirements for the relevant industry and use case and addresses unforeseen product misuse.  
Please report quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

---
license: other
license_name: nvidia-open-model-license
license_link: https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/
configs:
- config_name: math
  data_files:
  - split: train
    path: math/*
- config_name: science
  data_files:
  - split: train
    path: science/*
- config_name: chat
  data_files:
  - split: train
    path: chat/*
- config_name: instruction_following
  data_files:
  - split: train
    path: instruction_following/*
- config_name: safety
  data_files:
  - split: train
    path: safety/*
- config_name: conversational_agent
  data_files:
  - split: train
    path: conversational_agent/*
- config_name: swe
  data_files:
  - split: train
    path: swe/*
- config_name: terminal_agent
  data_files:
  - split: train
    path: terminal_agent/*
---


# Nemotron-Cascade-2-SFT-Data
We release the SFT data used for training [Nemotron-Cascade-2](https://huggingface.co/nvidia/Nemotron-Cascade-2-30B-A3B).


## Data sources

#### Math
Our non-proof math prompts are sourced from [Nemotron-Cascade-1-SFT](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-SFT-Stage-2) and [Nemotron-Math-v2](https://huggingface.co/datasets/nvidia/Nemotron-Math-v2), with responses generated by DeepSeek-V3.2, DeepSeek-V3.2-Speciale, and GPT-OSS-120B. For mathematical proofs, prompts are taken from [Nemotron-Math-Proofs-v1](https://huggingface.co/datasets/nvidia/Nemotron-Math-Proofs-v1) and generated using DeepSeek-V3.2-Speciale.


#### Science
We collect science prompts from [Nemotron-Cascade-1-SFT](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-SFT-Stage-2) and [Nemotron-Science-v1](https://huggingface.co/datasets/nvidia/Nemotron-Science-v1), coving physics, chemistry, and biology. Responses are generated by GPT-OSS-120B.


#### General Chat
We source general chat samples from [Nemotron-Cascade-1-SFT](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-SFT-Stage-2) and [Nemotron-Instruction-Following-Chat-v1](https://huggingface.co/datasets/nvidia/Nemotron-Instruction-Following-Chat-v1).


#### Instruction Following
The samples are sourced from [Nemotron-Cascade-1-SFT](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-SFT-Stage-2) and [Nemotron-Instruction-Following-Chat-v1](https://huggingface.co/datasets/nvidia/Nemotron-Instruction-Following-Chat-v1).


#### Safety
The samples are sourced from [Nemotron-SFT-Safety-v1](https://huggingface.co/datasets/nvidia/Nemotron-SFT-Safety-v1).


#### Conversational Agent
The prompts are sourced from [Nemotron-Agentic-v1](https://huggingface.co/datasets/nvidia/Nemotron-Agentic-v1) and [Nemotron-RL-Agentic-Conversational-Tool-Use-Pivot-v1](https://huggingface.co/datasets/nvidia/Nemotron-RL-Agentic-Conversational-Tool-Use-Pivot-v1), with responses generated by Qwen3-235B-A22B-Thinking-2507, Qwen3-32B, Qwen3-235B-A22B-Instruct-2507, and GPT-OSS-120B.


#### Software Engineering Agent
We collect agentless samples from [Nemotron-Cascade-1-SFT-SWE](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-1-SFT-SWE), covering buggy code localization, code repair, and test case generation. Agentic samples are drawn from [SWE-Gym](https://huggingface.co/datasets/SWE-Gym/SWE-Gym), [SWE-rebench](https://huggingface.co/datasets/nebius/SWE-rebench), and [R2E-Gym-Subset](https://huggingface.co/datasets/R2E-Gym/R2E-Gym-Subset).


#### Terminal Agent
The samples are sourced from [Nemotron-Terminal-Corpus](https://huggingface.co/datasets/nvidia/Nemotron-Terminal-Corpus).


## Training

We pack all SFT samples into sequences of up to 256K tokens and train the model in a single stage. Empirically, we find that the SFT model reaches optimal performance after approximately 1.5 epochs.

| Hyperparameters |  |
| :--- | :---: |
| Global Batch Size | 64 |
| Packed Sequence Length | 256K |
| Max Learning Rate | 5e-5 |
| Min Learning Rate | 5e-6 |
| Learning Rate Warmup Steps | 200 |
| Scheduler | cosine |
| Max Steps | 40,000 |
| Optimizer | AdamW  |
| Optimizer Config | beta_1=0.9<br>beta_2=0.98 |
| Weight Decay | 0.1 |
| # of training steps | 33,000 |


## Statistics

| Domain | # Samples |
| :--- | :---: |
| Math | 5,226,364 |
| Science | 2,717,163 |
| General Chat | 13,972,873 |
| Instruction Following | 820,263 |
| Safety | 3,570 |
| Conversational Agent | 822,213 |
| Software Engineering Agent | 439,610 |
| Terminal Agent | 822,213 |


## Release Date
Mar 19, 2026


## License
Your use of this model is governed by the [NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/).


## Citation
```
@article{Nemotron_Cascade_2,
  title={Nemotron-Cascade 2: Post-Training LLMs with Cascade RL and Multi-Domain On-Policy Distillation},
  author={Yang, Zhuolin and Liu, Zihan and Chen, Yang and Dai, Wenliang and Wang, Boxin and Lin, Sheng-Chieh and Lee, Chankyu and Chen, Yangyi and Jiang, Dongfu and He, Jiafan and Pi, Renjie and Lam, Grace and Lee, Nayeon and Bukharin, Alexander and Shoeybi, Mohammad and Catanzaro, Bryan and Ping, Wei},
  year={2026}
}
```
