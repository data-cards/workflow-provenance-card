# Workflow Provenance Card: run_discover_GR0_0

## Summary

- **Experiment Name:** `run_discover_GR0_0`
- **Run ID:** `0`
- **Workflow / Process ID:** `cd063b80-7420-43f9-ab2b-44b7eed53c8b`
- **Campaign / Default Namespace:** `run_discover_GR0_0`
- **Global Rank:** `0`
- **Agent (User):** `gabrielepadovani`
- **Execution Start (UTC):** `2026-03-03 10:04:17 UTC`
- **Execution End (UTC):** `2026-03-03 10:04:19 UTC`
- **Total Elapsed:** `1.196 s`
- **Python Version:** `3.13.11 | packaged by Anaconda, Inc. | (main, Dec 10 2025, 21:21:08) [Clang 20.1.8 ]`
- **Experiment Directory:** `prov_save_path/run_discover_0`
- **Artifact URI:** `prov_save_path/run_discover_0/artifacts_GR0`
- **Provenance Path:** `prov_save_path`
- **Namespaces:** `yprov=https://github.com/HPCI-Lab/yProv4ML; xsd_1=http://www.w3.org/2000/10/XMLSchema#; provml=prov-ml; dcterms=http://purl.org/dc/terms/; default=run_discover_GR0_0`

## Dataset Characteristics

*Produced by the **Inspect** and **Infer** pipeline phases.*

### Inspection

- **File Count:** `4`
- **Total Input Size:** `2.13 MB`
- **Formats:** `['.txt']`

#### Input Files
| Filename          | Suffix | Size      |
| ----------------- | ------ | --------- |
| train.txt         | .txt   | 1.64 MB   |
| train_limited.txt | .txt   | 66.57 KB  |
| test_limited.txt  | .txt   | 16.64 KB  |
| test.txt          | .txt   | 418.59 KB |

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

| # | Stage  | Name   | Description                  |
| - | ------ | ------ | ---------------------------- |
| 1 | ingest | ingest | Load unknown data from .txt  |
| 2 | output | split  | Create train/val/test splits |
| 3 | output | save   | Save to npz format           |

### Notes & Caveats
- Could not confidently detect domain. Consider specifying with --domain.
- No label column detected. This may be unsupervised or labels need to be added.

## Activity Timeline

*Rows sorted by start time. Activities without an end time have elapsed marked `-`.*

| Activity   | Started At (UTC)        | Ended At (UTC)          | Elapsed | Tasks |
| ---------- | ----------------------- | ----------------------- | ------- | ----- |
| Inspect    | 2026-03-03 10:04:19 UTC | -                       | -       | 1     |
| Infer      | 2026-03-03 10:04:19 UTC | -                       | -       | 1     |
| Propose    | 2026-03-03 10:04:19 UTC | -                       | -       | 1     |
| Generation | 2026-03-03 10:04:19 UTC | 2026-03-03 10:04:19 UTC | -       | 1     |

## Per-Activity Hardware Metrics

*Observed values recorded at activity execution time via hardware monitors.*

| Activity | CPU Usage (%) | Disk Usage (GB) | GPU Memory Power (W) | GPU Memory Usage (GB) | GPU Power (W) | GPU Temp (°C) | GPU Usage (%) | Memory Usage (GB) |
| -------- | ------------- | --------------- | -------------------- | --------------------- | ------------- | ------------- | ------------- | ----------------- |
| Infer    | 0.0000        | 42.4000         | 0.0000               | 15.1394               | 0.0000        | 0.0000        | 0.0000        | 46.3000           |
| Inspect  | 0.0000        | 42.4000         | 0.0000               | 15.1394               | 0.0000        | 0.0000        | 12.0000       | 46.3000           |
| Propose  | 0.0000        | 42.4000         | 0.0000               | 15.3716               | 0.0000        | 0.0000        | 0.0000        | 46.3000           |

### Hardware Insights

- **CPU Usage (%)**: highest in `Infer` at `0.0000`.
- **Disk Usage (GB)**: highest in `Infer` at `42.4000`.
- **GPU Memory Power (W)**: highest in `Infer` at `0.0000`.
- **GPU Memory Usage (GB)**: highest in `Propose` at `15.3716`.
- **GPU Power (W)**: highest in `Infer` at `0.0000`.
- **GPU Temp (°C)**: highest in `Infer` at `0.0000`.
- **GPU Usage (%)**: highest in `Inspect` at `12.0000`.
- **Memory Usage (GB)**: highest in `Infer` at `46.3000`.

## Output Artifacts

| Filename              | Path                                      | Size    | Generated At (UTC)      |
| --------------------- | ----------------------------------------- | ------- | ----------------------- |
| discovery_report.json | output/data_c37da0c/discovery_report.json | 1.62 KB | 2026-03-03 10:04:19 UTC |

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
| Total Tracked Size       | 2.87 KB   |

---
Provenance card generated by [yProv4ML](https://github.com/HPCI-Lab/yProv4ML) / [Flowcept](https://flowcept.org/) | [GitHub](https://github.com/ORNL/flowcept) | Version: 0.10.1 | Mar 03, 2026 at 10:04 AM EST
