# Workflow Card: Use Case 2 — Multi-Temporal Crop Classification Fine-Tuning

---

## 1. Workflow

- **name**: prithvi_crop_classification_finetuning
- **description**: End-to-end ML workflow that fine-tunes the IBM/NASA Prithvi-EO-1.0-100M geospatial foundation model on the HLS Multi-Temporal Crop Classification dataset to produce a pixel-wise segmentation model capable of classifying 13 crop types and land-cover categories across the contiguous United States (CONUS). The workflow ingests Harmonised Landsat-Sentinel (HLS) S30 satellite imagery at 30m resolution across three seasonal time steps (early, mid, late growing season 2022), applies Fmask cloud-quality filtering, constructs 224×224 px GeoTIFF chips with 18 input bands (6 spectral × 3 temporal), trains a UperNet segmentation head on top of the frozen temporal ViT encoder for 80 epochs using AdamW, and evaluates per-class IoU on a held-out 20% validation split. The resulting model achieves a mean IoU of 0.4269 across 13 classes.

---

## 2. Summary

- **execution_id**: prithvi_crop_classification_finetuning_v0
- **version**: 0
- **started_at**: 2024-02-05T13:30:00Z (ISO 8601 / UTC)
- **ended_at**: 2024-02-06T03:18:44Z (ISO 8601 / UTC)
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
- **compute_hardware**: 4× NVIDIA V100-SXM2-32GB, Intel Xeon E5-2686 v4 (16 cores), 244 GB RAM
- **runtime_environment**: Python 3.10.13, CUDA 11.8, cuDNN 8.6.0; mmsegmentation v1.2.2 running inside a custom Docker image (`nasa-impact/hls-foundation:1.2.2`)
- **resource_manager**: AWS EC2 (manual job submission via SLURM-compatible launcher script)
- **primary_software**: Python, PyTorch 1.13.1, mmsegmentation 1.2.2, terratorch 0.1.0, Hugging Face Transformers 4.35.2, rasterio 1.3.9, GDAL 3.7.0
- **environment_snapshot**: https://github.com/NASA-IMPACT/hls-foundation-os/blob/main/configs/multi_temporal_crop_classification.py; full pip freeze available at s3://nasa-impact-hls/runs/prithvi_crop_v0/environment.txt

---

## 4. Workflow Overview

### 4.1 Run Summary

- **total_activities**: 3
- **status_counts**: finished: 3, failed: 0, skipped: 0
- **arguments**: epochs: 80, optimiser: AdamW (β1=0.9, β2=0.999, ε=1e-8, weight_decay=0.05), learning_rate: 6e-5, lr_scheduler: cosine with linear warmup (warmup_epochs: 5), batch_size_per_gpu: 4, num_workers: 8, seed: 0, fp16: false, sync_bn: true, num_classes: 13, ignore_index: -1, loss: CrossEntropyLoss

**Significant Inputs:**

- `ibm-nasa-geospatial/multi-temporal-crop-classification` , GeoTIFF chips (224×224 px, 18 bands, 30m resolution), 3,854 chips; ~14 GB, https://huggingface.co/datasets/ibm-nasa-geospatial/cdl-crops/ 
- `ibm-nasa-geospatial/Prithvi-100M` , PyTorch model weights (ViT encoder), 100M parameters; ~380 MB, https://huggingface.co/ibm-nasa-geospatial/Prithvi-100M 

**Significant Outputs:**

- `Prithvi-100M-multi-temporal-crop-classification` , mmsegmentation checkpoint (.pth), ~380 MB, https://huggingface.co/ibm-nasa-geospatial/Prithvi-100M-multi-temporal-crop-classification 




### 4.2 Workflow Structure

```
DataPreparation → ModelFinetuning → ModelEvaluation
```

### 4.3 Resource Usage

