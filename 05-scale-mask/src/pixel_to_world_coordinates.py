import cv2
import numpy as np

# Intrinsic parameters (from your camera calibration)
fx = 1069.66
fy = 1069.57
cx = 961.73
cy = 529.245
k1 = -0.0514866
k2 = 0.0238413
p1 = 0.000217693
p2 = -0.000148725

# Load your point cloud data
# Replace this with your actual point cloud data loading code
# point_cloud = np.load('point_cloud.npy')

# Pixel coordinates (x, y)
x_pixel = 200
y_pixel = 300

# Normalize pixel coordinates
u = (x_pixel - cx) / fx
v = (y_pixel - cy) / fy

# Apply distortion correction
dist_coeffs = np.array([k1, k2, p1, p2, 0.0])  # k3, k4, k5 not used
distorted_points = cv2.undistortPoints(np.array([[u, v]], dtype=np.float32), cameraMatrix=np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]]), distCoeffs=dist_coeffs)
u_distorted = distorted_points[0][0][0]
v_distorted = distorted_points[0][0][1]

# Convert to world coordinates (X, Y)
X_camera_centric = u_distorted
Y_camera_centric = v_distorted

# Scaling factors to match point cloud scale
scaling_factor_x = 1.0  # Adjust as needed
scaling_factor_y = 1.0  # Adjust as needed
# scaling_factor = depth / np.sqrt(u**2 + v**2 + 1) # scaling factor based on depth


# Map to point cloud
X_world = X_camera_centric * scaling_factor_x
Y_world = Y_camera_centric * scaling_factor_y

print("Pixel Coordinates (x, y):", x_pixel, y_pixel)
print("World Coordinates (X, Y):", X_world, Y_world)
