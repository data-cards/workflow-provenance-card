# Provenance Card Template — v4
*A standardized framework for documenting the execution history of computational workflows*
*Inspired by Datasheets for Datasets (Gebru et al., 2018) and Model Cards (Mitchell et al., 2019)*

---

## What This Card Documents

The subject of a Provenance Card is a **workflow execution**: a bounded run of one or more activities that consumed inputs and produced outputs. Artifacts (datasets, models, files) appear in the card as *inputs to* or *outputs of* that execution — they are not the subject themselves. If you need to document an artifact in isolation, use a Datasheet or Model Card. Use this card to explain *how it came to be*.

A provenance card is not a provenance document. It is a curated, human-readable summary produced from a provenance document by a named author who is accountable for its content. As a consequence:

- A card may contain only a subset of the information in the underlying provenance document.
- A card may be enriched with information not present in the provenance document, clearly attributed as such.
- A card must never contradict the provenance document it is derived from.
- A card is a historical record of a specific execution. It should not be updated to reflect changes that occurred after that execution (e.g. a license change on an input dataset).

---

## How to Use This Template

This file is the **template**: it contains all fields, their descriptions, annotation levels, and filling guidance. It is not itself a provenance card.

To produce a card:

1. Copy the template.
2. Remove this preamble (everything up to and including the "Field Reference" section) and all `Description` column content — the filled card contains only sections, fields, annotation levels, source tags, and values.
3. Fill each field according to the guidelines below.
4. For repeating sections (§4 Inputs, §5 Execution Record, §6 Outputs), instantiate one block per artifact or activity, replacing `[N]` with a sequential number and `<name>` with a short identifier.
5. Complete the Coverage Statistics table last.

---

## Field Reference

### Annotation — obligation level

| Tag | Meaning |
|-----|---------|
| **[R]** Required | Must be present for the card to be valid. Absence makes the card unidentifiable, untrustworthy, or materially misleading. If a required field genuinely cannot be filled, state explicitly why rather than leaving it blank. |
| **[Rec]** Recommended | Should be filled in most circumstances. Omission is legitimate when the information is genuinely unavailable, but must not be silent — add a brief note explaining why (e.g. `[not captured by provenance tool]`, `[not applicable — no human labor involved]`). |
| **[O]** Optional | Useful in specific contexts. Omit freely when not applicable; no justification required. |

### Source — origin of the value

Fill the Source column for every field you populate. Choose one tag from the enum below, optionally followed by a parenthetical explanation when the derivation is non-obvious.

| Tag | Meaning |
|-----|---------|
| `[prov_doc]` | Value is taken directly from the provenance document, as-is or with trivial reformatting (e.g. unit conversion, timestamp normalization). Must not contradict the source document. |
| `[inferred]` | Value is derived or computed from provenance document content through a non-trivial but fully mechanical step — no human judgment involved beyond choosing the derivation method. The derivation should be noted if it could affect interpretation. Example: `[inferred] 4h 23m (end − start timestamps)`. |
| `[manual]` | Value was supplied by the card author, with no direct or fully mechanical basis in the provenance document. Use this also when a value combines inferred and manually added content — if human judgment shaped the value in any way, it is `[manual]`. The description can detail what was inferred vs. added. |

**Conservative rule:** when in doubt between `[inferred]` and `[manual]`, choose `[manual]`. The distinction that matters for trust is whether a human made a judgment call, not whether they consulted the provenance document.

### Config key

The exact key to use when pre-filling a field via the `--config` JSON file. Key matching is fuzzy (case and punctuation are ignored), but using the listed key is safest. Fields auto-extracted from the provenance document need not be set in config unless you want to override the extracted value.

---

## Filling Guidance by Section

### Card Metadata
This section is always filled entirely by the card author (`[manual]`). It is the only section that describes the card itself rather than the execution. Pay particular attention to:
- **Card Author**: this is the person or system accountable for the card's content, not necessarily the person who ran the workflow. They may be different.
- **Authoring Method**: `auto-generated` means a tool produced the card without human review; `hybrid` means a tool produced a draft that a human reviewed and amended; `manually written` means a human filled all fields directly. This affects how much trust a reader should place in the card's completeness.
- **Source Provenance Document**: link the provenance document consulted.

### §0 — Provenance Capture Metadata
This section describes the provenance record, not the execution itself. Its purpose is to help the reader assess the quality and completeness of the underlying source before reading the rest of the card. Fields here almost always come directly from the provenance document header or metadata block (`[prov_doc]`). **Known Capture Gaps** is the most important field in this section — be explicit about what the provenance tool did and did not record.

