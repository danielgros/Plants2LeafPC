# Plants2LeafPC: Acquisition of Leaf Point Cloud Data Via Stereo Images and Computer Vision Methods

## Project Overview

## Project Setup

### Matterport Mask-RCNN Setup

1. Clone the Matterport Mask-RCNN repository https://github.com/matterport/Mask_RCNN
2. Install dependencies
   ```bash
   pip3 install -r requirements.txt
   ```
3. Run setup from the repository root directory
    ```bash
    python3 setup.py install
    ``` 
4. Download pre-trained COCO weights (mask_rcnn_coco.h5) from the [releases page](https://github.com/matterport/Mask_RCNN/releases).







Clone THIS Repository within a directory within the "samples" folder in the Matterport Mask-RCNN repository like so

```maskrcnnrep[rename]/samples/senior-thesis-project/```

Copy the directory structure

```xargs mkdir -p < directory_structure.txt```

### Conda Environment Setup

### ZED SDK Setup

1. Download the ZED SDK Docker Image at ...

2. Start the docker container

```docker run --gpus all -it --privileged -v docker:/docker_volume stereolabs/zed:3.8-devel-cuda10.2-ubuntu18.04```

to exit the docker container:
Type Ctrl+p then Ctrl+q.


to enter the docker container:

```docker exec -it <continaer id> bash```


https://www.stereolabs.com/docs/docker/install-guide-linux/


## Miscellaneous

To Copy Directory Structure:

```find . -type d -not -path "./.git/*" > directory_structure.txt```


For access to the data submit a request via the discussion board



two avenues -> docker container version and conda version, 
