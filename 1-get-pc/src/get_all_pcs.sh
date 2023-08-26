#!/bin/bash



SOURCE_DIR=../data/data-collection-room-1/used_svo
files=(
   "$SOURCE_DIR"/*
)

printf '%s\n' "${files[@]##*/}"

for file in "${files[@]}";
do
    if [[ $file == *"08.00.00_png_ultra"* ]] || [[ $file == *"10.00.00_png_ultra"* ]] || [[ $file == *"16.00.00_png_ultra"* ]] || [[ $file == *"18.00.00_png_ultra"* ]]; then
        echo "$file"
        python3 get_pc.py "$file"
    fi

done		

# for file in "${files[@]}";
# do
#     if [[ $file == *"png_ultra"* ]]; then
#         echo "$file"
#         python3 "get_pc.py" "$file"
#     fi

# done	
