# Workflow Provenance Card: run_discover_GR0_0

## Summary

- **Experiment Name:** `run_discover_GR0_0`
- **Run ID:** `0`
- **Workflow / Process ID:** `faa94b2a-01da-4861-966b-89e31d5385e1`
- **Campaign / Default Namespace:** `run_discover_GR0_0`
- **Global Rank:** `0`
- **Agent (User):** `gabrielepadovani`
- **Execution Start (UTC):** `2026-03-03 10:16:29 UTC`
- **Execution End (UTC):** `2026-03-03 10:16:30 UTC`
- **Total Elapsed:** `1.179 s`
- **Python Version:** `3.13.11 | packaged by Anaconda, Inc. | (main, Dec 10 2025, 21:21:08) [Clang 20.1.8 ]`
- **Experiment Directory:** `prov_save_path/run_discover_0`
- **Artifact URI:** `prov_save_path/run_discover_0/artifacts_GR0`
- **Provenance Path:** `prov_save_path`
- **Namespaces:** `yprov=https://github.com/HPCI-Lab/yProv4ML; xsd_1=http://www.w3.org/2000/10/XMLSchema#; provml=prov-ml; dcterms=http://purl.org/dc/terms/; default=run_discover_GR0_0`

## Dataset Characteristics

*Produced by the **Inspect** and **Infer** pipeline phases.*

### Inspection

- **File Count:** `1`
- **Total Input Size:** `257.00 MB`
- **Formats:** `['.040000']`

#### Input Files
| Filename    | Suffix  | Size      |
| ----------- | ------- | --------- |
| p_28.040000 | .040000 | 257.00 MB |

### Inference

- **Likely Domain:** `general`
- **Has Labels:** `False`
- **Has Splits:** `False`
- **Suggested Storage Format:** `npz`

## ML Pipeline Proposal

*Produced by the **Propose** pipeline phase.*

- **Recommended Output Format:** `npz`
- **Confidence Level:** `low`

### Proposed Pipeline Steps

| # | Stage  | Name   | Description                    |
| - | ------ | ------ | ------------------------------ |
| 1 | ingest | ingest | Load unknown data from .040000 |
| 2 | output | split  | Create train/val/test splits   |
| 3 | output | save   | Save to npz format             |

### Notes & Caveats
- Could not confidently detect domain. Consider specifying with --domain.
- No label column detected. This may be unsupervised or labels need to be added.

## Activity Timeline

*Rows sorted by start time. Activities without an end time have elapsed marked `-`.*

| Activity   | Started At (UTC)        | Ended At (UTC)          | Elapsed | Tasks |
| ---------- | ----------------------- | ----------------------- | ------- | ----- |
| Inspect    | 2026-03-03 10:16:30 UTC | -                       | -       | 1     |
| Infer      | 2026-03-03 10:16:30 UTC | -                       | -       | 1     |
| Propose    | 2026-03-03 10:16:30 UTC | -                       | -       | 1     |
| Generation | 2026-03-03 10:16:30 UTC | 2026-03-03 10:16:30 UTC | -       | 1     |

## Per-Activity Hardware Metrics

*Observed values recorded at activity execution time via hardware monitors.*

| Activity | CPU Usage (%) | Disk Usage (GB) | GPU Memory Power (W) | GPU Memory Usage (GB) | GPU Power (W) | GPU Temp (°C) | GPU Usage (%) | Memory Usage (GB) |
| -------- | ------------- | --------------- | -------------------- | --------------------- | ------------- | ------------- | ------------- | ----------------- |
| Infer    | 0.0000        | 42.9000         | 0.0000               | 11.5277               | 0.0000        | 0.0000        | 0.0000        | 47.7000           |
| Inspect  | 0.0000        | 42.9000         | 0.0000               | 11.2888               | 0.0000        | 0.0000        | 18.0000       | 47.7000           |
| Propose  | 0.0000        | 42.9000         | 0.0000               | 11.7618               | 0.0000        | 0.0000        | 0.0000        | 47.7000           |

