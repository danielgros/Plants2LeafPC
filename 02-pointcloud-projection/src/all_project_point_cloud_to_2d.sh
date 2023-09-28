#!/bin/bash

# python3 "project_point_cloud_to_2d.py" \
#     "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/02-pointcloud-projection/data/raw/left_photo_2023-01-31_08.00.00_png_ultra.jpg" \
#     "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/02-pointcloud-projection/data/processed/pc_csvs/pc_2023-01-31_08.00.00_png_ultra.csv" \
#     "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/02-pointcloud-projection/data/processed/projected_image_2023-01-31_08.00.00_png_ultra.jpg" \
#     "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/02-pointcloud-projection/data/processed/projected_image_data_2023-01-31_08.00.00_png_ultra.txt"

# python3 "project_point_cloud_to_2d.py" \
#     "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/02-pointcloud-projection/data/raw/left_photo_2023-03-04_08.00.00_png_ultra.jpg" \
#     "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/02-pointcloud-projection/data/processed/pc_csvs/pc_2023-03-04_08.00.00_png_ultra.csv" \
#     "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/02-pointcloud-projection/data/processed/projected_image_2023-03-04_08.00.00_png_ultra.jpg" \
#     "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/02-pointcloud-projection/data/processed/projected_image_data_2023-03-04_08.00.00_png_ultra.txt"


# Define the directories
raw_dir="../data/raw"
csvs_dir="../data/processed/pc_csvs"
output_dir="../data/processed"

# Loop through the raw directory
for jpg_file in "$raw_dir"/left_photo*.jpg; do
    # Extract the common sequence from the file name
    common_sequence=$(basename "$jpg_file" | sed 's/^left_photo//' | sed 's/\.jpg$//')
    
    # Define the output file names
    csv_file="$csvs_dir/pc${common_sequence}.csv"
    output_jpg_file="$output_dir/projected_image${common_sequence}.jpg"
    output_txt_file="$output_dir/projected_image_data${common_sequence}.txt"

    # Print Names
    echo "JPG file: $jpg_file"
    echo "CSV file: $csv_file"
    echo "OUTPUT JPG file: $output_jpg_file"
    echo "OUTPUT DATA file: $output_txt_file"

    # Call the Python script with the parameters
    python3 "project_point_cloud_to_2d.py" "$jpg_file" "$csv_file" "$output_jpg_file" "$output_txt_file"
done
