# CoolBoxWizard
Creating CoolBox frames using YAML config file ready to be visualized by CoolBox.

This repository provides a set of functions to create [CoolBox](https://github.com/GangCaoLab/CoolBox) `coolbox.core.frame.frame.Frame` via a YAML config file.

## Example usages

### Basic usage

```python
from coolboxvizard import create_frame
frame = create_frame('config.yaml')
frame.plot('chr12:1514617-1614617')
```

### With highlighted regions

```python
from coolbox.api import HighLights
from coolboxvizard import create_frame

regions= ['chr12:1534617-1564617']

highlights = HighLights(regions, alpha=0.1, color='blue')

with highlights:
     frame = create_frame('config.yaml')
        
frame.plot('chr12:1514617-1614617')
```

### With vertical lines

```python
from coolbox.api import Vlines
from coolboxvizard import create_frame

highlight_lines = [('chr12', 1534617), ('chr12', 1564617)]

frame = create_frame('config.yaml')
frame = frame * Vlines(highlight_lines, line_width=1.5, alpha=0.25, color='green')
frame.plot('chr12:1514617-1614617')
```

### Using CoolBox Browser
```python
from coolbox.api import Browser

bsr = Browser(frame, 
              reference_genome='hg38', 
              widgets_box='simple',
            )

bsr.show('chr12:1514617-1614617')
bsr.save('test.png')
```

## Requirements
- [CoolBox](https://github.com/GangCaoLab/CoolBox)
- [PyYAML](https://pypi.org/project/PyYAML/)

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



