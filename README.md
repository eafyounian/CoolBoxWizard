# CoolBoxWizard
Creating CoolBox frames using YAML config file ready to be visualized by CoolBox.

This repository provides a set of functions to create [CoolBox](https://github.com/GangCaoLab/CoolBox) `coolbox.core.frame.frame.Frame` via a YAML config file.

## Config file example

```YAML
parameters:
  HiC: ## HiC parameters
    style: window
    resolution: 100000
    HiC_cmap: JuiceBoxLike
    depth_ratio: 1

  ATAC_seq: ## ATAC paramters
    max_value: 100
    min_value: 0
    height: 1

  ## etc.

tracks:
  track_0:
    order: 0
    track_type: HiCMat
    track_general_params: HiC
    file: path/to/.hic_file

  track_1:
    file: path/to/.bw_file
    order: 27
    title: ATAC sample
    track_type: BigWig
    track_general_params: ATAC_seq
    color: '#d4aa00'
    height: 0.75

  ## etc.
```


## Example use

```python
from coolboxvizard import create_frame
frame = create_frame('config.yaml')
frame.plot('chr12:1514617-1614617')
```


## Requirements
- [CoolBox](https://github.com/GangCaoLab/CoolBox)
- [PyYAML](https://pypi.org/project/PyYAML/)

