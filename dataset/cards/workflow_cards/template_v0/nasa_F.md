# Workflow Provenance Card: Inspect

## Summary
- **Workflow Name:** `Inspect`
- **Workflow ID:** `1332c1f4-fbf8-4c95-b1b7-d03227a95119`
- **Campaign ID:** `046c70d4-2cbf-4845-8407-9f339aff7e9b`
- **Execution Start (UTC):** `2026-03-03 15:14:31`
- **User:** `gabrielepadovani`
- **System Name:** `Darwin`

## Workflow-level Summary
- **Total Activities:** `6`
- **Status Counts:** `{'FINISHED': 7}`
- **Total Elapsed Workflow Time (s):** `unknown`
- **Resource Totals:**
  - `Average CPU (%)`: `12.3%`
  - **IO:**
    - `Read`: `16.00 KB`
    - `Write`: `200.00 KB`
    - `Read Ops`: `4`
    - `Write Ops`: `20`
- **Key Observations:**
  - Largest IO Activity: `_inspect_data` with Read `8.00 KB` and Write `100.00 KB`

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
| _inspect_data | {'FINISHED': 1} | 2026-03-03 15:14:31 | unknown | unknown |
| _sample_file | {'FINISHED': 1} | 2026-03-03 15:14:31 | unknown | unknown |
| _format_size | {'FINISHED': 2} | 2026-03-03 15:14:38 | unknown | unknown |
| _infer_characteristics | {'FINISHED': 1} | 2026-03-03 15:14:38 | unknown | unknown |
| _propose_pipeline | {'FINISHED': 1} | 2026-03-03 15:14:38 | unknown | unknown |
| _generate_discovery_markdown | {'FINISHED': 1} | 2026-03-03 15:14:38 | unknown | unknown |

### Interpretation & Insights
- No valid elapsed timings were available.

## Per Activity Details
- **_inspect_data**
  - Generated:
    - `file_count`: `1`
    - `files`: `[{"name": "usa_0_data.json", "path": "nasa/usa_0_data.json", "size": 593618502, "suffix": ".json"}]`
    - `formats`: `[".json"]`
    - `sample_data..json.first_item_keys`: `["features", "header", "messages", "parameters", "times", "type"]`
    - `sample_data..json.format`: `.json`
    - `sample_data..json.length`: `157`
    - `sample_data..json.path`: `nasa/usa_0_data.json`
    - `sample_data..json.type`: `array`
- **_sample_file**
  - Generated:
    - `first_item_keys`: `["features", "header", "messages", "parameters", "times", "type"]`
    - `format`: `.json`
    - `length`: `157`
    - `path`: `nasa/usa_0_data.json`
    - `type`: `array`
- **_format_size** (`n=2`)
- **_infer_characteristics**
  - Generated:
    - `has_labels`: `False`
    - `has_splits`: `False`
    - `likely_domain`: `general`
    - `modality`: `unknown`
    - `sparsity`: `None`
    - `suggested_format`: `npz`
- **_propose_pipeline**
  - Generated:
    - `confidence`: `low`
    - `notes`: `["Could not confidently detect domain. Consider specifying with --domain.", "No label column detected. This may be unsupervised or labels need to be added."]`
    - `output_format`: `npz`
    - `pipeline_steps`: `[{"description": "Load unknown data from .json", "name": "ingest", "stage": "ingest"}, {"description": "Create train/val/test splits", "name": "split", "stage": "output"}, {"description": "Save to npz format", "name":...`
- **_generate_discovery_markdown**

### Interpretation & Insights
- Activities with richest **generated** metadata: `_inspect_data` (9 fields), `_infer_characteristics` (6 fields), `_sample_file` (5 fields)
- Highest numeric variability fields: `_inspect_data:generated.file_count` (range=0.000), `_inspect_data:generated.sample_data..json.length` (range=0.000), `_sample_file:generated.length` (range=0.000), `_infer_characteristics:generated.has_labels` (range=0.000), `_infer_characteristics:generated.has_splits` (range=0.000)

## Workflow-level Resource Usage
| Metric | Value |
| --- | --- |
| Telemetry Samples (task start/end pairs) | 7 |
| CPU User Time Delta | 13.280 |
| CPU System Time Delta | 1.700 |
| Average CPU (%) Delta | 12.3% |
| Average CPU Frequency | 3,228 |
| Average Memory (%) | 47.7% |
| Disk Used Delta | 128.00 KB |
| Disk Read Time Delta (ms) | 2.000 |
| Disk Write Time Delta (ms) | 4.000 |
| Disk Busy Time Delta (ms) | 0.000 |
| Network Sent | 10.00 KB |
| Network Received | 4.00 KB |
| Network Packets Sent | 50 |
| Network Packets Received | 44 |
| Process CPU User Delta (s) | 11.497 |
| Process CPU System Delta (s) | 0.731 |
| Process Max RSS | 386.33 MB |
| Process Max VMS | 392.78 GB |
| Process Max Threads | 2 |
| Process Max Open FDs | 6 |

### Interpretation & Insights
- CPU-heavy period (avg delta): `12.3%`.
- Disk IO pressure: read `16.00 KB`, write `200.00 KB`.
- Network movement: sent `10.00 KB`, received `4.00 KB`.
- Process-level pressure: cpu_user_delta=`11.497`, cpu_system_delta=`0.731`.

## Per-activity Resource Usage
| Activity | Elapsed (s) | CPU User (s) | CPU System (s) | CPU (%) | Read | Write | Read Ops | Write Ops |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| _inspect_data | unknown | 6.640 | 0.850 | - | 8.00 KB | 100.00 KB | 2 | 10 |
| _sample_file | unknown | 6.640 | 0.850 | 12.3% | 8.00 KB | 100.00 KB | 2 | 10 |
| _format_size | unknown | 0.000 | 0.000 | - | - | - | - | - |
| _infer_characteristics | unknown | 0.000 | 0.000 | - | - | - | - | - |
| _propose_pipeline | unknown | 0.000 | 0.000 | - | - | - | - | - |
| _generate_discovery_markdown | unknown | 0.000 | 0.000 | - | - | - | - | - |

### Interpretation & Insights
- Most IO-heavy Activities (Read + Write):
  - `_inspect_data`: Read=8.00 KB, Write=100.00 KB
  - `_sample_file`: Read=8.00 KB, Write=100.00 KB
- Most CPU-active Activities:
  - `_sample_file`: CPU=12.3%
- Most network-active Activities:
  - `_inspect_data`: Sent=5.00 KB, Received=2.00 KB
  - `_sample_file`: Sent=5.00 KB, Received=2.00 KB

## Aggregation Method
- Grouping key: `activity_id`.
- Each grouped row may aggregate multiple task records (`n_tasks`).
- Aggregated metrics currently include count/status/timing.

---
Provenance card generated by [Flowcept](https://flowcept.org/) | [GitHub](https://github.com/ORNL/flowcept) | [Version: 0.10.1](https://github.com/ORNL/flowcept/releases/tag/v0.10.1) on Mar 03, 2026 at 10:14 AM EST
