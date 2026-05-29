# Workflow Card: Use Case 2 — Multi-Temporal Crop Classification Fine-Tuning

---

## 1. Workflow

- **name**: prithvi_crop_classification_finetuning
- **description**: End-to-end ML workflow that fine-tunes the IBM/NASA Prithvi-EO-1.0-100M geospatial foundation model on the HLS Multi-Temporal Crop Classification dataset to produce a segmentation model capable of classifying crop types and land cover across the contiguous United States using time-series Harmonised Landsat-Sentinel (HLS) satellite imagery.

---

## 2. Summary

- **execution_id**: prithvi_crop_classification_finetuning_v0
- **version**: 0
- **started_at**: 2024-02-05T13:30:00Z
- **ended_at**: 2024-02-06T03:18:44Z
- **duration**: 13h 48m 44s
- **status**: Completed
- **location**: us-east-1 (AWS EC2 p3.8xlarge)
- **user**: ibm-nasa-geospatial
- **entrypoint.repository**: https://github.com/NASA-IMPACT/hls-foundation-os
- **entrypoint.branch**: main
- **entrypoint.short_sha**: d82b4e3

---

## 3. Infrastructure

- **host_os**: Ubuntu 20.04.6 LTS
- **compute_hardware**: 4× NVIDIA V100-SXM2-32GB, Intel Xeon E5-2686 v4, 244 GB RAM
- **runtime_environment**: Python 3.10.13, CUDA 11.8, cuDNN 8.6.0
- **resource_manager**: AWS EC2 (manual job submission via SLURM-compatible launcher script)
- **primary_software**: Python, PyTorch, mmsegmentation, terratorch; Hugging Face Transformers
- **environment_snapshot**: https://github.com/NASA-IMPACT/hls-foundation-os/blob/main/configs/multi_temporal_crop_classification.py

---

## 4. Overview

### 4.1 Run Summary

- **total_activities**: 3
- **status_counts**: finished: 3
- **arguments**: epochs: 80, optimiser: AdamW (β1=0.9, β2=0.999, weight_decay=0.05), learning rate: 6e-5 (cosine schedule with linear warmup over 5 epochs)

**Notable Inputs:**
  - `ibm-nasa-geospatial/multi-temporal-crop-classification` — format: GeoTIFF chips (224×224 px, 18 bands, 30m resolution), size: 3 854 chips split 80/20 train/validation, source: https://huggingface.co/datasets/ibm-nasa-geospatial/cdl-crops/
  - `ibm-nasa-geospatial/Prithvi-100M` — format: PyTorch model weights, size: 100M parameters, source: https://huggingface.co/ibm-nasa-geospatial/Prithvi-100M

**Notable Outputs:**
  - `Prithvi-100M-multi-temporal-crop-classification` — type: fine-tuned segmentation model, location: https://huggingface.co/ibm-nasa-geospatial/Prithvi-100M-multi-temporal-crop-classification

**Structure (activity DAG):**
  1. DataPreparation
  2. ModelFinetuning
  3. ModelEvaluation

- **observations**: CDL (Crop Data Layer) labels are known to contain noise, which influences model performance. Fine-tuning with more accurate labels is expected to further improve results. Class imbalance is present (e.g., Open Water achieves highest IoU at 0.68 vs Alfalfa at 0.31). The model also handles static imagery via T=1.

### 4.2 Resource Usage

- **cpu**: Peak 16-core utilisation ~55% during GeoTIFF chip loading; predominantly GPU-bound during forward/backward passes
- **memory**: Peak RAM usage: 96 GB (concurrent chip loading with prefetch workers=8 per GPU)
- **gpu**: 4× NVIDIA V100-SXM2-32GB; average per-GPU utilisation ~89% during training; peak memory per GPU 28.4 GB
- **disk**: ~18 GB total — 3 854 GeoTIFF chips (~14 GB) + model checkpoint (~380 MB) + mmsegmentation log artefacts (~3.5 GB)
- **network**: ~15 GB ingress (HLS S30 chips + Prithvi-100M weights from HuggingFace Hub); ~400 MB egress (checkpoint upload)

---

## 5. Activities

#### Activity: `DataPreparation`

