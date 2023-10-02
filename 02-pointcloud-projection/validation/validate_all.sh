#!/bin/bash

# python3 "./validate_projected_pc.py" \
#     "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/02-pointcloud-projection/data/processed/projected_image_2023-01-30_08.00.00_png_ultra.jpg" \
#     "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/02-pointcloud-projection/data/processed/projected_image_data_2023-01-30_08.00.00_png_ultra.txt"

# Define the directory
dir="../data/processed"

# Loop through the raw directory
for jpg_file in "$dir"/projected_image*.jpg; do
    # Extract the common sequence from the file name
    common_sequence=$(basename "$jpg_file" | sed 's/^projected_image//' | sed 's/\.jpg$//')
    
    # Define the output file names
    pc_file="$dir/projected_image_data${common_sequence}.txt"

    # Print Names
    echo "JPG file: $jpg_file"
    echo "PC file: $pc_file"

    # Call the Python script with the parameters
    python3 "validate_projected_pc.py" "$jpg_file" "$pc_file"
done
