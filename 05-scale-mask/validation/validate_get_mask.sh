#!/bin/bash

python3 "./mask_to_color_image.py" \
    "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/05-scale-mask/data/raw/masks_2023-01-21_20.txt" \
    "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/05-scale-mask/data/raw/left_photo_2023-01-21_20.00.00_png_ultra.jpg" \
    "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/05-scale-mask/data/validation/color_"

python3 "./mask_to_color_image.py" \
    "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/05-scale-mask/data/raw/masks_2023-01-31_08.txt" \
    "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/05-scale-mask/data/raw/left_photo_2023-01-31_08.00.00_png_ultra.jpg" \
    "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/05-scale-mask/data/validation/color_"

python3 "./mask_to_color_image.py" \
    "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/05-scale-mask/data/raw/masks_2023-02-26_08.txt" \
    "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/05-scale-mask/data/raw/left_photo_2023-02-26_08.00.00_png_ultra.jpg" \
    "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/05-scale-mask/data/validation/color_"

python3 "./mask_to_color_image.py" \
    "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/05-scale-mask/data/raw/masks_2023-03-04_08.txt" \
    "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/05-scale-mask/data/raw/left_photo_2023-03-04_08.00.00_png_ultra.jpg" \
    "/hdd/gros2/maskrcnn/samples/plants_to_leaf_area/05-scale-mask/data/validation/color_"
