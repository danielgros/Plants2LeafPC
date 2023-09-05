import cv2
import numpy as np
import pickle

def main():
    # Intrinsic parameters (from camera calibration)
    fx=1069.66
    fy=1069.57
    k1=-0.0514866
    k2=0.0238413
    p1=0.000217693
    p2=-0.000148725
    k3=-0.00954097
    #FHD:
    # cx=961.73
    # cy=529.245
    #2K:
    cx=1105.73
    cy=610.245

    # Load your point cloud data (replace this with actual data loading)
    # point_cloud = np.load('point_cloud.npy')
    point_cloud_path = "../data/pc_2023-01-31_08.00.00_png_ultra.txt"
    with open(point_cloud_path, 'rb') as f:
        point_cloud = pickle.load(f)

    print((np.array(point_cloud).shape))

    target_image = cv2.imread('../data/left_photo_2023-01-31_08.00.00_png_ultra.jpg')

    # Extrinsic properties
    baseline = 119.887
    TY = -0.204801
    TZ = 0.0658791
    RX = 0.000977292
    RZ = 0.00274544

    # Initialize intrinsic and extrinsic parameters
    intrinsic_params = np.array([fx, fy, k1, k2, p1, p2, k3])
    extrinsic_params = np.array([baseline, TY, TZ, RX, RZ])
    optical_center = np.array([cx, cy])

    image = project_point_cloud(point_cloud, intrinsic_params, extrinsic_params, optical_center, target_image.shape)

    # Print minimum and maximum x, y pixel coordinates
    min_x = np.min(np.where(image > 0)[1])
    max_x = np.max(np.where(image > 0)[1])
    min_y = np.min(np.where(image > 0)[0])
    max_y = np.max(np.where(image > 0)[0])
    print("Min X Pixel:", min_x)
    print("Max X Pixel:", max_x)
    print("Min Y Pixel:", min_y)
    print("Max Y Pixel:", max_y)

    # Save the resulting image
    cv2.imwrite('../data/projected_image.png', image)



def project_point_cloud(point_cloud, intrinsic_params, extrinsic_params, optical_center, target_image_shape):
    # Image dimensions (replace with the actual dimensions of your image)
    # image_width = 1920
    # image_height = 1080
    image_height, image_width, _ = target_image_shape

    fx, fy, k1, k2, p1, p2, k3 = intrinsic_params.detach().numpy()
    baseline, TY, TZ, RX, RZ = extrinsic_params.detach().numpy()
    cx, cy = optical_center.detach().numpy()

    # Transformation matrix based on extrinsic properties
    R = cv2.Rodrigues(np.array([RX, TY, RZ]))[0]
    T = np.array([baseline / 2, TY, TZ])

    # Create an empty image
    image = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    projected_points = []

    # Iterate through points and project onto the 2D image
    for point in point_cloud:
        # Extract coordinates and color information
        x, y, z, r, g, b, a = point
        
        # Apply extrinsic transformation
        transformed_point = np.dot(R, np.array([x, y, z])) + T
        
        # Project to 2D using intrinsic parameters
        projected_point, _ = cv2.projectPoints(
            np.array([transformed_point]), 
            np.zeros((3,)), 
            np.zeros((3,)), 
            np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]]), 
            np.array([k1, k2, p1, p2, k3]))
        projected_points.append(projected_point)

        # Extract pixel coordinates
        x_pixel = int(projected_point[0][0][0])
        y_pixel = int(projected_point[0][0][1])
        
        # Check if the projected point is within image bounds
        if 0 <= x_pixel < image_width and 0 <= y_pixel < image_height:
            # Assign color information to the image
            image[y_pixel, x_pixel] = [r, g, b]
    
    projected_image = cv2.resize(image, (image_width, image_height))

    return projected_image


if __name__ == "__main__":
    main()