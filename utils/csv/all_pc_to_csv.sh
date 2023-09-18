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
    if [[ $file == *".txt"* ]]; then
        echo "$file"
        python3 pc_to_csv.py "$file"
    fi
done
