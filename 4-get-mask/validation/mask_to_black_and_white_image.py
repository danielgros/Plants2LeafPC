import numpy as np
from PIL import Image
import pickle

mask_path = './mask.txt'

# Create a random true/false array of size 1024x1024x1
# array = np.random.choice([True, False], size=(1024, 1024, 1))
with open(mask_path, 'rb') as f:
    mask = pickle.load(f)


array = np.array(mask)

print(array.shape)

# Convert true to black and false to white
# array = np.where(array, 0, 255)

# # Reshape the array to remove singleton dimension
# array = array.squeeze()

# # Convert the numpy array to a PIL image
# image = Image.fromarray(array.astype('uint8'), 'L')  # 'L' mode for grayscale

# # Save the image
# image.save('output_image.png')
