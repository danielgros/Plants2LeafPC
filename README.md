# Plants2LeafPC: Acquisition of Leaf Point Cloud Data Via Stereo Images and Computer Vision Methods

## Project Overview

UIUC researchers are experimenting with genetic modifications on plants and tracking their growth to measure the effectiveness of these modifications on the plant’s ability to survive in drier and hotter climates. Metrics that communicate the quality of growth can be gathered from a leaf’s phenotype data, including its width. This research project aims at making extraction of phenotype data easier, as in the case of leaf width, by providing researchers with an accurate and precise model of individual leaves.

A vision-based method using stereo images was developed to acquire a 3D model of a leaf. First a stereo camera was utilized to capture recordings of a scene and generate point clouds. Then, the point clouds were projected onto a 2D representation to run a trained instance segmentation model on them to detect leaves in the 2D representation and predict leaf masks. These masks were used as filters on these 2D representations to acquire leaf point clouds after reprojection to 3D.

This research project and the resulting software produced by it demonstrate an effective workflow for acquiring leaf point clouds with birds-eye-view stereo images. Although the accuracy of some measurements doesn’t make the product of this project ready to be shared, the results give empirical evidence that the method utilized is able to go through the process of acquiring leaf models for plants in environments with dense leaf clusters. These products are a step in allowing leaf phenotype measurements to be taken with ease, helping researchers track plant growth and improve their experiments.

## Project Setup

### Repository + Directory Setup
1. Clone this repository
2. Navigate to Plants2LeafPC directory
3. Copy the directory structure
    ```bash 
    xargs mkdir -p < directory_structure.txt
    ```

### Conda Environment Setup

1. Navigate to Plants2LeafPC directory
2. Download and install conda: https://www.anaconda.com/download/ 
3. Install general conda environment to run all scripts except those pertaining to the ml model
    ```bash
    conda env create -f setup/general_env.yml
    ```
4. Install ml model conda environment to run all scripts pertaining to the ml model
    ```bash
    conda env create -f setup/ml_model_env.yml
    ```

### Matterport Mask-RCNN Setup

1. Navigate to Plants2LeafPC/04-model/src
2. Clone the Matterport Mask-RCNN repository https://github.com/matterport/Mask_RCNN
3. Navigate to Plants2LeafPC/04-model/src/Mask_RCNN
4. Activate ml model conda environment
    ```bash
    conda activate ml_model_env
    ```
4. Install dependencies
   ```bash
   pip3 install -r requirements.txt
   ```
5. Run setup from the repository root directory
    ```bash
    python3 setup.py install
    ``` 
6. Download pre-trained COCO weights (mask_rcnn_coco.h5) from the [releases page](https://github.com/matterport/Mask_RCNN/releases).

### ZED SDK Setup

1. Browse the ZED SDK Docker Images at https://hub.docker.com/r/stereolabs/zed/tags?page=1
2. Select one based on your OS and GPUs
3. Download the image onto your machine (using 3.8-devel-cuda10.2-ubuntu18.04 as an example)
    ```bash
    docker pull stereolabs/zed:3.8-devel-cuda10.2-ubuntu18.04
    ```
4. Spin up a container using the downloaded image (using 3.8-devel-cuda10.2-ubuntu18.04 as an example)
    ```bash
    docker run --gpus all -it --name zed_sdk_container --privileged -v docker:/docker_volume stereolabs/zed:3.8-devel-cuda10.2-ubuntu18.04 bash
    ```
5. Install ZED SDK in container (in current directory: /usr/local/zed)
    ```bash
    python3 get_python_api.py
    ```
6. To exit the container type Ctrl+p then Ctrl+q


## Use Guide


### 00-get-svo-files
This is used to capture recordings using the ZED Camera
Make sure ZED Camera is connected to a machine with the ZED SDK installed and the Plants2LeafPC/00-get-svo-files directory

1. Navigate to Plants2LeafPC/00-get-svo-files/
2. Transfer over files into container
    ```bash
    docker cp src zed_sdk_container:/docker_volume
    ```
3. Enter the spun up container with the ZED SDK install
    ```bash
    docker exec -it zed_sdk_container bash
    ```
4. Navigate to transfered directory
    ```bash
    cd /docker_volume/src/bash_scripts
    ```
5. Run data collection script
    ```bash
    ./data_collection.sh
    ```

### 01-get-pc



### 02-pointcloud-projection



### 03-annotations



### 04-model



### 05-get-mask


### 06-scale-mask



### 07-crop-pc




## Miscellaneous

To Copy New Directory Structure:

```find . -type d -not -path "./.git/*" > directory_structure.txt```


For access to the data submit a request via the discussion board




two avenues -> docker container version and conda version, 
