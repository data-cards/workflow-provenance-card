

<div align="center">
  <a href="https://github.com/HPCI-Lab">
    <img src="./assets/HPCI_Logo-t.png" alt="HPCI Lab Logo" width="100" height="100">
  </a>

  <h3 align="center">Provenance Cards</h3>

  <p align="center">
    A meaningful description
    <br />
    <!-- <a href="https://hpci-lab.github.io/yProv4ML/"><strong>Explore the docs »</strong></a> -->
    <br />
    <br />
    <a href="https://github.com/HPCI-Lab/ProvenanceCards/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/HPCI-Lab/ProvenanceCards/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<br />

<div align="center">
  
[![Contributors](https://img.shields.io/github/contributors/HPCI-Lab/ProvenanceCards?style=for-the-badge)](https://github.com/HPCI-Lab/ProvenanceCards/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/HPCI-Lab/ProvenanceCards?style=for-the-badge)](https://github.com/HPCI-Lab/ProvenanceCards/network/members)
[![Stars](https://img.shields.io/github/stars/HPCI-Lab/ProvenanceCards?style=for-the-badge)](https://github.com/HPCI-Lab/ProvenanceCards/stargazers)
[![Issues](https://img.shields.io/github/issues/HPCI-Lab/ProvenanceCards?style=for-the-badge)](https://github.com/HPCI-Lab/ProvenanceCards/issues)
[![GPLv3 License](https://img.shields.io/badge/LICENCE-GPL3.0-green?style=for-the-badge)](https://opensource.org/licenses/)

</div>

A more in depth intrdouction to the repo and the benchmark

### Install

Requires [Ollama](https://ollama.com/download) and a decent gpu

```bash
pip install -r requirements.txt
```

### Running

Create inference files (summaries of processes from provenance card or json): 

```bash
python src/main.py
```

Compute statistics from inference run: 

```bash
python src/analyze.py outputs/*run_folder*
```


### Models 

- Qwen2.5-Coder-7B
- Llama-3.2-3B
- Phi-4-Mini
- Mistral-7B-v0.3

### Datasets

### Metrics

- Coverage: percentage of provenance attributes mentioned
  Check how many provenance attributes from a checklist are mentioned in the model's description.

- Hallucination: percentage of claims not supported by source text
  What fraction of the model's claims are NOT supported by the source?
  Right now it's just a lexical check: a claim is 'supported' if enough of its content words appear in the source text.

- Consistency: Pairwise cosine similarity between chunk summaries (High consistency if the model produces coherent descriptions across chunks)

- ROUGE-L F1: ROUGE-L Score against a reference

- Tokens to coverage: How many tokens before quality threshold is reached?


### TODO

- add provenance to inference
- viz dashboard with correct "lower is better / higher is better"
- more analysis?
- better reference for text gold standard 