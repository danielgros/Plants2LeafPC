#!/bin/bash


SOURCE_DIR=../data/data-collection-room-2/output
files=(
   "$SOURCE_DIR"/*
)

printf '%s\n' "${files[@]##*/}"

for file in "${files[@]}";
do
    if [[ $file == *".txt"* ]]; then
        echo "$file"
        python3 pc_to_csv.py "$file"
    fi

done		
