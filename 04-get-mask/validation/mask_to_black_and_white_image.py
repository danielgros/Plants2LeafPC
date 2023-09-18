import numpy as np
from PIL import Image
import pickle
import sys

mask_path = sys.argv[1]
image_path = sys.argv[2]

with open(mask_path, 'rb') as f:
    masks = pickle.load(f)

for mask_key in masks.keys():

    mask = masks[mask_key]

    # Conver the list to a numpy array
    array = np.array(mask)

    # Convert true to black and false to white
    array = np.where(array, 0, 255)

    # Reshape the array to remove singleton dimension
    array = array.squeeze()

    # Convert the numpy array to a PIL image
    image = Image.fromarray(array.astype('uint8'), 'L')  # 'L' mode for grayscale

    # Save the image
    image.save(image_path + mask_key + ".jpg")
