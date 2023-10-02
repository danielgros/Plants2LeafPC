#!/bin/bash

# Define the directory
input_dir="../data/raw"
output_dir="../data/processed"

# Loop through the raw directory
for mask_file in "$input_dir"/scaled_mask*.jpg; do
    # Extract the common sequence from the file name
    common_sequence=$(basename "$mask_file" | sed 's/^scaled_mask//' | sed 's/\.txt$//')
    
    # Define the output file names
    pc_file="$input_dir/projected_image_data${common_sequence}.txt"
    cropped_pc_file="$output_dir/cropped_pc${common_sequence}.txt"
    emphasized_pc_file="$output_dir/emphasized_pc${common_sequence}.txt"

    # Print Names
    echo "Mask file: $mask_file"
    echo "PC file: $pc_file"
    echo "Cropped PC file" "$cropped_pc_file"
    echo "Emphasized PC file" "$emphasized_pc_file"

    # Call the Python script with the parameters
    python3 "validate_projected_pc.py" "$mask_file" "$pc_file" "$cropped_pc_file" "$emphasized_pc_file"
    python3 "pc_to_csv.py" "$cropped_pc_file"
    python3 "pc_to_csv.py" "$emphasized_pc_file"
done
