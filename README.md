# Multi-view Multi-label Network Traffic Classification Based on MLP-Mixer Neural Network

## Introduction

This repository is a PyTorch implementation of [Multi-view Multi-label Network Traffic Classification Based on MLP-Mixer Neural Network](https://arxiv.org/abs/2210.16719).

Our model is constructed primarily using the [Mlp-Mixer](https://github.com/google-research/vision_transformer).

### Dataset

1. The USTC-TFC2016 dataset is [USTC](https://github.com/yungshenglu/USTC-TFC2016).

2. The VPN-nonVPN dataset is [VPN](https://www.unb.ca/cic/datasets/vpn.html).

3. The Tor-nonTor dataset is [Tor](https://www.unb.ca/cic/datasets/tor.html).

## Requirement

Hardware: >= 10G GPU memory

Software: [PyTorch](https://pytorch.org/)>=1.0.0, python3

## Getting Started

### Installation

1. Clone this repository.
```
git clone https://github.com/Anunknownresearcher/multi-view_multi-label_network_classification.git
```

2. Install Python dependencies.
```
pip install -r requirements.txt
```

### Implementation
1. Download datasets (i.e. [USTC](https://github.com/yungshenglu/USTC-TFC2016)) and preprocess the dataset.

```
python precessing.py --inputpath pcap_path --pre_type 1d --outputpath output_path --max_len 1600 --dataset_type TOR
```

2. Train (Validation is included at the end of the training)

The preprocessed datasset is [dataset](https://gitee.com/AACHILLSS/multi-view_multi-label_network_classification/tags).

Change the root of data path in train_config.yaml and train the model:

```
python train.py
```

3. Test

The trained model is [model](https://gitee.com/AACHILLSS/multi-view_multi-label_network_classification/tags).

Change the root of data path in test_config.yaml and test the model:

```
python train.py
```



## Citation
If you like our work and use the code or models for your research, please cite our work as follows.
```
@article{zheng2023multiview,
      title={Multi-view Multi-label Anomaly Network Traffic Classification based on MLP-Mixer Neural Network}, 
      author={Yu Zheng and Zhangxuan Dang and Chunlei Peng and Chao Yang and Xinbo Gao},
      year={2023},
      eprint={2210.16719},
      url={https://arxiv.org/abs/2210.16719},
      eprinttype = {arXiv},
}
```




