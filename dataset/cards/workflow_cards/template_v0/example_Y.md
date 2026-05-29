# Workflow Provenance Card: run_discover_GR0_22

## Summary

- **Experiment Name:** `run_discover_GR0_22`
- **Run ID:** `22`
- **Workflow / Process ID:** `4dc5ff9f-9803-4f0d-90b2-eea3b75b3377`
- **Campaign / Default Namespace:** `run_discover_GR0_22`
- **Global Rank:** `0`
- **Agent (User):** `gabrielepadovani`
- **Execution Start (UTC):** `2026-02-25 15:04:22 UTC`
- **Execution End (UTC):** `2026-02-25 15:04:24 UTC`
- **Total Elapsed:** `2.087 s`
- **Python Version:** `3.13.11 | packaged by Anaconda, Inc. | (main, Dec 10 2025, 21:21:08) [Clang 20.1.8 ]`
- **Experiment Directory:** `prov_save_path/run_discover_22`
- **Artifact URI:** `prov_save_path/run_discover_22/artifacts_GR0`
- **Provenance Path:** `prov_save_path`
- **Namespaces:** `yprov=https://github.com/HPCI-Lab/yProv4ML; xsd_1=http://www.w3.org/2000/10/XMLSchema#; provml=prov-ml; dcterms=http://purl.org/dc/terms/; default=run_discover_GR0_22`

## Dataset Characteristics

*Produced by the **Inspect** and **Infer** pipeline phases.*

### Inspection

- **File Count:** `1`
- **Total Input Size:** `147.28 KB`
- **Formats:** `['.nc']`

#### Input Files
| Filename                                                                 | Suffix | Size      |
| ------------------------------------------------------------------------ | ------ | --------- |
| tasmax_day_NorCPM1_historical_r1i1p1f1_gn_20240319_20240321_v20200724.nc | .nc    | 147.28 KB |

### Inference

- **Modality:** `gridded`
- **Likely Domain:** `climate`
- **Has Labels:** `False`
- **Has Splits:** `False`
- **Suggested Storage Format:** `zarr`

## ML Pipeline Proposal

*Produced by the **Propose** pipeline phase.*

- **Recommended Output Format:** `zarr`
- **Confidence Level:** `medium`

### Proposed Pipeline Steps

| # | Stage      | Name      | Description                       |
| - | ---------- | --------- | --------------------------------- |
| 1 | ingest     | ingest    | Load gridded data from .nc        |
| 2 | preprocess | regrid    | Regrid to uniform resolution      |
| 3 | transform  | normalize | Normalize to [0,1] or standardize |
| 4 | output     | split     | Create train/val/test splits      |
| 5 | output     | save      | Save to zarr format               |

### Notes & Caveats
- No label column detected. This may be unsupervised or labels need to be added.

## Activity Timeline

*Rows sorted by start time. Activities without an end time have elapsed marked `-`.*

| Activity   | Started At (UTC)        | Ended At (UTC)          | Elapsed | Tasks |
| ---------- | ----------------------- | ----------------------- | ------- | ----- |
| Inspect    | 2026-02-25 15:04:24 UTC | -                       | -       | 1     |
| Infer      | 2026-02-25 15:04:24 UTC | -                       | -       | 1     |
| Propose    | 2026-02-25 15:04:24 UTC | -                       | -       | 1     |
| Generation | 2026-02-25 15:04:24 UTC | 2026-02-25 15:04:24 UTC | -       | 1     |

## Per-Activity Hardware Metrics

*Observed values recorded at activity execution time via hardware monitors.*

| Activity | CPU Usage (%) | Disk Usage (GB) | GPU Memory Power (W) | GPU Memory Usage (GB) | GPU Power (W) | GPU Temp (°C) | GPU Usage (%) | Memory Usage (GB) |
| -------- | ------------- | --------------- | -------------------- | --------------------- | ------------- | ------------- | ------------- | ----------------- |
| Infer    | 0.0000        | 42.8000         | 0.0000               | 15.1573               | 0.0000        | 0.0000        | 0.0000        | 56.4000           |
| Inspect  | 0.0000        | 42.8000         | 0.0000               | 15.1573               | 0.0000        | 0.0000        | 10.0000       | 56.4000           |
| Propose  | 0.0000        | 42.8000         | 0.0000               | 15.3891               | 0.0000        | 0.0000        | 0.0000        | 56.4000           |

### Hardware Insights

- **CPU Usage (%)**: highest in `Infer` at `0.0000`.
- **Disk Usage (GB)**: highest in `Infer` at `42.8000`.
- **GPU Memory Power (W)**: highest in `Infer` at `0.0000`.
- **GPU Memory Usage (GB)**: highest in `Propose` at `15.3891`.
- **GPU Power (W)**: highest in `Infer` at `0.0000`.
- **GPU Temp (°C)**: highest in `Infer` at `0.0000`.
- **GPU Usage (%)**: highest in `Inspect` at `10.0000`.
- **Memory Usage (GB)**: highest in `Infer` at `56.4000`.

## Output Artifacts

| Filename              | Path                                                                                                       | Size    | Generated At (UTC)      |
| --------------------- | ---------------------------------------------------------------------------------------------------------- | ------- | ----------------------- |
| discovery_report.json | output/tasmax_day_NorCPM1_historical_r1i1p1f1_gn_20240319_20240321_v20200724_5db3d9b/discovery_report.json | 1.90 KB | 2026-02-25 15:04:24 UTC |

## Provenance Lineage

### Activity Dependencies (`wasInformedBy`)

| Activity          | Informed By         |
| ----------------- | ------------------- |
| Inspect           | run_discover_GR0_22 |
| Infer             | run_discover_GR0_22 |
| Propose           | run_discover_GR0_22 |
| Generation        | run_discover_GR0_22 |
| apple_gpu/Inspect | Inspect             |
| apple_gpu/Infer   | Infer               |
| apple_gpu/Propose | Propose             |

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

| Generated Entity                     | Derived From                                  |
| ------------------------------------ | --------------------------------------------- |
| discovery_report.json/Generation     | Original_discovery_report.json/Generation     |
| DISCOVERY_REPORT.md/Generation       | Original_DISCOVERY_REPORT.md/Generation       |
| requirements.txt/run_discover_GR0_22 | Original_requirements.txt/run_discover_GR0_22 |

### Entity Usage (`used`)

| Activity            | Entity Used                                   |
| ------------------- | --------------------------------------------- |
| run_discover_GR0_22 | Original_requirements.txt/run_discover_GR0_22 |
| run_discover_GR0_22 | requirements.txt/run_discover_GR0_22          |

## Object Artifacts Summary

| Metric                   | Value     |
| ------------------------ | --------- |
| Total Objects            | 25        |
| Metric Files             | 24        |
| Output Files             | 1         |
| Hardware Monitor Sources | apple_gpu |
| Total Tracked Size       | 3.15 KB   |

---
Provenance card generated by [yProv4ML](https://github.com/HPCI-Lab/yProv4ML) / [Flowcept](https://flowcept.org/) | [GitHub](https://github.com/ORNL/flowcept) | Version: 0.10.1 | Feb 25, 2026 at 03:04 PM EST
