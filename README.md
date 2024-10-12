---
created: 2024-05-03T20:20
modified: 2024-08-04T21:52
---
# Plants2LeafPC: Acquisition of Leaf Point Cloud Data Via Stereo Images and Computer Vision Methods

## Project Overview

UIUC researchers are experimenting with genetic modifications on plants and tracking their growth to measure the effectiveness of these modifications on the plant’s ability to survive in drier and hotter climates. Metrics that communicate the quality of growth can be gathered from a leaf’s phenotype data, including its width. This research project aims at making extraction of phenotype data easier, as in the case of leaf width, by providing researchers with an accurate and precise model of individual leaves.

A vision-based method using stereo images was developed to acquire a 3D model of a leaf. First a stereo camera was utilized to capture recordings of a scene and generate point clouds. Then, the point clouds were projected onto a 2D representation to run a trained instance segmentation model on them to detect leaves in the 2D representation and predict leaf masks. These masks were used as filters on these 2D representations to acquire leaf point clouds after reprojection to 3D.

This research project and the resulting software produced by it demonstrate an effective workflow for acquiring leaf point clouds with birds-eye-view stereo images. Although the accuracy of some measurements doesn’t make the product of this project ready to be shared, the results give empirical evidence that the method utilized is able to go through the process of acquiring leaf models for plants in environments with dense leaf clusters. These products are a step in allowing leaf phenotype measurements to be taken with ease, helping researchers track plant growth and improve their experiments.

## Project Setup
> **Note:** This setup guide is not comprehensive and there may be steps missing.


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
5. Run setup.py
    ```bash
    python3 setup.py install
    ``` 
6. Download pre-trained COCO weights (mask_rcnn_coco.h5) from the [releases page](https://github.com/matterport/Mask_RCNN/releases) into the Mask_RCNN directory.
7. Exit conda environment
    ```
    conda deactivate
    ```

### ZED SDK Setup

1. Download and install docker: https://www.docker.com/products/docker-desktop/
2. Browse the ZED SDK Docker Images at https://hub.docker.com/r/stereolabs/zed/tags?page=1
3. Select one based on your OS and GPUs
4. Download the image onto your machine (using 3.8-devel-cuda10.2-ubuntu18.04 as an example)
    ```bash
    docker pull stereolabs/zed:3.8-devel-cuda10.2-ubuntu18.04
    ```
5. Spin up a container using the downloaded image (using 3.8-devel-cuda10.2-ubuntu18.04 as an example)
    ```bash
    docker run --gpus all -it --name zed_sdk_container --privileged -v docker:/docker_volume stereolabs/zed:3.8-devel-cuda10.2-ubuntu18.04 bash
    ```
6. Install ZED SDK in container (in current directory: /usr/local/zed)
    ```bash
    python3 get_python_api.py
    ```
7. To exit the container type Ctrl+p then Ctrl+q


## Use Guide
> **Note:** This usage guide is not comprehensive and there may be steps missing.


### 00-get-svo-files
This step is used to capture recordings using the ZED Camera.

1. Make sure the ZED Camera is connected to a machine with the ZED SDK installed and the Plants2LeafPC/00-get-svo-files directory
2. Navigate to Plants2LeafPC
3. Transfer over files into container
    ```bash
    docker cp 00-get-svo-files zed_sdk_container:/docker_volume
    ```
4. Enter the spun up container with the ZED SDK install
    ```bash
    docker exec -it zed_sdk_container bash
    ```
5. Navigate to transfered directory
    ```bash
    cd /docker_volume/00-get-svo-files/src/bash_scripts
    ```
6. Make data collection file executable
    ```
    chmod +x ./data_collection.sh
    ```
7. Run data collection script
    ```bash
    ./data_collection.sh
    ```
8. To exit the container type Ctrl+p then Ctrl+q

### 01-get-pc
This step is used to convert the ZED camera recordings into point clouds

1. Navigate to Plants2LeafPC
2. Transfer over files into container
    ```bash
    docker cp 01-get-pc zed_sdk_container:/docker_volume
    ```
3. Enter the spun up container with the ZED SDK install
    ```bash
    docker exec -it zed_sdk_container bash
    ```
4. Navigate to transfered directory
    ```bash
    cd /docker_volume/01-get-pc/src
    ```
5. Make point cloud acquisition file executable
    ```
    chmod +x ./get_all_pcs.sh
    ```
6. Run conversion script
    ```bash
    ./get_all_pcs.sh 
    ```
7. To exit the container type Ctrl+p then Ctrl+q

### 02-pointcloud-projection
This step converts the point clouds into more easily used formats: csv file + 2d image 

1. Activate general conda environment
    ```
    conda activate general_env
    ```
2. Navigate to Plants2LeafPC/02-pointcloud-projection/src
3. Run script to turn point cloud into a csv file of pixel color values
    ```
    ./all_pc_to_csv.sh
    ```
4. Run script to turn point clouds into a 2d image representation (for training the model)
    ```
    ./all_project_point_cloud_to_2d.sh
    ```
5. Deactivate conda environment
    ```
    conda deactivate
    ```

### 03-annotations
This step includes annotating the images for training the Mask RCNN model

1. Go to the VGG Image Annotator website: https://annotate.officialstatistics.org/
2. Follow the provided steps to annotate images
3. Save images within 03-annotations/data/images/
4. Save annotations within 03-annotations/data/annots/
5. Activate general conda environment
    ```
    conda activate general_env
    ```
6. To transform the annotations into a format more easily readable by the Mask RCNN model, navigate to 03-annotations/src and execute:
    ```
    python3 annots_transformation.py
    ```
7. To copy over the images and annotations to the model folder execute:
    ```
    ./copy_images_and_annots_transformation.sh
    ```
8. Deactivate conda environment
    ```
    conda deactivate
    ```

### 04-model
This step trains the model to be able to perform instance segmentation as defined in the annotated images.

1. Activate ml_model conda environment
    ```
    conda activate ml_model_env
    ```
2. Navigate to 04-model/src
3. Execute
    ```
    python3 leaves_model.py
    ```
4. Deactivate conda environment
    ```
    conda deactivate
    ```

### 05-get-mask
This step uses the trained Mask RCNN model to obtain leaves (masks) for an image

1. Activate ml_model conda environment
    ```
    conda activate ml_model_env
    ```
2. Navigate to 05-get-mask/src
3. Execute
    ```
    python3 get_mask.py
    ```
4. Deactivate conda environment
    ```
    conda deactivate
    ```

### 06-scale-mask
This step scales the leaf masks obtained from the model to the sizes of the original point clouds

1. Activate general conda environment
    ```
    conda activate general_env
    ```
2. Navigate to 06-scale-mask/src
3. Execute
    ```
    ./scale_all_masks.sh
    ```
4. Deactivate conda environment
    ```
    conda deactivate
    ```

### 07-crop-pc
This step crops the point cloud based on the leaf masks

1. Activate general conda environment
    ```
    conda activate general_env
    ```
2. Navigate to 07-crop-pc/src
3. Execute
    ```
    ./crop_all_pcs.sh
    ```
4. Deactivate conda environment
    ```
    conda deactivate
    ```

---

## Miscellaneous

To Copy New Directory Structure: ```find . -type d -not -path "./.git/*" > directory_structure.txt```


For access to sorghum plant recordings submit a request via the discussion board
