#!/bin/bash

# Define the directory
proj_dir="../data/processed"
val_dir="../data/validation"

# Loop through the raw directory
for proj_file in "$proj_dir"/projected_image_data*.txt; do
    # Extract the common sequence from the file name
    common_sequence=$(basename "$proj_file" | sed 's/^projected_image_data//' | sed 's/\.txt$//')
    
    # Define the output file names
    pc_file="$val_dir/validate_projected_image_data${common_sequence}.txt"

    # Print Names
    echo "Projection file: $proj_file"
    echo "PC file: $pc_file"

    # Call the Python script with the parameters
    python3 "projected_point_cloud_to_3d.py" "$proj_file" "$pc_file"
done
