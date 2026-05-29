# Workflow Card Template

A structured template for documenting scientific / ML workflow runs. Each field has a description of what it should contain and is marked as **Required** or **Optional**.

Fields marked `~` indicate a value that was not captured; this is acceptable for optional fields.

---

## 1. Workflow

| Field | Required? | Description |
|---|---|---|
| `name` | Required | A short, human-readable name for this workflow. |
| `description` | Required | A plain-language summary of what the workflow does. Should be understandable without additional context. |

---

## 2. Summary

| Field | Required? | Description |
|---|---|---|
| `execution_id` | Required | A unique identifier for this specific run, typically a slug combining date, workflow name, and version. |
| `version` | Optional | The version tag of the workflow definition used for this run. |
| `started_at` | Required | timestamp marking when execution began. Should include the standard adopted. |
| `ended_at` | Required | timestamp marking when execution ended. Should include the standard adopted. |
| `duration` | Optional | Total wall-clock duration of the run. |
| `status` | Required | Overall status of the run (e.g. Completed, Failed, Partial). |
| `location` | Optional | Compute environment or cluster where the workflow executed. |
| `user` | Optional | Username or identity of the person who triggered the run. |
| `entrypoint.repository` | Required | URL or path to the main source code repository used for this run. |
| `entrypoint.branch` | Optional | The Git branch checked out at execution time. |
| `entrypoint.short_sha` | Optional | The abbreviated commit hash, uniquely identifying the exact code snapshot. |

---

## 3. Infrastructure

| Field | Required? | Description |
|---|---|---|
| `host_os` | Optional | Operating system and version running on the compute hosts. |
| `compute_hardware` | Required | Description of the physical hardware used (e.g. number and type of GPUs/CPUs). |
| `runtime_environment` | Optional | Container image, virtual environment, or execution runtime (e.g. a Docker image tag). |
| `resource_manager` | Optional | Job scheduler or resource manager used (e.g. Slurm, Kubernetes). |
| `primary_software` | Required | Key libraries and frameworks and their versions that the workflow depends on. |
| `environment_snapshot` | Optional | List or reference to a full environment export (e.g. a conda YAML or lock file) for reproducibility. |

---

## 4. Overview

A high-level picture of the run as a whole: what it did, how it performed, what it consumed, and anything worth noting. All narrative and aggregate information lives here before the reader descends into per-activity detail.

### 4.1 Run Summary

| Field | Required? | Description |
|---|---|---|
| `total_activities` | Required | Total number of distinct activity types (stages / steps) in the workflow. |
| `status_counts` | Required | Counts of tasks by their final status across all activities (e.g. finished, failed, skipped). |
| `arguments` | Optional | Global arguments or configuration flags that governed the entire run — anything affecting reproducibility such as random seeds, determinism flags, or boolean toggles. The set of keys is not prescribed; document whatever is relevant to your workflow. |
| `notable inputs` | Required if inputs exist | For each top-level input: its name/identifier, type or format, source path or reference, and an optional pointer to an associated data card or metadata file. |
| `notable outputs` | Optional | For each top-level output artifact: its name/identifier, type or format, storage location or reference, and any associated metadata. May be omitted if outputs are captured at the activity level instead. |
| `structure` | Optional | A visual or textual representation of how activities connect to each other. May be an ASCII-art DAG, a Mermaid diagram, a link to an image, or a numbered list of stages with their dependencies. |
| `observations` | Optional | Free-text section for the workflow operator. Record anything noteworthy about this specific run: anomalies, performance notes, decisions made mid-run, deviations from expected behaviour, or anything that would help a future reader understand the context of the results. |

### 4.2 Resource Usage

Aggregate resource consumption across all tasks and hosts. Report the dimensions your monitoring system captures; omit or mark `~` anything not measured. The specific metric names within each subsection are suggestions, not requirements.

| Field | Required? | Description |
|---|---|---|
| `cpu` | Optional | Aggregate CPU consumption. Relevant metrics may include total user/system time, average utilization percentage, and average clock frequency. |
| `memory` | Optional | Aggregate memory consumption. Relevant metrics may include net change in used memory, average utilization percentage, and swap usage. |
| `gpu` | Optional | Aggregate GPU metrics. Relevant metrics may include total GPU memory consumed and average temperature. Omit entirely if GPUs were not used. |
| `disk` | Optional | Aggregate disk I/O. Relevant metrics may include bytes read/written, number of read/write operations, and I/O timing. |
| `network` | Optional | Aggregate network transfer. Relevant metrics may include total inbound and outbound bytes. |

---

## 5. Activities

Repeat this block for each activity (stage / step) in the workflow. An activity may consist of a single task or many parallel / sequential tasks.

| Field | Required? | Description |
|---|---|---|
| `name` | Required | Unique name of this activity within the workflow. |
| `task_count` | Required | Total number of task instances spawned for this activity. |
| `started_at` | Required | Timestamp when the first task of this activity began. |
| `ended_at` | Required | Timestamp when the last task of this activity finished. |
| `duration` | Optional | Wall-clock duration from first task start to last task end. |
| `status` | Required | Counts of tasks by outcome (e.g. success: N, error: M). |
| `hosts` | Optional | For each compute host involved in this activity: its identifier, the number of tasks it ran, and its resource consumption. Use the same resource dimensions as section 4.2 (CPU, memory, GPU, disk, network), selecting whichever are relevant and measured. If only one host was used, a single block suffices. |
| `inputs` | Required if the activity has inputs | Describe the inputs consumed by this activity. For a single-task activity, report the exact value of each input parameter. For a multi-task activity, summarise the distribution of values across tasks (e.g. min, a central tendency, a high percentile, and max — or any other summary that captures the spread). Inputs identical across all tasks may be reported as a single value. |
| `outputs` | Required if the activity produces outputs | Describe the outputs produced by this activity using the same approach as inputs: exact values for single-task activities, a distribution summary for multi-task ones. |

---

## 6. Significant Artifacts

Repeat the input block for each significant input artifact, and the output block for each significant output artifact. List only the artifacts required to reproduce the run or to interpret its results.

### Input Artifact

| Field | Required? | Description |
|---|---|---|
| `name` | Required | A short identifier for this input artifact. |
| `description` | Required | Human-readable description of what this artifact is, including its format, origin, and relevance to the workflow. |
| `reference` | Required | Path, URI, or identifier that uniquely locates this artifact so it can be retrieved later. |

### Output Artifact

| Field | Required? | Description |
|---|---|---|
| `name` | Required | A short identifier for this output artifact. |
| `description` | Required | Human-readable description of what this artifact is, including its format and what it represents. |
| `reference` | Required | Path, URI, or identifier that uniquely locates this artifact so it can be retrieved later. |
