# Workflow Provenance Card: Inspect

## Summary
- **Workflow Name:** `Inspect`
- **Workflow ID:** `8474faec-bd9d-4b3e-8294-c4e8fbe865ed`
- **Campaign ID:** `970d7235-2e74-447d-a9d4-597f61d87618`
- **Execution Start (UTC):** `2026-02-25 20:04:23`
- **User:** `gabrielepadovani`
- **System Name:** `Darwin`

## Workflow-level Summary
- **Total Activities:** `6`
- **Status Counts:** `{'FINISHED': 7}`
- **Total Elapsed Workflow Time (s):** `unknown`
- **Resource Totals:**
  - `Memory Used`: `75.75 MB`

## Workflow Structure

```text
   input
     │
     ▼
 _inspect_data
     │
 _sample_file
     │
 _format_size
     │
 _infer_characteristics
     │
 _propose_pipeline
     │
 _generate_discovery_markdown
     ▼
   output
```

## Timing Report
Rows are sorted by **First Started At** (ascending).

| Activity | Status Counts | First Started At | Last Ended At | Median Elapsed (s) |
| --- | --- | --- | --- | --- |
| _inspect_data | {'FINISHED': 1} | 2026-02-25 20:04:23 | unknown | unknown |
| _sample_file | {'FINISHED': 1} | 2026-02-25 20:04:23 | unknown | unknown |
| _format_size | {'FINISHED': 2} | 2026-02-25 20:04:24 | unknown | unknown |
| _infer_characteristics | {'FINISHED': 1} | 2026-02-25 20:04:24 | unknown | unknown |
| _propose_pipeline | {'FINISHED': 1} | 2026-02-25 20:04:24 | unknown | unknown |
| _generate_discovery_markdown | {'FINISHED': 1} | 2026-02-25 20:04:24 | unknown | unknown |

### Interpretation & Insights
- No valid elapsed timings were available.

## Per Activity Details
- **_inspect_data**
  - Generated:
    - `file_count`: `1`
    - `files`: `[{"name": "tasmax_day_NorCPM1_historical_r1i1p1f1_gn_20240319_20240321_v20200724.nc", "path": "tasmax_day_NorCPM1_historical_r1i1p1f1_gn_20240319_20240321_v20200724.nc", "size": 150818, "suffix": ".nc"}]`
    - `formats`: `[".nc"]`
    - `sample_data..nc.error`: `llvmlite.binding.initialize() is deprecated and will be removed. LLVM initialization is now handled automatically. Please remove calls to...`
    - `sample_data..nc.format`: `.nc`
    - `sample_data..nc.path`: `tasmax_day_NorCPM1_historical_r1i1p1f1_gn_20240319_20240321_v20200724.nc`
    - `total_size`: `150818`
- **_sample_file**
  - Generated:
    - `error`: `llvmlite.binding.initialize() is deprecated and will be removed. LLVM initialization is now handled automatically. Please remove calls to...`
    - `format`: `.nc`
    - `path`: `tasmax_day_NorCPM1_historical_r1i1p1f1_gn_20240319_20240321_v20200724.nc`
- **_format_size** (`n=2`)
- **_infer_characteristics**
  - Generated:
    - `has_labels`: `False`
    - `has_splits`: `False`
    - `likely_domain`: `climate`
    - `modality`: `gridded`
    - `sparsity`: `None`
    - `suggested_format`: `zarr`
- **_propose_pipeline**
  - Generated:
    - `confidence`: `medium`
    - `notes`: `["No label column detected. This may be unsupervised or labels need to be added."]`
    - `output_format`: `zarr`
    - `pipeline_steps`: `[{"description": "Load gridded data from .nc", "name": "ingest", "stage": "ingest"}, {"description": "Regrid to uniform resolution", "name": "regrid", "stage": "preprocess"}, {"description": "Normalize to [0,1] or sta...`
- **_generate_discovery_markdown**

### Interpretation & Insights
- Activities with richest **generated** metadata: `_inspect_data` (7 fields), `_infer_characteristics` (6 fields), `_propose_pipeline` (4 fields)
- Highest numeric variability fields: `_inspect_data:generated.file_count` (range=0.000), `_inspect_data:generated.total_size` (range=0.000), `_infer_characteristics:generated.has_labels` (range=0.000), `_infer_characteristics:generated.has_splits` (range=0.000)

## Workflow-level Resource Usage
| Metric | Value |
| --- | --- |
| Telemetry Samples (task start/end pairs) | 7 |
| CPU User Time Delta | 0.000 |
| CPU System Time Delta | 0.000 |
| Average CPU Frequency | 3,228 |
| Memory Used Delta | 75.75 MB |
| Average Memory (%) | 56.4% |
| Disk Used Delta | 4.00 KB |
| Disk Read Time Delta (ms) | 0.000 |
| Disk Write Time Delta (ms) | 0.000 |
| Disk Busy Time Delta (ms) | 0.000 |
| Process CPU User Delta (s) | 1.512 |
| Process CPU System Delta (s) | 0.283 |
| Process Max RSS | 416.69 MB |
| Process Max VMS | 392.75 GB |
| Process Max Threads | 3 |
| Process Max Open Files | 1 |
| Process Max Open FDs | 7 |

### Interpretation & Insights
- Memory pressure (delta): `75.75 MB`; peak RSS: `416.69 MB`.
- Process-level pressure: cpu_user_delta=`1.512`, cpu_system_delta=`0.283`.

## Per-activity Resource Usage
| Activity | Elapsed (s) | CPU User (s) | CPU System (s) | Memory Delta |
| --- | --- | --- | --- | --- |
| _inspect_data | unknown | 0.000 | 0.000 | 37.88 MB |
| _sample_file | unknown | 0.000 | 0.000 | 37.88 MB |
| _format_size | unknown | 0.000 | 0.000 | - |
| _infer_characteristics | unknown | 0.000 | 0.000 | - |
| _propose_pipeline | unknown | 0.000 | 0.000 | - |
| _generate_discovery_markdown | unknown | 0.000 | 0.000 | - |

### Interpretation & Insights
- Largest memory growth Activities:
  - `_inspect_data`: Memory Delta=37.88 MB
  - `_sample_file`: Memory Delta=37.88 MB

## Aggregation Method
- Grouping key: `activity_id`.
- Each grouped row may aggregate multiple task records (`n_tasks`).
- Aggregated metrics currently include count/status/timing.

---
Provenance card generated by [Flowcept](https://flowcept.org/) | [GitHub](https://github.com/ORNL/flowcept) | [Version: 0.10.1](https://github.com/ORNL/flowcept/releases/tag/v0.10.1) on Feb 25, 2026 at 03:04 PM EST
