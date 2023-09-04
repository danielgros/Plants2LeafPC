#!/bin/bash

python3 "../src/get_mask.py" 
python3 "./mask_to_color_image.py"
python3 "./mask_to_black_and_white_image.py"