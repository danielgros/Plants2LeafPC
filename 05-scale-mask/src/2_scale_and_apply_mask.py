import pickle
import numpy as np
from scipy.ndimage import zoom

def scale_mask(mask, new_height, new_width):
    y, x, z = np.array(mask).shape

    # Calculate scaling factors
    x_scale = new_width / x
    y_scale = new_height / y

    # Scale the mask using nearest-neighbor interpolation
    scaled_mask = zoom(mask, (x_scale, y_scale, 1), order=0)

    # Convert the scaled mask to boolean values (True/False)
    scaled_mask = scaled_mask >= 0.5

    # Print the original and scaled masks
    # print("Original Mask:")
    # print(mask)

    # print("\nScaled Mask:")
    # print(scaled_mask)

    return scaled_mask


def main():
    # mask_path = sys.argv[1]
    # point_cloud_path = sys.argv[2]

    mask_path = "../data/masks.txt"
    with open(mask_path, 'rb') as f:
        masks = pickle.load(f)

    # list of each leaf mask on the image
    list_keys = list(masks.keys())
    print(np.array(masks[list(masks.keys())[0]]).shape)

    point_cloud_data_path = "../data/projected_image_data.txt"
    with open(point_cloud_data_path, 'rb') as f:
        point_cloud_data = pickle.load(f)

    print(np.array(point_cloud_data).shape)
    projected_image_height, projected_image_width = np.array(point_cloud_data).shape

    scaled_mask = {}

    for mask_key in list_keys:
        scaled_mask[mask_key] = scale_mask(masks[mask_key], projected_image_height, projected_image_width)


    output_filename = '../data/scaled_mask.txt'

    with open(output_filename, 'wb') as f:
        pickle.dump(scaled_mask, f)


if __name__ == "__main__":
    main()