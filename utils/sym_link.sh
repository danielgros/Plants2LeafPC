#!/bin/bash

# Specify the source directory containing the files
SOURCE_DIR="/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/01-get-pc/data/processed/sample/output"

# Specify the output directory for the symbolic links
OUTPUT_DIR="/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/05-scale-mask/data/raw"

# Check if the source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
  echo "Source directory does not exist: $SOURCE_DIR"
  exit 1
fi

# Check if the output directory exists, or create it if it doesn't
if [ ! -d "$OUTPUT_DIR" ]; then
  mkdir -p "$OUTPUT_DIR"
fi

# Loop through the files in the source directory
for file in "$SOURCE_DIR"/*; do
  # Check if it's a regular file
  if [ -f "$file" ]; then
    # Extract the filename from the path
    filename=$(basename "$file")
    # Create a symbolic link in the output directory with the same name
    ln -sf "$file" "$OUTPUT_DIR/$filename"
  fi
done
