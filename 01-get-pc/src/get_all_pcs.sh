#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Usage: $0 <source_dir>"
  exit 1
fi

SOURCE_DIR="$1"
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
