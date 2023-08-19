#!/bin/bash


#filename=$(first_test)
#echo File Name: ${filename}

SOURCE_DIR=./data
files=(
   "$SOURCE_DIR"/*
)



# printf '%s\n' "${files[@]##*/}"

for file in "${files[@]}";
do
    if [[ $file == *"06.00.00_png_ultra"* ]] || [[ $file == *"12.00.00_png_ultra"* ]] || [[ $file == *"18.00.00_png_ultra"* ]]; then
        echo "$file"
        python3 get_data.py "$file"
    fi

done		
