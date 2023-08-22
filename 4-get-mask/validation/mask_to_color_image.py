from PIL import Image, ImageDraw
import numpy as np
import pickle

mask_path = '../data/validation/mask.txt'

with open(mask_path, 'rb') as f:
    masks = pickle.load(f)

mask = masks[list(masks.keys())[0]]

# Conver the list to a numpy array
mask_array = np.array(mask)

# Load the image 
IMAGE_PATH = '../data/validation/photo.jpg'
image = Image.open(IMAGE_PATH)

# Create a copy of the image to draw highlights on
highlighted_image = image.copy()

# Define the highlight color (change this to your desired color)
highlight_color = (255, 0, 0, 128)  # Red color

# Create a Pillow draw object
draw = ImageDraw.Draw(highlighted_image)

# Iterate through the mask_array and draw highlights where True
for y in range(mask_array.shape[0]):
    for x in range(mask_array.shape[1]):
        if mask_array[y, x, 0]:
            draw.rectangle([x, y, x + 1, y + 1], outline=highlight_color)

# Save or display the highlighted image
highlighted_image.save('../data/validation/output/leaf_image_color.jpg')  # Save the highlighted image