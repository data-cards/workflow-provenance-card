---
license: apache-2.0
language:
- en
tags:
- Pytorch
- mmsegmentation
- segmentation
- Crop Classification
- Multi Temporal
- Geospatial
- Foundation model
datasets:
- ibm-nasa-geospatial/multi-temporal-crop-classification
metrics:
- accuracy
- IoU
library_name: terratorch
pipeline_tag: image-segmentation
---
### Model and Inputs
The pretrained [Prithvi-EO-1.0-100M](https://huggingface.co/ibm-nasa-geospatial/Prithvi-100M/blob/main/README.md) parameter model is finetuned to classify crop and other land cover types based off HLS data and CDL labels from the [multi_temporal_crop_classification dataset](https://huggingface.co/datasets/ibm-nasa-geospatial/multi-temporal-crop-classification). 

This dataset includes input chips of 224x224x18, where 224 is the height and width and 18 is combined with 6 bands of 3 time-steps. The bands are:
 
1. Blue
2. Green
3. Red
4. Narrow NIR
5. SWIR 1
6. SWIR 2

Labels are from CDL(Crop Data Layer) and classified into 13 classes.

![](multi_temporal_crop_classification.png)

The Prithvi-100m model was initially pretrained using a sequence length of 3 timesteps. For this task, we leverage the capacity for multi-temporal data input, which has been integrated from the foundational pretrained model. This adaptation allows us to achieve more generalized finetuning outcomes.

### Code
Code for Finetuning is available through [github](https://github.com/NASA-IMPACT/hls-foundation-os/)

Configuration used for finetuning is available through [config](https://github.com/NASA-IMPACT/hls-foundation-os/blob/main/configs/multi_temporal_crop_classification.py).

### Results
The experiment by running the mmseg stack for 80 epochs using the above config led to the following result:

|     **Classes**    | **IoU**| **Acc**|
|:------------------:|:------:|:------:|
| Natural Vegetation | 0.4038 | 46.89% |
|       Forest       | 0.4747 | 66.38% |
|        Corn        | 0.5491 | 65.47% |
|      Soybeans      | 0.5297 | 67.46% |
|      Wetlands      | 0.402  | 58.91% |
|  Developed/Barren  | 0.3611 | 56.49% |
|     Open Water     | 0.6804 | 90.37% |
|    Winter Wheat    | 0.4967 | 67.16% |
|       Alfalfa      | 0.3084 | 66.75% |
|Fallow/Idle Cropland| 0.3493 | 59.23% |
|       Cotton       | 0.3237 | 66.94% |
|       Sorghum      | 0.3283 | 73.56% |
|        Other       | 0.3427 | 47.12% |

|**aAcc**|**mIoU**|**mAcc**|
|:------:|:------:|:------:|
| 60.64% | 0.4269 | 64.06% |

It is important to acknowledge that the CDL (Crop Data Layer) labels employed in this process are known to contain noise and are not entirely precise, thereby influencing the model's performance. Fine-tuning the model with more accurate labels is expected to further enhance its overall effectiveness, leading to improved results.

### Baseline
The baseline model along with its results can be accessed [here](https://github.com/ClarkCGA/multi-temporal-crop-classification-baseline).

### Inference
The github repo includes an inference script that allows to run the hls-cdl crop classification model for inference on HLS images. These input have to be geotiff format, including 18 bands for 3 time-step, and each time-step includes the channels described above (Blue, Green, Red, Narrow NIR, SWIR, SWIR 2) in order. There is also a **demo** that leverages the same code **[here](https://huggingface.co/spaces/ibm-nasa-geospatial/Prithvi-100M-multi-temporal-crop-classification-demo)**.

### Feedback

Your feedback is invaluable to us. If you have any feedback about the model, please feel free to share it with us. You can do this by submitting issues on our open-source repository, [hls-foundation-os](https://github.com/NASA-IMPACT/hls-foundation-os/issues), on GitHub.

## Citation

If this model helped your research, please cite `HLS Multi Temporal Crop Classification Model` in your publications. Here is an example BibTeX entry:

```
@misc{hls-multi-temporal-crop-classification-model,
    author = {Li, Hanxi (Steve) and Khallaghi, Sam and Cecil, Michael and Kordi, Fatemeh and Fraccaro, Paolo and Alemohammad, Hamed and Ramachandran, Rahul},
    doi    = { 10.57967/hf/0954 },
    month  = aug,
    title  = {{HLS Multi Temporal Crop Classification Model}},
    url    = {https://huggingface.co/ibm-nasa-geospatial/Prithvi-100M-multi-temporal-crop-classification},
    year   = {2023}
}
```