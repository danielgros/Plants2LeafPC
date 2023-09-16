import pickle
import numpy as np

def color_point(point):
    x, y, z, r, g, b, a = point
    return [x, y, z, 255, 0, 0, 255]

def main():

    scaled_mask_path = "../data/scaled_mask.txt"
    with open(scaled_mask_path, 'rb') as f:
        masks = pickle.load(f)

    # list of each leaf mask on the image
    list_keys = list(masks.keys())
    print(np.array(masks[list(masks.keys())[0]]).shape)

    point_cloud_data_path = "../data/projected_image_data.txt"
    with open(point_cloud_data_path, 'rb') as f:
        point_cloud_data = pickle.load(f)

    print(np.array(point_cloud_data).shape)
    projected_image_height, projected_image_width = np.array(point_cloud_data).shape

    cropped_pc = []
    emphasized_pc = []

    mask = masks[list_keys[0]]

    for height_coordinate in range(0, projected_image_height):
        for width_coordinate in range(0, projected_image_width):
            if mask[height_coordinate][width_coordinate][0] == True:
                for point in point_cloud_data[height_coordinate][width_coordinate]:
                    cropped_pc.append(point)
                    emphasized_pc.append(color_point(point))
            else:
                for point in point_cloud_data[height_coordinate][width_coordinate]:
                    emphasized_pc.append(point)
    
    print("cropped_pc", np.array(cropped_pc).shape)

    print("emphasized_pc", np.array(emphasized_pc).shape)

    
    output_filename = "../data/cropped_pc.txt"

    with open(output_filename, 'wb') as f:
        pickle.dump(cropped_pc, f)

    output_filename = "../data/emphasized_pc.txt"

    with open(output_filename, 'wb') as f:
        pickle.dump(emphasized_pc, f)

if __name__ == "__main__":
    main()