import csv
import math
import pickle
import cv2
import numpy as np
import sys


def projectionToPC():
    if len(sys.argv) != 3:
        print("Usage: python3 project_point_cloud_to_2d.py <left_image_path> <point_cloud_path> <projected_image_path> <projected_image_data_path>")
        sys.exit(1)

    projected_image_data_path = sys.argv[1]
    output_point_cloud_path = sys.argv[2]

    with open(projected_image_data_path, 'rb') as f:
        projection = pickle.load(f)

    height, width = projection.shape
    point_cloud = []
    
    for r in range(0, height):
        for c in range(0, width):
            for point in projection[r, c]:
                point_cloud.append(point)

    with open(output_point_cloud_path, 'wb') as f:
        pickle.dump(point_cloud, f)


if __name__ == "__main__":
    projectionToPC()
