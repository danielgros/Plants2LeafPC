# Senior Thesis Project

## Project Overview

## Project Setup

### Matterport Mask-RCNN Setup

### Conda Environment Setup

### ZED SDK Setup


run the docker container

```docker run --gpus all -it --privileged -v docker:/docker_volume stereolabs/zed:3.8-devel-cuda10.2-ubuntu18.04```

to exit the docker container:
Type Ctrl+p then Ctrl+q.


to enter the docker container:

```docker exec -it <continaer id> bash```


https://www.stereolabs.com/docs/docker/install-guide-linux/


## Miscellaneous

To Copy Directory Structure:

```find . -type d -not -path "./.git/*" > directory_structure.txt```