### Hardware Insights

- **CPU Usage (%)**: highest in `Infer` at `0.0000`.
- **Disk Usage (GB)**: highest in `Infer` at `42.9000`.
- **GPU Memory Power (W)**: highest in `Infer` at `0.0000`.
- **GPU Memory Usage (GB)**: highest in `Propose` at `11.7618`.
- **GPU Power (W)**: highest in `Infer` at `0.0000`.
- **GPU Temp (°C)**: highest in `Infer` at `0.0000`.
- **GPU Usage (%)**: highest in `Inspect` at `18.0000`.
- **Memory Usage (GB)**: highest in `Infer` at `47.7000`.

## Output Artifacts

| Filename              | Path                                                    | Size    | Generated At (UTC)      |
| --------------------- | ------------------------------------------------------- | ------- | ----------------------- |
| discovery_report.json | redi_discovery/turbolence_2807555/discovery_report.json | 1.26 KB | 2026-03-03 10:16:30 UTC |

## Provenance Lineage

### Activity Dependencies (`wasInformedBy`)

| Activity          | Informed By        |
| ----------------- | ------------------ |
| Inspect           | run_discover_GR0_0 |
| Infer             | run_discover_GR0_0 |
| Propose           | run_discover_GR0_0 |
| Generation        | run_discover_GR0_0 |
| apple_gpu/Inspect | Inspect            |
| apple_gpu/Infer   | Infer              |
| apple_gpu/Propose | Propose            |

### Entity Generation (`wasGeneratedBy`)

| Activity          | Entities Produced | Examples                                                                                                               |
| ----------------- | ----------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Generation        | 4                 | Original_discovery_report.json/Generation, discovery_report.json/Generation, Original_DISCOVERY_REPORT.md/Generation … |
| Infer             | 6                 | modality, likely_domain, has_labels …                                                                                  |
| Inspect           | 5                 | files, total_size, formats …                                                                                           |
| Propose           | 4                 | pipeline_steps, output_format, confidence …                                                                            |
| apple_gpu/Infer   | 8                 | apple_gpu/cpu_usage/Infer, apple_gpu/memory_usage/Infer, apple_gpu/disk_usage/Infer …                                  |
| apple_gpu/Inspect | 8                 | apple_gpu/cpu_usage/Inspect, apple_gpu/memory_usage/Inspect, apple_gpu/disk_usage/Inspect …                            |
| apple_gpu/Propose | 8                 | apple_gpu/cpu_usage/Propose, apple_gpu/memory_usage/Propose, apple_gpu/disk_usage/Propose …                            |

### Entity Derivations (`wasDerivedFrom`)

| Generated Entity                    | Derived From                                 |
| ----------------------------------- | -------------------------------------------- |
| discovery_report.json/Generation    | Original_discovery_report.json/Generation    |
| DISCOVERY_REPORT.md/Generation      | Original_DISCOVERY_REPORT.md/Generation      |
| requirements.txt/run_discover_GR0_0 | Original_requirements.txt/run_discover_GR0_0 |

### Entity Usage (`used`)

| Activity           | Entity Used                                  |
| ------------------ | -------------------------------------------- |
| run_discover_GR0_0 | Original_requirements.txt/run_discover_GR0_0 |
| run_discover_GR0_0 | requirements.txt/run_discover_GR0_0          |

## Object Artifacts Summary

| Metric                   | Value     |
| ------------------------ | --------- |
| Total Objects            | 25        |
| Metric Files             | 24        |
| Output Files             | 1         |
| Hardware Monitor Sources | apple_gpu |
| Total Tracked Size       | 2.50 KB   |

---
Provenance card generated by [yProv4ML](https://github.com/HPCI-Lab/yProv4ML) / [Flowcept](https://flowcept.org/) | [GitHub](https://github.com/ORNL/flowcept) | Version: 0.10.1 | Mar 03, 2026 at 10:16 AM EST
