---
license: cc-by-4.0
language:
- en
tags:
- remote sensing
- segmentation
- crop type
- foundation model
size_categories:
- 1K<n<10K
---


# Dataset Card for Multi-Temporal Crop Classification

## Dataset Description

- **Homepage: https://huggingface.co/datasets/ibm-nasa-geospatial/cdl-crops/**
- **Point of Contact: Dr. Hamed Alemohammad (halemohammad@clarku.edu)** 

### Dataset Summary

This dataset contains temporal Harmonized Landsat-Sentinel imagery of diverse land cover and crop type classes across the Contiguous United States for the year 2022. The target labels are derived from USDA's Crop Data Layer (CDL). It's primary purpose is for training segmentation geospatial machine learning models.

### Dataset Structure


## TIFF Files
Each tiff file covers a 224 x 224 pixel area at 30m spatial resolution. Each input satellite file contains 18 bands including 6 spectral bands for three time steps stacked together. Each GeoTIFF file for the mask contains one band with the target classes for each pixel. 

## Band Order
In each input GeoTIFF the following bands are repeated three times for three observations throughout the growing season:
Channel, Name, HLS S30 Band number  
1, Blue,  B02  
2, Green, B03  
3, Red,   B04  
4, NIR,   B8A  
5, SW 1,  B11  
6, SW 2,  B12  

Masks are a single band with values:  
0   :   "No Data"
1	:	"Natural Vegetation"
2	:	"Forest"
3	:	"Corn"
4	:	"Soybeans"
5	:	"Wetlands"
6	:	"Developed/Barren"
7	:	"Open Water"
8	:	"Winter Wheat"
9	:	"Alfalfa"
10	:	"Fallow/Idle Cropland"
11	:	"Cotton"
12	:	"Sorghum"
13	:	"Other"	 

## Class Distribution
### Training Data Distribution
![Training Data](training_dst.png)

### Validation Data Distribution
![Validation Data](validation_dst.png)

## Data Splits
The 3,854 chips have been randomly split into training (80%) and validation (20%) with corresponding ids recorded in cvs files `train_data.txt` and `validation_data.txt`.

## Dataset Creation
### Query and Scene Selection
First, a set of 5,000 chips were defined based on samples from the USDA CDL to ensure a representative sampling across the CONUS. Next, for each chip, the corresponding HLS S30 scenes between March and September 2022 were queried, and scenes with low cloud cover were retrieved. Then, three scenes are selected among the low cloudy scenes to ensure a scene from early in the season, one in the middle, and one toward the end. The three final scenes were then reprojected to CDL's projection grid (`EPSG:5070`) using bilinear interpolation. 

### Chip Generation
In the final step, the three scenes for each chip were clipped to the bounding box of the chip, and 18 spectral bands were stacked together. In addition, a quality control was applied to each chip using the `Fmask` layer of the HLS dataset. Any chip containing clouds, cloud shadow, adjacent to cloud or missing values were discarded. This resulted in 3,854 chips.

### Dataset Download
You can download the data in `.tgz` format from this repository (you need to install [Git Large File Sotrage](https://git-lfs.com/) for this). The same version of the data is hosted on [Source Cooperative](https://beta.source.coop/repositories/clarkcga/multi-temporal-crop-classification/description) as objects on AWS S3. 

### Citation

If this dataset helped your research, please cite `hls-multi-temporal-crop-classification` in your publications. Here is an example BibTeX entry:

```
@misc{hls-multi-temporal-crop-classification,
    author = {Cecil, Michael and Kordi, Fatemehand Li, Hanxi (Steve) and Khallaghi, Sam and Alemohammad, Hamed},
    doi    = {10.57967/hf/0955},
    month  = aug,
    title  = {{HLS Multi Temporal Crop Classification}},
    url    = {https://huggingface.co/ibm-nasa-geospatial/multi-temporal-crop-classification},
    year   = {2023}
}
```