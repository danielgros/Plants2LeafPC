import pickle
import numpy as np
from scipy.ndimage import zoom
import sys
import cv2

def scale_mask(mask, new_height, new_width):
    print(np.array(mask).shape)
    height, width, _depth = np.array(mask).shape

    # Calculate scaling factors
    height_scale = new_height / height
    width_scale = new_width / width

    # Scale the mask using nearest-neighbor interpolation
    scaled_mask = zoom(mask, (height_scale, width_scale, 1), order=0, mode='nearest')

    # Convert the scaled mask to boolean values (True/False)
    scaled_mask = scaled_mask >= 1

    return scaled_mask


def main():
    mask_path = sys.argv[1]
    point_cloud_data_path = sys.argv[2]
    scaled_mask_path = sys.argv[3]

    with open(mask_path, 'rb') as f:
        masks = pickle.load(f)

    # list of each leaf mask on the image
    list_keys = list(masks.keys())
    print(np.array(masks[list(masks.keys())[0]]).shape)

    # with open(point_cloud_data_path, 'rb') as f:
    #     point_cloud_data = pickle.load(f)

    # print(np.array(point_cloud_data).shape)
    # projected_image_height, projected_image_width = np.array(point_cloud_data).shape
    projected_image_height, projected_image_width = cv2.imread(point_cloud_data_path).shape[:2]
    print(projected_image_height, projected_image_width)

    scaled_mask = {}

    for mask_key in list_keys:
        scaled_mask[mask_key] = scale_mask(masks[mask_key], projected_image_height, projected_image_width)

    with open(scaled_mask_path, 'wb') as f:
        pickle.dump(scaled_mask, f)



if __name__ == "__main__":
    main()
