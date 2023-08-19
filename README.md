# Senior Thesis Project

docker run --gpus all -it --privileged -v docker:/docker_volume stereolabs/zed:3.8-devel-cuda10.2-ubuntu18.04

to exit:
Type Ctrl+p then Ctrl+q.


to enter 
docker exec -it <continaer id> bash

https://www.stereolabs.com/docs/docker/install-guide-linux/



To Copy Directory Structure:

```find . -type d -not -path "./.git/*" > directory_structure.txt```