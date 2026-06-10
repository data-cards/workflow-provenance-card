# Workflow Cards Artifact Repository

This repository contains the public artifacts for the paper:

**Workflow Cards: Structured Summaries of Workflow Executions Using Provenance Data**

Workflow Cards are lightweight Markdown summaries of workflow executions generated from provenance data. They are designed to make workflow-level information easier to inspect directly and easier to use as context for large language model (LLM) question answering.

This repository provides:

- the Workflow Card template definition used during the paper;
- example Workflow Cards and companion Model/Data Cards;
- the Benchmark I question set, cards, and ground-truth answers;
- the Benchmark II question set and scripts for the [Flowcept](https://github.com/ORNL/flowcept/) and [yProvML](https://github.com/HPCI-Lab/yProv/) provenance pipeline;
- example LLM prompts used for answer evaluation;
- the code used to run the question-answering, judging, statistics, and plotting steps reported in the paper.

## Repository Layout

```text
.
├── templates/
│   └── WORKFLOW_CARD_TEMPLATE.md
├── dataset/
│   ├── cards/
│   │   ├── *_modelcard_pretrained.md
│   │   ├── *_datacard.md
│   │   ├── *_modelcard_finetuned.md
│   │   └── workflow_cards/
│   ├── gt/
│   ├── questions/
│   └── model_lineage.json
├── src/
│   ├── pipeline1/
│   ├── pipeline2/
│   ├── metrics_pipeline.py
│   └── utils.py
├── assets/
│   └── prompts/
└── requirements.txt
```

## What Is Included

### Template Definition

The canonical Workflow Card template used in the paper is:

```text
templates/WORKFLOW_CARD_TEMPLATE.md
```

The file includes embedded metadata declaring `version: v6`. The rendered template in the paper was generated from this structure. Older template iterations were removed from this artifact repository to keep a single public template definition.

### Benchmark I Artifacts

Benchmark I evaluates whether Workflow Cards expose execution-level information not already present in existing Model Cards and Data Cards.

Relevant files:

- `dataset/model_lineage.json`: five fine-tuning use cases used in the benchmark.
- `dataset/cards/*_modelcard_pretrained.md`: input Model Cards.
- `dataset/cards/*_datacard.md`: input Data Cards.
- `dataset/cards/*_modelcard_finetuned.md`: output/fine-tuned Model Cards.
- `dataset/cards/workflow_cards/*_workflow_card.md`: Workflow Cards generated for the benchmark.
- `dataset/questions/questions_bench_1.csv`: Benchmark I question set.
- `dataset/gt/*_answers.csv`: reference answers used for scoring.
- `assets/prompts/`: example LLM prompts used for answer evaluation.
- `src/pipeline1/`: scripts for card collection, card combinations, answer generation, judging, metrics, and plots.

### Benchmark II Artifacts

Benchmark II evaluates Workflow Cards as an LLM-facing representation of provenance for a scientific ML workflow instrumented with [Flowcept](https://github.com/ORNL/flowcept/) and [yProvML](https://github.com/HPCI-Lab/yProv/).

Relevant files:

- `dataset/questions/questions_bench_2.csv`: Benchmark II question set.
- `src/pipeline2/run_flowcept.py`: orchestrates the four-stage scientific ML workflow used to capture provenance.
- `src/pipeline2/convert_json2card.py`: converts [Flowcept](https://github.com/ORNL/flowcept/) and [yProvML](https://github.com/HPCI-Lab/yProv/) provenance records into Workflow Cards.
- `src/pipeline2/jsons2card.py`: helper to convert each captured provenance segment into cards.
- `src/pipeline2/generate_answers_gpt.py`: answers Benchmark II questions from the generated Workflow Card using local Ollama models.
- `src/pipeline2/generate_answers_agent.py`: answers Benchmark II questions through the schema-based provenance querying path.
- `src/pipeline2/generate_review_gpt.py`: LLM-as-a-Judge scoring for Benchmark II answers.
- `assets/prompts/`: example prompts for the LLM-as-a-Judge evaluation.

The Benchmark II scripts are the experiment code used for the paper. They assume local installations of [Flowcept](https://github.com/ORNL/flowcept/), [yProvML](https://github.com/HPCI-Lab/yProv/), REDI, PyTorch, Ollama, and the climate input data used by the workflow.

## Installation

Create and activate a Python environment, then install the base dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Some scripts require additional packages that are not listed in the minimal `requirements.txt`, depending on which part of the artifact you rerun:

- `huggingface_hub` for scraping Model/Data Cards;
- `matplotlib` and `seaborn` for plot generation;
- `ollama` and a running Ollama server for local LLM judging;
- `torch`, `xarray`, `flowcept`, `yprov4ml`, and REDI for Benchmark II provenance capture.

Several benchmark scripts were run in the original experiment checkout named `ProvenanceCards` and still contain that path prefix. If your checkout has a different directory name, either rename the checkout or create a local symlink before running the benchmark scripts:

```bash
ln -s . ProvenanceCards
```

## Reproducing Benchmark I

Run commands from the repository root.

1. Optionally refresh Hugging Face cards:

```bash
python src/pipeline1/01_scrape_cards.py
```

2. Generate all-card and leave-one-out card combinations:

```bash
python src/pipeline1/02_generate_card_combinations.py
```

3. Generate answers with the configured GPT/Azure endpoint:

```bash
python src/pipeline1/03_generate_answers_gpt.py
```

This script expects an API key in `.env` and currently contains the Azure OpenAI endpoint and deployment name used by the authors.

4. Score single-card and leave-one-out answers:

```bash
python src/pipeline1/04_create_results_dataset_oneonly.py
python src/pipeline1/04_create_results_dataset_loo.py
```

5. Generate paper figures:

```bash
python src/pipeline1/04_create_cards_stats.py
python src/pipeline1/04_create_cards_stats_aggr.py
python src/pipeline1/06_generate_plots.py
```

The scripts write derived outputs such as concatenated cards, answer files, result CSVs, analysis tables, and figures.

## Reproducing Benchmark II

Benchmark II requires the local scientific workflow environment used in the paper.

At minimum, install and configure:

- [Flowcept](https://github.com/ORNL/flowcept/);
- [yProvML](https://github.com/HPCI-Lab/yProv/);
- REDI;
- PyTorch;
- Ollama with the models used for answering and judging;
- the DLESyM/REDI input data referenced by the scripts.

Then run:

```bash
KMP_DUPLICATE_LIB_OK=TRUE python src/pipeline2/run_flowcept.py
```

This produces provenance under `pipeline2_output/jsons/` and related workflow outputs. Convert the captured provenance into Workflow Cards with:

```bash
python src/pipeline2/jsons2card.py
```

or directly:

```bash
python src/pipeline2/convert_json2card.py pipeline2_output/jsons/redi_yprov
python src/pipeline2/convert_json2card.py pipeline2_output/jsons/finetuning_yprov
python src/pipeline2/convert_json2card.py pipeline2_output/jsons/inference_yprov
python src/pipeline2/convert_json2card.py pipeline2_output/jsons/analysis_yprov
```

The generated cards are written to:

```text
pipeline2_output/provenancecards/
```

Benchmark II answer generation and judging use:

```bash
python src/pipeline2/generate_answers_gpt.py
python src/pipeline2/generate_answers_agent.py
python src/pipeline2/generate_review_gpt.py
```

These scripts assume local paths and services from the experiment environment. If your checkout directory differs from the original experiment path, use the `ProvenanceCards` symlink above or update the path constants in the scripts before running them.

## Notes on Reproducibility

The repository is intended as the artifact companion to the paper rather than a packaged Python library. The included datasets, cards, question sets, and scripts document the benchmark setup and support rerunning the experiments under the same local services.

The most portable artifacts are:

- `templates/WORKFLOW_CARD_TEMPLATE.md`;
- `dataset/cards/`;
- `dataset/questions/`;
- `dataset/gt/`;
- `assets/prompts/`;
- `src/pipeline1/`;
- `src/pipeline2/convert_json2card.py`.

Some full experiment reruns require external services or large local data that are not stored in this repository, including LLM endpoints, Ollama model weights, and the Benchmark II climate workflow inputs.

## Workflow Card Generators

The following provenance systems can automatically generate Workflow Cards from captured provenance data:

- [Flowcept](https://github.com/ORNL/flowcept/)
- [yProvML](https://github.com/HPCI-Lab/yProv/)

## Citation

If you use this repository, cite the paper:

```bibtex
@inproceedings{workflowcards2026,
  title  = {Workflow Cards: Structured Summaries of Workflow Executions Using Provenance Data},
  year   = {2026}
}
```

The final venue metadata will be added after publication.
