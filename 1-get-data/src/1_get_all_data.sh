#!/bin/bash



SOURCE_DIR=../data/current-data
files=(
   "$SOURCE_DIR"/*
)

#filename=$(first_test)
#echo File Name: ${filename}

# printf '%s\n' "${files[@]##*/}"

# for file in "${files[@]}";
# do
#     if [[ $file == *"06.00.00_png_ultra"* ]] || [[ $file == *"12.00.00_png_ultra"* ]] || [[ $file == *"18.00.00_png_ultra"* ]]; then
#         echo "$file"
#         python3 get_data.py "$file"
#     fi

# done		

for file in "${files[@]}";
do
    if [[ $file == *"png_ultra"* ]]; then
        echo "$file"
        python3 "1_get_data.py" "$file"
    fi

done	