### §4, §5, §6 — Repeating Blocks
These sections use a repeating block pattern. Each distinct artifact (input or output) and each distinct activity gets its own block.

- Replace `[N]` with a sequential integer starting from 1.
- Replace `<name>` with a short, stable identifier for the artifact or activity (e.g. `training-corpus`, `feature-extraction`, `checkpoint-epoch-10`). This identifier is used for cross-references between sections.
- In §5 (Execution Record), the **Inputs Consumed** and **Outputs Produced** fields should reference identifiers from §4 and §6 respectively, not free-text descriptions. This is what makes the card machine-parsable.
- Activities in §5 may be ordered by logical dependency (i.e. topological order of the DAG), not necessarily by wall-clock start time. If two activities ran in parallel, list them in any consistent order and note the parallelism in their descriptions.

### §8 vs. §9 — Two Distinct Quality Assessments
These sections are easy to conflate but cover different things:
- **§8 Execution Quality** answers: *did the workflow do what it was supposed to do?* It covers metrics, errors, and validation — the substance of the run.
- **§9 Provenance Record Quality** answers: *how well was this execution documented?* It covers completeness of the provenance capture, unlogged activities, and reproducibility — the quality of the record, independent of whether the execution succeeded.

A failed execution (§8 issues) can still have excellent provenance capture (§9 complete). A successful execution can be poorly documented. Fill these sections independently.

### Coverage Statistics
Fill this table last. For fixed sections, count the number of fields that have a non-empty value. For repeating sections (§4, §5, §6), count total fields across all instantiated blocks: if §4 has 3 input blocks of 7 fields each, Total Fields = 21. A field counts as "filled" even if its value is a documented omission note (e.g. `[not captured]`) — the goal is to make incompleteness visible, not to hide it.

---

## Card Metadata
*Who produced this card, when, and from what sources. The card author is accountable for its content.*
*This section describes the card itself, not the execution it documents.*

| Field | Ann. | Source | Config Key | Description |
|-------|------|--------|------------|-------------|
| Card ID | **[R]** | | `card_id` | Unique identifier for this provenance card |
| Card Creation Timestamp | **[R]** | | `card_creation_timestamp` | When this card was first created (ISO 8601) |
| Card Author | **[R]** | | `card_author` | Person or system that produced this card and is accountable for its content |
| Authoring Method | **[R]** | | `authoring_method` | `auto-generated` / `hybrid` / `manually written` |
| Source Provenance Document | **[R]** | | `source_provenance_documents` | PID or path to provenance document this card was produced from |
| Card Contact | **[Rec]** | | `card_contact` | Point of contact for questions or corrections about this card (may differ from execution contact) |

---

## 0. Provenance Capture Metadata
*Describes the provenance record itself — how it was produced and what it covers.*

| Field | Ann. | Source | Config Key | Description |
|-------|------|--------|------------|-------------|
| Capture Tool | **[R]** | | `capture_tool` | Library / system that generated the provenance record (name + version) |
| Capture Method | **[R]** | | `capture_method` | `automatic instrumentation` / `manual logging` / `hybrid` |
| Provenance Format | **[R]** | | `provenance_format` | File format and standard (e.g. W3C PROV-JSON, JSONL, RDF/Turtle) |
| Record ID | **[R]** | | `record_id` | Unique identifier for the provenance record this card summarizes |
| Record Creation Timestamp | **[Rec]** | | `record_creation_timestamp` | When the provenance record was written (ISO 8601) |
| Coverage Level | **[Rec]** | | `coverage_level` | `workflow-level only` / `activity-level` / `fine-grained (task-level)` |
| Known Capture Gaps | **[Rec]** | | `known_capture_gaps` | Aspects of the execution NOT captured in the provenance document, and why |
| Related Records | **[O]** | | `related_records` | IDs/paths of other provenance records covering the same or linked executions |

---

## 1. Workflow Identification
*Uniquely identifies this execution.*

