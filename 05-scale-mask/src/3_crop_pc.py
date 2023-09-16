import pickle
import numpy as np

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
    
    
    output_filename = "../data/cropped_pc.txt"

    with open(output_filename, 'wb') as f:
        pickle.dump(cropped_pc, f)

if __name__ == "__main__":
    main()