# Workflow Provenance Card: Inspect

## Summary
- **Workflow Name:** `Inspect`
- **Workflow ID:** `a9df97d0-a9f1-4ca7-aa1a-a21e41a7570e`
- **Campaign ID:** `fb675635-e6a2-4640-ad34-6f8983ddbdfb`
- **Execution Start (UTC):** `2026-03-03 15:04:19`
- **User:** `gabrielepadovani`
- **System Name:** `Darwin`

## Workflow-level Summary
- **Total Activities:** `6`
- **Status Counts:** `{'FINISHED': 7}`
- **Total Elapsed Workflow Time (s):** `unknown`
- **Resource Totals:**
  - `Memory Used`: `48.00 KB`

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
| _inspect_data | {'FINISHED': 1} | 2026-03-03 15:04:19 | unknown | unknown |
| _sample_file | {'FINISHED': 1} | 2026-03-03 15:04:19 | unknown | unknown |
| _format_size | {'FINISHED': 2} | 2026-03-03 15:04:19 | unknown | unknown |
| _infer_characteristics | {'FINISHED': 1} | 2026-03-03 15:04:19 | unknown | unknown |
| _propose_pipeline | {'FINISHED': 1} | 2026-03-03 15:04:19 | unknown | unknown |
| _generate_discovery_markdown | {'FINISHED': 1} | 2026-03-03 15:04:19 | unknown | unknown |

### Interpretation & Insights
- No valid elapsed timings were available.

## Per Activity Details
- **_inspect_data**
  - Generated:
    - `file_count`: `4`
    - `files`: `[{"name": "train.txt", "path": "data/train.txt", "size": 1714528, "suffix": ".txt"}, {"name": "train_limited.txt", "path": "data/train_limited.txt", "size": 68166, "suffix": ".txt"}, {"name": "test_limited.txt", "path...`
    - `formats`: `[".txt"]`
    - `sample_data..txt.format`: `.txt`
    - `sample_data..txt.path`: `data/train.txt`
    - `total_size`: `2228366`
- **_sample_file**
  - Generated:
    - `format`: `.txt`
    - `path`: `data/train.txt`
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
    - `pipeline_steps`: `[{"description": "Load unknown data from .txt", "name": "ingest", "stage": "ingest"}, {"description": "Create train/val/test splits", "name": "split", "stage": "output"}, {"description": "Save to npz format", "name": ...`
- **_generate_discovery_markdown**

### Interpretation & Insights
- Activities with richest **generated** metadata: `_inspect_data` (6 fields), `_infer_characteristics` (6 fields), `_propose_pipeline` (4 fields)
- Highest numeric variability fields: `_inspect_data:generated.file_count` (range=0.000), `_inspect_data:generated.total_size` (range=0.000), `_infer_characteristics:generated.has_labels` (range=0.000), `_infer_characteristics:generated.has_splits` (range=0.000)

## Workflow-level Resource Usage
| Metric | Value |
| --- | --- |
| Telemetry Samples (task start/end pairs) | 7 |
| CPU User Time Delta | 0.000 |
| CPU System Time Delta | 0.000 |
| Average CPU Frequency | 3,228 |
| Memory Used Delta | 48.00 KB |
| Average Memory (%) | 46.3% |
| Disk Read Time Delta (ms) | 0.000 |
| Disk Write Time Delta (ms) | 0.000 |
| Disk Busy Time Delta (ms) | 0.000 |
| Network Sent | 1.00 KB |
| Network Received | 84.00 KB |
| Network Packets Sent | 16 |
| Network Packets Received | 115 |
| Process CPU User Delta (s) | 0.006 |
| Process CPU System Delta (s) | 0.009 |
| Process Max RSS | 325.80 MB |
| Process Max VMS | 392.61 GB |
| Process Max Threads | 3 |
| Process Max Open FDs | 6 |

### Interpretation & Insights
- Memory pressure (delta): `48.00 KB`; peak RSS: `325.80 MB`.
- Network movement: sent `1.00 KB`, received `84.00 KB`.
- Process-level pressure: cpu_user_delta=`0.006`, cpu_system_delta=`0.009`.

## Per-activity Resource Usage
| Activity | Elapsed (s) | CPU User (s) | CPU System (s) | Memory Delta |
| --- | --- | --- | --- | --- |
| _inspect_data | unknown | 0.000 | 0.000 | 32.00 KB |
| _sample_file | unknown | 0.000 | 0.000 | 16.00 KB |
| _format_size | unknown | 0.000 | 0.000 | - |
| _infer_characteristics | unknown | 0.000 | 0.000 | - |
| _propose_pipeline | unknown | 0.000 | 0.000 | - |
| _generate_discovery_markdown | unknown | 0.000 | 0.000 | - |

### Interpretation & Insights
- Largest memory growth Activities:
  - `_inspect_data`: Memory Delta=32.00 KB
  - `_sample_file`: Memory Delta=16.00 KB
- Most network-active Activities:
  - `_inspect_data`: Sent=1.00 KB, Received=52.00 KB
  - `_format_size`: Sent=-, Received=21.00 KB
  - `_sample_file`: Sent=-, Received=11.00 KB

## Aggregation Method
- Grouping key: `activity_id`.
- Each grouped row may aggregate multiple task records (`n_tasks`).
- Aggregated metrics currently include count/status/timing.

---
Provenance card generated by [Flowcept](https://flowcept.org/) | [GitHub](https://github.com/ORNL/flowcept) | [Version: 0.10.1](https://github.com/ORNL/flowcept/releases/tag/v0.10.1) on Mar 03, 2026 at 10:04 AM EST
