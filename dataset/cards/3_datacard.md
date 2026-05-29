---
language:
- en
- fr
- de
- it
task_categories:
- text-classification
- token-classification
- table-question-answering
- question-answering
- zero-shot-classification
- summarization
- feature-extraction
- text-generation
- text2text-generation
- translation
- fill-mask
- tabular-classification
- tabular-to-text
- table-to-text
- text-retrieval
- other
multilinguality:
- multilingual
tags:
- legal
- business
- psychology
- privacy
size_categories:
- 100K<n<1M
pretty_name: Ai4Privacy PII200k Dataset
source_datasets:
- original
configs:
- config_name: default
  data_files: '*.jsonl'
---

# Ai4Privacy Community

Join our community at https://discord.gg/FmzWshaaQT to help build open datasets for privacy masking.

# Purpose and Features


Previous world's largest open dataset for privacy. Now it is [pii-masking-300k](https://huggingface.co/datasets/ai4privacy/pii-masking-300k)

The purpose of the dataset is to train models to remove personally identifiable information (PII) from text, especially in the context of AI assistants and LLMs. 


The example texts have **54 PII classes** (types of sensitive data), targeting **229 discussion subjects / use cases** split across business, education, psychology and legal fields, and 5 interactions styles (e.g. casual conversation, formal document, emails etc...).

Key facts:

- Size: 13.6m text tokens in ~209k examples with 649k PII tokens (see [summary.json](summary.json))
- 4 languages, more to come!
  - English
  - French
  - German
  - Italian
- Synthetic data generated using proprietary algorithms
  - No privacy violations!
- Human-in-the-loop validated high quality dataset

# Getting started


Option 1: Python
```terminal
  pip install datasets
```
```python
from datasets import load_dataset
dataset = load_dataset("ai4privacy/pii-masking-200k")
```

# Token distribution across PII classes

We have taken steps to balance the token distribution across PII classes covered by the dataset.
This graph shows the distribution of observations across the different PII classes in this release:

![Token distribution across PII classes](pii_class_count_histogram.png)

There is 1 class that is still overrepresented in the dataset: firstname.
We will further improve the balance with future dataset releases.
This is the token distribution excluding the FIRSTNAME class:

![Token distribution across PII classes excluding `FIRSTNAME`](pii_class_count_histogram_without_FIRSTNAME.png)