- **cpu**: Peak 16-core utilisation ~55% during GeoTIFF chip loading and Fmask processing; predominantly GPU-bound during forward/backward passes; average sustained ~22% across full run duration
- **memory**: Peak RAM usage: 96 GB (concurrent chip loading with prefetch workers=8 per GPU); average sustained: ~71 GB
- **gpu**: 4× NVIDIA V100-SXM2-32GB; average per-GPU utilisation ~89% during training steps; peak memory per GPU 28.4 GB; total GPU memory bandwidth utilised: ~1.2 TB/s aggregate during backward passes
- **disk**: ~18 GB total — 3,854 GeoTIFF chips (~14 GB) + model checkpoint (~380 MB) + mmsegmentation log artefacts and tensorboard events (~3.5 GB)
- **network**: ~15 GB ingress (HLS S30 chips + Prithvi-100M weights from HuggingFace Hub); ~400 MB egress (checkpoint upload to HuggingFace Hub)

---


### 4.4 Observations
- USDA CDL (Crop Data Layer) labels are known to contain spatial registration noise and temporal misalignment artefacts, which introduce label noise into the training masks; fine-tuning with higher-quality labels is expected to further improve mIoU.
- Significant class imbalance is present: Open Water achieves the highest per-class IoU (0.68) while Alfalfa achieves the lowest (0.31), likely reflecting both class frequency differences and spectral similarity to other vegetation.
- The model also handles static (single-date) imagery via T=1 input; the temporal ViT encoder degrades gracefully to a standard spatial ViT when only one time step is provided.
- ModelFinetuning accounted for 85.1% of total wall-clock time (11h 44m of 13h 48m).
- Average per-GPU memory usage of 28.4 GB (of 32 GB available) left limited headroom; batch size was fixed at 4 per GPU to avoid OOM events during backward passes with the UperNet decoder.
- Chips rejected by Fmask cloud-quality filtering were excluded before the 80/20 split, leaving 3,854 usable chips from an original pool of ~4,200 candidate locations.

## 5. Activities

#### Activity: `DataPreparation`

- **name**: DataPreparation
- **task_count**: 1
- **started_at**: 2024-02-05T13:30:00Z
- **ended_at**: 2024-02-05T15:04:17Z
- **duration**: 1h 34m 17s
- **status**: success: 1, error: 0
- **hosts**:
  - host: `ip-10-0-3-12.ec2.internal`, tasks: 1
    - cpu_usage: avg=52.3%, peak=55.1%
    - memory_usage: avg=38 GB, peak=51 GB
    - disk_read: ~21 GB (raw HLS S30 scenes from S3 staging bucket)
    - disk_write: ~14.4 GB (3,854 GeoTIFF chips + train_data.txt / validation_data.txt)
    - gpu_usage: 0% (CPU-only stage)
- **inputs**:
  - `USDA CDL 2022` — USDA Crop Data Layer providing target class labels for 13 land-cover/crop categories at 30m resolution across CONUS; accessed via USDA CropScape WCS endpoint; rasterised and reprojected to EPSG:5070 (Albers Equal Area) to match HLS chip grid
  - `HLS S30 scenes (2022)` — Harmonised Landsat-Sentinel-2 scenes (bands: Blue, Green, Red, Narrow NIR, SWIR 1, SWIR 2) retrieved from NASA LP DAAC for the March–September 2022 growing season at each chip location; three acquisition dates selected per chip (early/mid/late season) based on cloud cover ranking; reprojected to EPSG:5070; Fmask cloud/shadow/snow masks applied to exclude low-quality pixels
- **outputs**:
  - `ibm-nasa-geospatial/multi-temporal-crop-classification` — 3,854 GeoTIFF chips (after Fmask QC; 346 chips rejected from original ~4,200); each chip: 224×224 px, 18-band input (6 spectral bands × 3 time steps), 1-band CDL-derived class mask (13 classes + no-data); 80/20 train/validation split recorded in train_data.txt (3,083 chips) / validation_data.txt (771 chips); mean per-band normalisation statistics computed from training split and saved to dataset_stats.json

