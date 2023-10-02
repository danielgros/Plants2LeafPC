import pickle
import numpy as np
import sys

def color_point(point):
    x, y, z, r, g, b, a = point
    return [x, y, z, 255, 0, 0, 255]

def main():

    mask_file = sys.argv[1]
    projected_image_data_file = sys.argv[2]
    cropped_pc_file = sys.argv[3]
    emphasized_pc_file = sys.argv[3]

    with open(mask_file, 'rb') as f:
        masks = pickle.load(f)

    # list of each leaf mask on the image
    list_keys = list(masks.keys())
    print(np.array(masks[list(masks.keys())[0]]).shape)

    with open(projected_image_data_file, 'rb') as f:
        point_cloud_data = pickle.load(f)

    print(np.array(point_cloud_data).shape)
    projected_image_height, projected_image_width = np.array(point_cloud_data).shape

    cropped_pc = []
    emphasized_pc = []

    for mask_key in list_keys:
        for height_coordinate in range(0, projected_image_height):
            for width_coordinate in range(0, projected_image_width):
                if masks[mask_key][height_coordinate][width_coordinate][0]:
                    for point in point_cloud_data[height_coordinate][width_coordinate]:
                        cropped_pc.append(point)
                        emphasized_pc.append(color_point(point))
                else:
                    for point in point_cloud_data[height_coordinate][width_coordinate]:
                        emphasized_pc.append(point)
    
        print("cropped_pc", np.array(cropped_pc).shape)
        print("emphasized_pc", np.array(emphasized_pc).shape)

        with open(cropped_pc_file + mask_key + ".txt", 'wb') as f:
            pickle.dump(cropped_pc, f)

        with open(emphasized_pc_file + mask_key + ".txt", 'wb') as f:
            pickle.dump(emphasized_pc, f)

if __name__ == "__main__":
    main()