| Field | Ann. | Source | Config Key | Description |
|-------|------|--------|------------|-------------|
| Workflow Execution ID | **[R]** | | `workflow_execution_id` | Unique identifier for this specific run (e.g. run ID, workflow ID) |
| Workflow Name | **[R]** | | `workflow_name` | Human-readable name of the workflow or pipeline |
| Execution Type | **[Rec]** | | `execution_type` | e.g. `training` / `inference` / `data preprocessing` / `evaluation` |
| Workflow Version | **[Rec]** | | `workflow_version` | Version of the workflow definition or script, if tracked |
| Execution Status | **[R]** | | `execution_status` | `FINISHED` / `FAILED` / `INTERRUPTED` / … |
| Start Timestamp | **[R]** | | `start_timestamp` | When the execution began (ISO 8601) |
| End Timestamp | **[R]** | | `end_timestamp` | When the execution ended (ISO 8601) |
| Duration | **[Rec]** | | `duration` | Total wall-clock time; may be computed from start/end timestamps |

---

## 2. Execution Context
*Where and why the workflow ran — the environment, not the data.*

| Field | Ann. | Source | Config Key | Description |
|-------|------|--------|------------|-------------|
| Code Reference | **[R]** | | `code_reference` | Script, commit hash, or entry-point that was executed |
| Trigger / Purpose | **[Rec]** | | `trigger_purpose` | What initiated this run and why (e.g. manual launch, scheduled job, upstream event) |
| Hardware | **[Rec]** | | `hardware` | CPU / GPU / accelerator type and count |
| Operating System | **[Rec]** | | `operating_system` | OS name and version |
| Software Stack | **[Rec]** | | `software_stack` | Key frameworks and libraries with versions |
| Configuration | **[Rec]** | | `configuration` | Config file path(s) or inline key parameters |
| Hostname / Cluster | **[O]** | | `hostname_cluster` | Machine name or cluster node |

---

## 3. Actors
*Who was responsible for this execution, with explicit roles.*

| Field | Ann. | Source | Config Key | Description |
|-------|------|--------|------------|-------------|
| Executor | **[R]** | | `executor` | Person or system account that launched the workflow |
| Data Owner / Steward | **[Rec]** | | `data_owner_steward` | Who holds rights or responsibility over the input data |
| Contact | **[Rec]** | | `contact` | Point of contact for questions about this execution (distinct from Card Contact) |
| Infrastructure Owner | **[O]** | | `infrastructure_owner` | Who owns/operates the compute environment |
| Tool / Framework Authors | **[O]** | | `tool_framework_authors` | Authors of key libraries used (if attribution is relevant) |
| Institutional Affiliation | **[O]** | | `institutional_affiliation` | Organization associated with the executor |

---

## 4. Inputs
*All artifacts and resources consumed by the execution.*
*Repeat one block per distinct input artifact or input group. Cross-reference these identifiers in §5.*

### Input [N] — `<name>`

| Field | Ann. | Source | Config Key | Description |
|-------|------|--------|------------|-------------|
| Name / ID | **[R]** | | `name_id` | Identifier or name of the input; used as the cross-reference target from §5 |
| Type | **[R]** | | `type` | `dataset` / `model` / `tensor` / `file` / `parameter` / `environment` / … |
| Provenance Reference | **[Rec]** | | `provenance_reference` | Where this input came from; link to its own provenance record or data card if available |
| Version / Checksum | **[Rec]** | | `version_checksum` | Version tag, hash, or timestamp of the input at time of use |
| Access Path | **[O]** | | `access_path` | URI, file path, or registry reference at time of execution |
| License Reference | **[O]** | | `license_reference` | Pointer to the authoritative license document or data card for this input; reflects what was understood to apply at execution time — not a claim about current license status |

---

## 5. Execution Record
*The log of activities performed during the workflow — each activity is one logical step.*
*Activities may be sequential or form a DAG; list in topological (dependency) order, not necessarily wall-clock order.*
*Cross-reference inputs by their §4 Name/ID and outputs by their §6 Name/ID.*

### Activity [N] — `<name>`

| Field | Ann. | Source | Config Key | Description |
|-------|------|--------|------------|-------------|
| Activity ID | **[R]** | | `activity_id` | Identifier of this activity within the workflow |
| Activity Type | **[R]** | | `activity_type` | e.g. `FeatureExtraction` / `Training` / `Evaluation` / `Registration` / `Inference` / … |
| Inputs Consumed | **[R]** | | `inputs_consumed` | §4 Name/IDs or prior activity output IDs used by this step |
| Outputs Produced | **[R]** | | `outputs_produced` | §6 Name/IDs generated by this step |
| Description | **[Rec]** | | `description` | Short human-readable explanation of what this step does |
| Start / End Timestamp | **[Rec]** | | `start_end_timestamp` | When this activity started and ended (ISO 8601) |
| Parameters / Hyperparameters | **[Rec]** | | `parameters_hyperparameters` | Key settings controlling this activity |