- **name**: DataPreparation
- **task_count**: 1
- **started_at**: 2024-02-05T13:30:00Z
- **ended_at**: 2024-02-05T15:04:17Z
- **duration**: 1h 34m 17s
- **status**: success: 1
  - **hosts**: ip-10-0-3-12.ec2.internal
  - **inputs**:
    - `USDA CDL 2022` — USDA Crop Data Layer providing target class labels for 13 land-cover/crop categories at 30m resolution across the CONUS
    - `HLS S30 scenes (2022)` — Harmonised Landsat-Sentinel scenes (March–September 2022) retrieved for each chip location; three scenes per chip (early/mid/late season); reprojected to EPSG:5070
  - **outputs**:
    - `ibm-nasa-geospatial/multi-temporal-crop-classification` — 3 854 GeoTIFF chips (post quality control with Fmask); 18-band input (6 spectral bands × 3 time steps) + 1-band CDL-derived mask; 80/20 train/validation split recorded in train_data.txt / validation_data.txt

#### Activity: `ModelFinetuning`

- **name**: ModelFinetuning
- **task_count**: 1
- **started_at**: 2024-02-05T15:05:02Z
- **ended_at**: 2024-02-06T02:49:31Z
- **duration**: 11h 44m 29s
- **status**: success: 1
  - **hosts**: ip-10-0-3-12.ec2.internal
  - **inputs**:
    - `ibm-nasa-geospatial/Prithvi-100M` — pretrained temporal ViT encoder (MAE, MSE loss) trained on contiguous US HLS V2 L30 data; 100M parameters; accepts (B, C, T, H, W) remote sensing video format
    - `ibm-nasa-geospatial/multi-temporal-crop-classification` — 3 854 chip dataset; input chips 224×224×18; 13-class CDL-derived masks
    - `multi_temporal_crop_classification.py` — mmsegmentation training configuration defining model, dataset, augmentation, optimiser and schedule
  - **outputs**:
    - `Prithvi-100M-multi-temporal-crop-classification` — fine-tuned segmentation model checkpoint; 80-epoch training run; mIoU: 0.4269, mAcc: 64.06%, aAcc: 60.64%

#### Activity: `ModelEvaluation`

- **name**: ModelEvaluation
- **task_count**: 1
- **started_at**: 2024-02-06T02:50:14Z
- **ended_at**: 2024-02-06T03:18:44Z
- **duration**: 28m 30s
- **status**: success: 1
  - **hosts**: ip-10-0-3-12.ec2.internal
  - **inputs**:
    - `Prithvi-100M-multi-temporal-crop-classification` — fine-tuned checkpoint
    - `validation split` — 20% held-out chips from ibm-nasa-geospatial/multi-temporal-crop-classification
  - **outputs**:
    - Per-class IoU / Acc report — Natural Vegetation: IoU 0.40; Forest: 0.47; Corn: 0.55; Soybeans: 0.53; Wetlands: 0.40; Developed/Barren: 0.36; Open Water: 0.68; Winter Wheat: 0.50; Alfalfa: 0.31; Fallow/Idle: 0.35; Cotton: 0.32; Sorghum: 0.33; Other: 0.34
    - Aggregate metrics — mIoU: 0.4269, mAcc: 64.06%, aAcc: 60.64%

---

## 6. Significant Artifacts

### Input Artifacts

**Artifact: `ibm-nasa-geospatial/Prithvi-100M`**
- **name**: ibm-nasa-geospatial/Prithvi-100M
- **description**: First-of-its-kind temporal Vision Transformer (ViT + MAE) pretrained by IBM and NASA on contiguous US HLS V2 L30 data. Accepts remote sensing data in (B, C, T, H, W) format. 100M parameters. Six spectral bands (Blue, Green, Red, Narrow NIR, SWIR 1, SWIR 2). License: Apache-2.0.
- **reference**: https://huggingface.co/ibm-nasa-geospatial/Prithvi-100M

**Artifact: `ibm-nasa-geospatial/multi-temporal-crop-classification`**
- **name**: ibm-nasa-geospatial/multi-temporal-crop-classification
- **description**: 3 854 GeoTIFF chips of 224×224 px at 30m resolution covering the CONUS for 2022. Each chip has 18 input bands (6 spectral × 3 time steps) and a 13-class CDL-derived segmentation mask. Randomly split 80/20 train/validation. License: Apache-2.0.
- **reference**: https://huggingface.co/datasets/ibm-nasa-geospatial/cdl-crops/

### Output Artifacts

**Artifact: `Prithvi-100M-multi-temporal-crop-classification`**
- **name**: Prithvi-100M-multi-temporal-crop-classification
- **description**: Fine-tuned geospatial segmentation model based on Prithvi-EO-1.0-100M, trained for 80 epochs on the HLS multi-temporal crop classification dataset using the mmsegmentation stack. Achieves mIoU of 0.4269 across 13 land-cover/crop classes. Includes an inference script and interactive demo.
- **reference**: https://huggingface.co/ibm-nasa-geospatial/Prithvi-100M-multi-temporal-crop-classification