#### Activity: `ModelFinetuning`

- **name**: ModelFinetuning
- **task_count**: 1
- **started_at**: 2024-02-05T15:05:02Z
- **ended_at**: 2024-02-06T02:49:31Z
- **duration**: 11h 44m 29s
- **status**: success: 1, error: 0
- **hosts**:
  - host: `ip-10-0-3-12.ec2.internal`, tasks: 1
    - gpu_usage: avg=89.1%, peak=99.4% (across 4× V100)
    - gpu_memory_usage: avg=26.8 GB/GPU, peak=28.4 GB/GPU
    - cpu_usage: avg=19.6%, peak=38.4% (DataLoader workers + augmentation)
    - memory_usage: avg=71 GB, peak=96 GB
    - disk_read: ~14 GB (chip streaming across 80 epochs)
    - disk_write: ~3.9 GB (epoch checkpoints, tensorboard logs)
- **inputs**:
  - `ibm-nasa-geospatial/Prithvi-100M` — pretrained temporal Vision Transformer encoder (ViT-B/16 + Masked Autoencoder pretraining, MSE loss) trained on contiguous US HLS V2 L30 data; 100M parameters; accepts input tensors in (B, C, T, H, W) remote sensing video format; encoder weights frozen for first 5 warmup epochs then partially unfrozen at layers 8–12 for epochs 6–80
  - `ibm-nasa-geospatial/multi-temporal-crop-classification` — 3,083 chip training split; input chips 224×224×18; 13-class CDL-derived masks; online augmentation: random horizontal/vertical flip (p=0.5), random rotation (±15°), colour jitter on spectral bands (brightness ±0.1)
  - `multi_temporal_crop_classification.py` — mmsegmentation training configuration defining UperNet decode head (in_channels=[384,384,384,384], channels=256, dropout_ratio=0.1), dataset pipeline, augmentation policy, AdamW optimiser, cosine LR schedule, and DDP training strategy
- **outputs**:
  - `Prithvi-100M-multi-temporal-crop-classification` — fine-tuned segmentation model checkpoint (best epoch: 73 of 80, selected by validation mIoU); 80-epoch training run; final training loss: 0.412; best validation mIoU: 0.4269; mAcc: 64.06%; aAcc: 60.64%; checkpoint saved as `best_mIoU_iter_24819.pth` (~380 MB)

#### Activity: `ModelEvaluation`

- **name**: ModelEvaluation
- **task_count**: 1
- **started_at**: 2024-02-06T02:50:14Z
- **ended_at**: 2024-02-06T03:18:44Z
- **duration**: 28m 30s
- **status**: success: 1, error: 0
- **hosts**:
  - host: `ip-10-0-3-12.ec2.internal`, tasks: 1
    - gpu_usage: avg=44.7% (single-GPU inference, batch size 4)
    - gpu_memory_usage: avg=9.2 GB
    - cpu_usage: avg=11.3%
    - memory_usage: avg=28 GB
- **inputs**:
  - `Prithvi-100M-multi-temporal-crop-classification` — best validation checkpoint (epoch 73)
  - `validation split` — 771 held-out chips from ibm-nasa-geospatial/multi-temporal-crop-classification; same per-band normalisation statistics as training split
- **outputs**:
  - Per-class IoU / Accuracy report:

    | Class | IoU | Accuracy |
    |---|---|---|
    | Natural Vegetation | 0.40 | 52.3% |
    | Forest | 0.47 | 61.8% |
    | Corn | 0.55 | 69.4% |
    | Soybeans | 0.53 | 67.1% |
    | Wetlands | 0.40 | 54.2% |
    | Developed/Barren | 0.36 | 49.7% |
    | Open Water | 0.68 | 81.5% |
    | Winter Wheat | 0.50 | 63.9% |
    | Alfalfa | 0.31 | 44.1% |
    | Fallow/Idle | 0.35 | 47.8% |
    | Cotton | 0.32 | 45.5% |
    | Sorghum | 0.33 | 46.2% |
    | Other | 0.34 | 47.0% |

  - Aggregate metrics — mIoU: 0.4269, mAcc: 64.06%, aAcc: 60.64%

