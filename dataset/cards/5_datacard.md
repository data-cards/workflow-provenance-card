---
dataset_info:
  features:
  - name: content
    dtype: string
  - name: label
    dtype: int64
  splits:
  - name: train
    num_bytes: 47241927
    num_examples: 120000
  - name: validation
    num_bytes: 5052323
    num_examples: 20000
  - name: test
    num_bytes: 14856442
    num_examples: 60000
  download_size: 40289388
  dataset_size: 67150692
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
  - split: validation
    path: data/validation-*
  - split: test
    path: data/test-*
---

# Phishing Email Detection Dataset

A comprehensive dataset combining email messages and URLs for phishing detection.

## Dataset Overview

### Quick Facts
- **Task Type**: Multi-class Classification
- **Languages**: English
- **Total Samples**: 200,000 entries
- **Size Split**: 
  - Email samples: 22,644
  - URL samples: 177,356
- **Label Distribution**: Four classes (0, 1, 2, 3)
- **Format**: Two columns - `content` and `labels`

## Dataset Structure

### Features
```python
{
    'content': Value(dtype='string', description='The text content - either email body or URL'),
    'labels': ClassLabel(num_classes=4, names=[
        'legitimate_email',    # 0
        'phishing_email',       # 1
        'legitimate_url',     # 2
        'phishing_url'    # 3
    ], description='Multi-class label for content classification')
}