# Compatible Machine Learning Tasks:
- Tokenclassification. Check out a HuggingFace's [guide on token classification](https://huggingface.co/docs/transformers/tasks/token_classification).
  - [ALBERT](https://huggingface.co/docs/transformers/model_doc/albert), [BERT](https://huggingface.co/docs/transformers/model_doc/bert), [BigBird](https://huggingface.co/docs/transformers/model_doc/big_bird), [BioGpt](https://huggingface.co/docs/transformers/model_doc/biogpt), [BLOOM](https://huggingface.co/docs/transformers/model_doc/bloom), [BROS](https://huggingface.co/docs/transformers/model_doc/bros), [CamemBERT](https://huggingface.co/docs/transformers/model_doc/camembert), [CANINE](https://huggingface.co/docs/transformers/model_doc/canine), [ConvBERT](https://huggingface.co/docs/transformers/model_doc/convbert), [Data2VecText](https://huggingface.co/docs/transformers/model_doc/data2vec-text), [DeBERTa](https://huggingface.co/docs/transformers/model_doc/deberta), [DeBERTa-v2](https://huggingface.co/docs/transformers/model_doc/deberta-v2), [DistilBERT](https://huggingface.co/docs/transformers/model_doc/distilbert), [ELECTRA](https://huggingface.co/docs/transformers/model_doc/electra), [ERNIE](https://huggingface.co/docs/transformers/model_doc/ernie), [ErnieM](https://huggingface.co/docs/transformers/model_doc/ernie_m), [ESM](https://huggingface.co/docs/transformers/model_doc/esm), [Falcon](https://huggingface.co/docs/transformers/model_doc/falcon), [FlauBERT](https://huggingface.co/docs/transformers/model_doc/flaubert), [FNet](https://huggingface.co/docs/transformers/model_doc/fnet), [Funnel Transformer](https://huggingface.co/docs/transformers/model_doc/funnel), [GPT-Sw3](https://huggingface.co/docs/transformers/model_doc/gpt-sw3), [OpenAI GPT-2](https://huggingface.co/docs/transformers/model_doc/gpt2), [GPTBigCode](https://huggingface.co/docs/transformers/model_doc/gpt_bigcode), [GPT Neo](https://huggingface.co/docs/transformers/model_doc/gpt_neo), [GPT NeoX](https://huggingface.co/docs/transformers/model_doc/gpt_neox), [I-BERT](https://huggingface.co/docs/transformers/model_doc/ibert), [LayoutLM](https://huggingface.co/docs/transformers/model_doc/layoutlm), [LayoutLMv2](https://huggingface.co/docs/transformers/model_doc/layoutlmv2), [LayoutLMv3](https://huggingface.co/docs/transformers/model_doc/layoutlmv3), [LiLT](https://huggingface.co/docs/transformers/model_doc/lilt), [Longformer](https://huggingface.co/docs/transformers/model_doc/longformer), [LUKE](https://huggingface.co/docs/transformers/model_doc/luke), [MarkupLM](https://huggingface.co/docs/transformers/model_doc/markuplm), [MEGA](https://huggingface.co/docs/transformers/model_doc/mega), [Megatron-BERT](https://huggingface.co/docs/transformers/model_doc/megatron-bert), [MobileBERT](https://huggingface.co/docs/transformers/model_doc/mobilebert), [MPNet](https://huggingface.co/docs/transformers/model_doc/mpnet), [MPT](https://huggingface.co/docs/transformers/model_doc/mpt), [MRA](https://huggingface.co/docs/transformers/model_doc/mra), [Nezha](https://huggingface.co/docs/transformers/model_doc/nezha), [Nyströmformer](https://huggingface.co/docs/transformers/model_doc/nystromformer), [QDQBert](https://huggingface.co/docs/transformers/model_doc/qdqbert), [RemBERT](https://huggingface.co/docs/transformers/model_doc/rembert), [RoBERTa](https://huggingface.co/docs/transformers/model_doc/roberta), [RoBERTa-PreLayerNorm](https://huggingface.co/docs/transformers/model_doc/roberta-prelayernorm), [RoCBert](https://huggingface.co/docs/transformers/model_doc/roc_bert), [RoFormer](https://huggingface.co/docs/transformers/model_doc/roformer), [SqueezeBERT](https://huggingface.co/docs/transformers/model_doc/squeezebert), [XLM](https://huggingface.co/docs/transformers/model_doc/xlm), [XLM-RoBERTa](https://huggingface.co/docs/transformers/model_doc/xlm-roberta), [XLM-RoBERTa-XL](https://huggingface.co/docs/transformers/model_doc/xlm-roberta-xl), [XLNet](https://huggingface.co/docs/transformers/model_doc/xlnet), [X-MOD](https://huggingface.co/docs/transformers/model_doc/xmod), [YOSO](https://huggingface.co/docs/transformers/model_doc/yoso)
- Text Generation: Mapping the unmasked_text to to the masked_text or privacy_mask attributes. Check out HuggingFace's [guide to fine-tunning](https://huggingface.co/docs/transformers/v4.15.0/training)
  - [T5 Family](https://huggingface.co/docs/transformers/model_doc/t5), [Llama2](https://huggingface.co/docs/transformers/main/model_doc/llama2)

# Information regarding the rows:
- Each row represents a json object with a natural language text that includes placeholders for PII (and could plausibly be written by a human to an AI assistant).

- Sample row:
  - "source_text" (previously "unmasked_text") shows a natural sentence generally containing PII
    - "Product officially launching in Washington County. Estimate profit of $488293.16. Expenses by Checking Account.",
  - "target_text" (previously "masked_text") contains a PII free natural text
    - "Product officially launching in [COUNTY]. Estimate profit of [CURRENCYSYMBOL][AMOUNT]. Expenses by [ACCOUNTNAME]."
  - "privacy_mask" indicates the mapping between the privacy token instances and the string within the natural text. It contains the information explicit format for privacy mask labels
    - [{"value": "Washington County", "start": 32, "end": 49, "label": "COUNTY"}, {"value": "$", "start": 70, "end": 71, "label": "CURRENCYSYMBOL"}, {"value": "488293.16", "start": 71, "end": 80, "label": "AMOUNT"}, {"value": "Checking Account", "start": 94, "end": 110, "label": "ACCOUNTNAME"}]
  - "span_labels" is an array of arrays formatted in the following way [start, end, pii token instance].*
    - "[[0, 32, \"O\"], [32, 49, \"COUNTY\"], [49, 70, \"O\"], [70, 71, \"CURRENCYSYMBOL\"], [71, 80, \"AMOUNT\"], [80, 94, \"O\"], [94, 110, \"ACCOUNTNAME\"], [110, 111, \"O\"]]",
  - "mbert_bio_labels" follows the common place notation for "beginning", "inside" and "outside" of where each private tokens starts.[original paper](https://arxiv.org/abs/cmp-lg/9505040)
    - ["O", "O", "O", "O", "O", "B-COUNTY", "I-COUNTY", "O", "O", "O", "O", "O", "B-CURRENCYSYMBOL", "B-AMOUNT", "I-AMOUNT", "I-AMOUNT", "I-AMOUNT", "I-AMOUNT", "I-AMOUNT", "O", "O", "O", "O", "B-ACCOUNTNAME", "I-ACCOUNTNAME", "I-ACCOUNTNAME", "O"]
  - "mbert_text_tokens" breaks down the unmasked sentence into tokens using Bert Family tokeniser to help fine-tune large language models.
    - ["Product", "officially", "launch", "##ing", "in", "Washington", "County", ".", "Esti", "##mate", "profit", "of", "$", "488", "##2", "##9", "##3", ".", "16", ".", "Ex", "##penses", "by", "Check", "##ing", "Account", "."]

  - Additional meta data: "id": 176510, "language": "en", "set": "train".

*note for the nested objects, we store them as string to maximise compability between various software.

# About Us:

At Ai4Privacy, we are commited to building the global seatbelt of the 21st century for Artificial Intelligence to help fight against potential risks of personal information being integrated into data pipelines.

Newsletter & updates: [www.Ai4Privacy.com](www.Ai4Privacy.com)
- Looking for ML engineers, developers, beta-testers, human in the loop validators (all languages)
- Integrations with already existing open solutions
- Ask us a question on discord: [https://discord.gg/kxSbJrUQZF](https://discord.gg/kxSbJrUQZF)

# Roadmap and Future Development

- Carbon Neutral
- Benchmarking
- Better multilingual and especially localisation
- Extended integrations
- Continuously increase the training set
- Further optimisation to the model to reduce size and increase generalisability 
- Next released major update is planned for the 14th of December 2023 (subscribe to newsletter for updates)

# Use Cases and Applications

**Chatbots**: Incorporating a PII masking model into chatbot systems can ensure the privacy and security of user conversations by automatically redacting sensitive information such as names, addresses, phone numbers, and email addresses.

**Customer Support Systems**: When interacting with customers through support tickets or live chats, masking PII can help protect sensitive customer data, enabling support agents to handle inquiries without the risk of exposing personal information.

**Email Filtering**: Email providers can utilize a PII masking model to automatically detect and redact PII from incoming and outgoing emails, reducing the chances of accidental disclosure of sensitive information.

**Data Anonymization**: Organizations dealing with large datasets containing PII, such as medical or financial records, can leverage a PII masking model to anonymize the data before sharing it for research, analysis, or collaboration purposes.

**Social Media Platforms**: Integrating PII masking capabilities into social media platforms can help users protect their personal information from unauthorized access, ensuring a safer online environment.

**Content Moderation**: PII masking can assist content moderation systems in automatically detecting and blurring or redacting sensitive information in user-generated content, preventing the accidental sharing of personal details.

**Online Forms**: Web applications that collect user data through online forms, such as registration forms or surveys, can employ a PII masking model to anonymize or mask the collected information in real-time, enhancing privacy and data protection.

**Collaborative Document Editing**: Collaboration platforms and document editing tools can use a PII masking model to automatically mask or redact sensitive information when multiple users are working on shared documents.

**Research and Data Sharing**: Researchers and institutions can leverage a PII masking model to ensure privacy and confidentiality when sharing datasets for collaboration, analysis, or publication purposes, reducing the risk of data breaches or identity theft.

**Content Generation**: Content generation systems, such as article generators or language models, can benefit from PII masking to automatically mask or generate fictional PII when creating sample texts or examples, safeguarding the privacy of individuals.

(...and whatever else your creative mind can think of)

# Support and Maintenance

AI4Privacy is a project affiliated with [AISuisse SA](https://www.aisuisse.com/).