---

## 6. Significant Workflow Artifacts

### Input Artifacts

**Artifact: `ibm-nasa-geospatial/Prithvi-100M`**
- **identifier**: ibm-nasa-geospatial/Prithvi-100M
- **description**: First-of-its-kind temporal Vision Transformer (ViT-B/16 backbone + Masked Autoencoder pretraining) developed jointly by IBM and NASA, pretrained on contiguous US HLS V2 L30 data. Accepts remote sensing input in (B, C, T, H, W) format, natively handling multi-temporal image sequences. Six spectral bands: Blue, Green, Red, Narrow NIR, SWIR 1, SWIR 2. 100M parameters. Pretrained using MSE reconstruction loss on randomly masked image patches. License: Apache-2.0.
- **reference**: https://huggingface.co/ibm-nasa-geospatial/Prithvi-100M
- **size**: ~380 MB
- **additional metadata**: architecture: ViT-B/16 + temporal positional encoding; pretraining: MAE (mask_ratio=0.75); input_format: (B, C, T, H, W); spectral_bands: [Blue, Green, Red, NarrowNIR, SWIR1, SWIR2]; spatial_resolution: 30m; license: Apache-2.0

**Artifact: `ibm-nasa-geospatial/multi-temporal-crop-classification`**
- **identifier**: ibm-nasa-geospatial/multi-temporal-crop-classification
- **description**: 3,854 GeoTIFF chips of 224×224 pixels at 30m spatial resolution covering the CONUS for the 2022 growing season. Each chip contains 18 input bands (6 spectral bands × 3 seasonal time steps: early/mid/late season) derived from HLS S30 Harmonised Landsat-Sentinel-2 imagery, plus a 1-band CDL-derived segmentation mask covering 13 land-cover and crop type classes. Chips are quality-filtered using Fmask. Randomly split 80/20 into training (3,083 chips) and validation (771 chips). License: Apache-2.0.
- **reference**: https://huggingface.co/datasets/ibm-nasa-geospatial/cdl-crops/
- **size**: ~14 GB (3,854 GeoTIFF chips)
- **additional metadata**: num_chips: 3,854; chips_rejected_fmask: 346; num_classes: 13; spatial_resolution: 30m; crs: EPSG:5070; spectral_bands_per_timestep: 6; num_timesteps: 3; train_chips: 3,083; val_chips: 771; source_labels: USDA CDL 2022; license: Apache-2.0

### Output Artifacts

**Artifact: `Prithvi-100M-multi-temporal-crop-classification`**
- **identifier**: Prithvi-100M-multi-temporal-crop-classification
- **description**: Fine-tuned geospatial segmentation model based on Prithvi-EO-1.0-100M, trained for 80 epochs on the HLS multi-temporal crop classification dataset using the mmsegmentation stack with a UperNet segmentation head. Best checkpoint selected at epoch 73 by validation mIoU. Achieves a mean IoU of 0.4269 across 13 land-cover and crop type classes, with highest per-class IoU for Open Water (0.68) and lowest for Alfalfa (0.31). Includes an inference script and an interactive Gradio demo. License: Apache-2.0.
- **reference**: https://huggingface.co/ibm-nasa-geospatial/Prithvi-100M-multi-temporal-crop-classification
- **size**: ~380 MB
- **additional metadata**: best_epoch: 73; mIoU: 0.4269; mAcc: 0.6406; aAcc: 0.6064; decode_head: UperNet; training_loss_final: 0.412; checkpoint_file: best_mIoU_iter_24819.pth; license: Apache-2.0
