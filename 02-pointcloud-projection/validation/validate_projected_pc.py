import numpy as np
import sys
import pickle
import cv2

def main():
    point_cloud_image_path = sys.argv[1]
    point_cloud_data_path = sys.argv[2]

    with open(point_cloud_data_path, 'rb') as f:
        point_cloud_data = pickle.load(f)

    data_shape = np.array(point_cloud_data).shape
    image_shape = cv2.imread(point_cloud_image_path).shape[:2]    
    print(data_shape)
    print(image_shape)

    assert data_shape[0] == image_shape[0]
    assert data_shape[1] == image_shape[1]



if __name__ == "__main__":
    main()
