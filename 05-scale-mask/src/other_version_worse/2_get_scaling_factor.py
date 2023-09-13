import cv2
import numpy as np
from scipy.optimize import minimize

# Intrinsic parameters (from your camera calibration)
fx = 1069.66
fy = 1069.57
cx = 961.73
cy = 529.245
k1 = -0.0514866
k2 = 0.0238413

# Pixel coordinates (x, y)
x_pixel = 200
y_pixel = 300

# Initial estimates
initial_depth = 5.0
initial_scaling_factor = 1.0
initial_point = np.array([0.0, 0.0])  # Initial point in the point cloud

def objective(params):
    depth, scaling_factor, point = params
    
    # Calculate normalized coordinates (u, v)
    u = (x_pixel - cx) / fx
    v = (y_pixel - cy) / fy
    
    # Calculate scaling factor
    scaling_factor_calc = depth / np.sqrt(u**2 + v**2 + 1)
    
    # Calculate estimated pixel coordinates
    u_estimated = u * scaling_factor
    v_estimated = v * scaling_factor
    
    # Calculate error
    error = np.sqrt((u_estimated - point[0])**2 + (v_estimated - point[1])**2)
    return error

# Minimize the objective function to estimate depth, scaling factor, and point
result = minimize(objective, [initial_depth, initial_scaling_factor, initial_point])

depth_estimate, scaling_factor_estimate, point_estimate = result.x

print("Pixel Coordinates (x, y):", x_pixel, y_pixel)
print("Estimated Depth:", depth_estimate)
print("Estimated Scaling Factor:", scaling_factor_estimate)
print("Estimated Point in Point Cloud:", point_estimate)
