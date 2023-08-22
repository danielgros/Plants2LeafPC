#!/bin/bash



SOURCE_DIR=../data/camera-callibration-new/used_svo
files=(
   "$SOURCE_DIR"/*
)

printf '%s\n' "${files[@]##*/}"

for file in "${files[@]}";
do
    if [[ $file == *"png_ultra"* ]]; then
        echo "$file"
        python3 "get_pc.py" "$file"
    fi

done	