---

## 6. Outputs
*All artifacts produced by the execution — one block per distinct output.*
*This is a registry of what the workflow created, linking back to activities in §5.*

### Output [N] — `<name>`

| Field | Ann. | Source | Config Key | Description |
|-------|------|--------|------------|-------------|
| Name / ID | **[R]** | | `name_id` | Identifier or name of the output; used as the cross-reference target from §5 |
| Type | **[R]** | | `type` | `model` / `dataset` / `tensor` / `metric` / `log` / `artifact` / … |
| Produced by Activity | **[R]** | | `produced_by_activity` | Activity ID from §5 that created this output |
| Location / Access Path | **[Rec]** | | `location_access_path` | Where this output is stored at time of card creation |
| Format | **[Rec]** | | `format` | File format or serialization standard |
| Version / Checksum | **[O]** | | `version_checksum` | Hash or version at time of creation |
| Artifact Card Reference | **[O]** | | `artifact_card_reference` | Pointer to the data card or model card for this output, if one exists |

---

## 7. Resource Consumption
*Compute, energy, and human resources used by the execution as a whole.*

| Field | Ann. | Source | Config Key | Description |
|-------|------|--------|------------|-------------|
| Total Duration | **[R]** | | `total_duration` | Wall-clock time for the full execution |
| CPU / GPU Time | **[Rec]** | | `cpu_gpu_time` | Compute-hours consumed |
| Peak Memory | **[Rec]** | | `peak_memory` | Peak RAM / VRAM usage |
| Energy / CO₂ | **[Rec]** | | `energy_co2` | Energy consumed or CO₂ equivalent emitted |
| Storage Written | **[Rec]** | | `storage_written` | Total data written to persistent storage |
| Human Labor | **[O]** | | `human_labor` | Person-hours of manual effort involved in this execution (data labeling, setup, review) |

---

## 8. Execution Quality
*How well the execution performed — the substance of what ran, not the quality of its documentation.*

| Field | Ann. | Source | Config Key | Description |
|-------|------|--------|------------|-------------|
| Key Metrics | **[Rec]** | | `key_metrics` | Primary metrics produced (loss, accuracy, throughput, etc.) with values |
| Known Issues | **[Rec]** | | `known_issues` | Errors, anomalies, or unexpected behaviors observed during execution |
| Validation Performed | **[Rec]** | | `validation_performed` | Any checks run on outputs (tests, assertions, human review) |

---

## 9. Provenance Record Quality
*How completely and reliably this execution was documented — independent of whether it succeeded.*

| Field | Ann. | Source | Config Key | Description |
|-------|------|--------|------------|-------------|
| Capture Completeness | **[R]** | | `capture_completeness` | Fraction or narrative description of what was logged vs. what ran |
| Unlogged Activities | **[Rec]** | | `unlogged_activities` | Activities that occurred but were not captured in the provenance record |
| Unlogged Inputs / Outputs | **[Rec]** | | `unlogged_inputs_outputs` | Artifacts used or produced that are absent from §4 / §6 |
| Reproducibility | **[Rec]** | | `reproducibility` | Could this execution be reproduced from this record alone? If yes, how. If no, what is missing. |

---

## Coverage Statistics
*Fill this table after completing all other sections.*
*For repeating sections, multiply the per-block field count by the number of instantiated blocks.*
*A field counts as "filled" if it contains any value, including a documented omission note.*

| Section | Total Fields | Filled | Missing | Fill % |
|---------|-------------|--------|---------|--------|
| Card Metadata | 8 | — | — | — |
| §0 Provenance Capture Metadata | 8 | — | — | — |
| §1 Workflow Identification | 8 | — | — | — |
| §2 Execution Context | 7 | — | — | — |
| §3 Actors | 6 | — | — | — |
| §4 Inputs (6 fields × N blocks) | 6 × N | — | — | — |
| §5 Execution Record (7 fields × M blocks) | 7 × M | — | — | — |
| §6 Outputs (7 fields × P blocks) | 7 × P | — | — | — |
| §7 Resource Consumption | 6 | — | — | — |
| §8 Execution Quality | 3 | — | — | — |
| §9 Provenance Record Quality | 4 | — | — | — |
| **Total** | | — | — | — |
