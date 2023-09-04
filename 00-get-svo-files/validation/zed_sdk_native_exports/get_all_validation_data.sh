#!/bin/bash

SOURCE_DIR=../../data/camera-callibration-new/used_svo
files=(
   "$SOURCE_DIR"/*
)

for file in "${files[@]}";
do
    if [[ $file == *"png_ultra"* ]]; then
        echo "$file"
        python3 "export_mesh.py" "$file"
        python3 "export_point_cloud.py" "$file"
        python3 "export_2d_images.py" "$file"
        python3 "export_depth_image.py" "$file"
    fi

done	
