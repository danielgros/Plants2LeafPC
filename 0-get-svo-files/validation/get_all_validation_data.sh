#!/bin/bash

SOURCE_DIR=../data/current-data
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
    fi

done	
