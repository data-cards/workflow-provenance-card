# Workflow Provenance Card: Inspect

## Summary
- **Workflow Name:** `Inspect`
- **Workflow ID:** `3cfbf01a-9678-4c87-aed8-295db90a39aa`
- **Campaign ID:** `a97ebdf4-5e57-47f2-977d-872145a3aad1`
- **Execution Start (UTC):** `2026-03-03 15:11:49`
- **User:** `gabrielepadovani`
- **System Name:** `Darwin`

## Workflow-level Summary
- **Total Activities:** `6`
- **Status Counts:** `{'FINISHED': 7}`
- **Total Elapsed Workflow Time (s):** `unknown`
- **Resource Totals:**
  - `Memory Used`: `784.00 KB`
  - **IO:**
    - `Write`: `544.00 KB`
    - `Write Ops`: `120`
- **Key Observations:**
  - Largest IO Activity: `_inspect_data` with Read `-` and Write `272.00 KB`

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
| _inspect_data | {'FINISHED': 1} | 2026-03-03 15:11:49 | unknown | unknown |
| _sample_file | {'FINISHED': 1} | 2026-03-03 15:11:49 | unknown | unknown |
| _format_size | {'FINISHED': 2} | 2026-03-03 15:11:49 | unknown | unknown |
| _infer_characteristics | {'FINISHED': 1} | 2026-03-03 15:11:49 | unknown | unknown |
| _propose_pipeline | {'FINISHED': 1} | 2026-03-03 15:11:49 | unknown | unknown |
| _generate_discovery_markdown | {'FINISHED': 1} | 2026-03-03 15:11:49 | unknown | unknown |

### Interpretation & Insights
- No valid elapsed timings were available.

## Per Activity Details
- **_inspect_data**
  - Generated:
    - `file_count`: `1190`
    - `files`: `[{"name": "AuAu200_170kHz_10C_Iter2_3147.xml_TPCMLDataInterface_6.npy", "path": "fusion/AuAu200_170kHz_10C_Iter2_3147.xml_TPCMLDataInterface_6.npy", "size": 1529984, "suffix": ".npy"}, {"name": "AuAu200_170kHz_10C_Ite...`
    - `formats`: `[".npy"]`
    - `sample_data..npy.dtype`: `uint16`
    - `sample_data..npy.format`: `.npy`
    - `sample_data..npy.path`: `fusion/AuAu200_170kHz_10C_Iter2_3147.xml_TPCMLDataInterface_6.npy`
    - `sample_data..npy.shape`: `[192, 249, 16]`
    - `total_size`: `152998400`
- **_sample_file**
  - Generated:
    - `dtype`: `uint16`
    - `format`: `.npy`
    - `path`: `fusion/AuAu200_170kHz_10C_Iter2_3147.xml_TPCMLDataInterface_6.npy`
    - `shape`: `[192, 249, 16]`
- **_format_size** (`n=2`)
- **_infer_characteristics**
  - Generated:
    - `has_labels`: `False`
    - `has_splits`: `False`
    - `likely_domain`: `general`
    - `modality`: `sequence_or_image`
    - `sparsity`: `None`
    - `suggested_format`: `npz`
- **_propose_pipeline**
  - Generated:
    - `confidence`: `low`
    - `notes`: `["Could not confidently detect domain. Consider specifying with --domain.", "No label column detected. This may be unsupervised or labels need to be added."]`
    - `output_format`: `npz`
    - `pipeline_steps`: `[{"description": "Load sequence_or_image data from .npy", "name": "ingest", "stage": "ingest"}, {"description": "Create train/val/test splits", "name": "split", "stage": "output"}, {"description": "Save to npz format"...`
- **_generate_discovery_markdown**

### Interpretation & Insights
- Activities with richest **generated** metadata: `_inspect_data` (8 fields), `_infer_characteristics` (6 fields), `_sample_file` (4 fields)
- Highest numeric variability fields: `_inspect_data:generated.file_count` (range=0.000), `_inspect_data:generated.total_size` (range=0.000), `_infer_characteristics:generated.has_labels` (range=0.000), `_infer_characteristics:generated.has_splits` (range=0.000)

## Workflow-level Resource Usage
| Metric | Value |
| --- | --- |
| Telemetry Samples (task start/end pairs) | 7 |
| CPU User Time Delta | 0.030 |
| CPU System Time Delta | 0.010 |
| Average CPU Frequency | 3,228 |
| Memory Used Delta | 784.00 KB |
| Average Memory (%) | 45.6% |
| Disk Read Time Delta (ms) | 0.000 |
| Disk Write Time Delta (ms) | 4.000 |
| Disk Busy Time Delta (ms) | 0.000 |
| Process CPU User Delta (s) | 0.009 |
| Process CPU System Delta (s) | 0.014 |
| Process Max RSS | 328.23 MB |
| Process Max VMS | 392.73 GB |
| Process Max Threads | 3 |
| Process Max Open FDs | 6 |

### Interpretation & Insights
- Memory pressure (delta): `784.00 KB`; peak RSS: `328.23 MB`.
- Disk IO pressure: read `-`, write `544.00 KB`.
- Process-level pressure: cpu_user_delta=`0.009`, cpu_system_delta=`0.014`.

## Per-activity Resource Usage
| Activity | Elapsed (s) | CPU User (s) | CPU System (s) | Memory Delta | Write | Write Ops |
| --- | --- | --- | --- | --- | --- | --- |
| _inspect_data | unknown | 0.020 | 0.010 | 768.00 KB | 272.00 KB | 60 |
| _sample_file | unknown | 0.010 | 0.000 | 16.00 KB | 272.00 KB | 60 |
| _format_size | unknown | 0.000 | 0.000 | - | - | - |
| _infer_characteristics | unknown | 0.000 | 0.000 | - | - | - |
| _propose_pipeline | unknown | 0.000 | 0.000 | - | - | - |
| _generate_discovery_markdown | unknown | 0.000 | 0.000 | - | - | - |

### Interpretation & Insights
- Most IO-heavy Activities (Read + Write):
  - `_inspect_data`: Read=-, Write=272.00 KB
  - `_sample_file`: Read=-, Write=272.00 KB
- Largest memory growth Activities:
  - `_inspect_data`: Memory Delta=768.00 KB
  - `_sample_file`: Memory Delta=16.00 KB

## Aggregation Method
- Grouping key: `activity_id`.
- Each grouped row may aggregate multiple task records (`n_tasks`).
- Aggregated metrics currently include count/status/timing.

---
Provenance card generated by [Flowcept](https://flowcept.org/) | [GitHub](https://github.com/ORNL/flowcept) | [Version: 0.10.1](https://github.com/ORNL/flowcept/releases/tag/v0.10.1) on Mar 03, 2026 at 10:11 AM EST
