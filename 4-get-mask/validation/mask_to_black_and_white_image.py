import numpy as np
from PIL import Image
import pickle

mask_path = '../data/validation/mask.txt'

with open(mask_path, 'rb') as f:
    masks = pickle.load(f)

mask = masks[list(masks.keys())[0]]

# Conver the list to a numpy array
array = np.array(mask)

# Convert true to black and false to white
array = np.where(array, 0, 255)

# Reshape the array to remove singleton dimension
array = array.squeeze()

# Convert the numpy array to a PIL image
image = Image.fromarray(array.astype('uint8'), 'L')  # 'L' mode for grayscale

# Save the image
image.save('../data/validation/output/leaf_image_black_and_white.jpg')
