import cv2
import numpy as np
import pickle
import torch
import torch.optim as optim

from world_to_pixel_coordinates import project_point_cloud

# Load point cloud data and target image (replace with actual data loading)
point_cloud_path = "../data/pc_2023-01-31_08.00.00_png_ultra.txt"
with open(point_cloud_path, 'rb') as f:
    point_cloud = pickle.load(f)
target_image = cv2.imread('../data/left_photo_2023-01-31_08.00.00_png_ultra.jpg')

# Intrinsic parameters (from camera calibration)
fx = 1069.66
fy = 1069.57
k1 = -0.0514866
k2 = 0.0238413
p1 = 0.000217693
p2 = -0.000148725
k3 = -0.00954097
# FHD:
# cx = 961.73
# cy = 529.245
# 2K:
cx = 1105.73
cy = 610.245

# Extrinsic properties
baseline = 119.887
TY = -0.204801
TZ = 0.0658791
RX = 0.000977292
RZ = 0.00274544

# Convert everything to PyTorch tensors with gradient computation enabled
initial_intrinsic_params = torch.tensor([fx, fy, k1, k2, p1, p2, k3], dtype=torch.float32, requires_grad=True)
initial_extrinsic_params = torch.tensor([baseline, TY, TZ, RX, RZ], dtype=torch.float32, requires_grad=True)
initial_optical_center = torch.tensor([cx, cy], dtype=torch.float32, requires_grad=True)

# Create an optimizer for all parameters
optimizer = optim.SGD([initial_intrinsic_params, initial_extrinsic_params, initial_optical_center], lr=0.1)

# Define a loss function (e.g., mean squared error between projected image and target image)
def loss_function(intrinsic_params, extrinsic_params, optical_center, target_image):
    # Project the point cloud using optimized parameters
    projected_image = project_point_cloud(point_cloud, intrinsic_params, extrinsic_params, optical_center, target_image.shape)
    cv2.imwrite('../data/projected_image.png', projected_image)
    
    # Convert projected_image and target_image to PyTorch tensors
    projected_image_tensor = torch.from_numpy(projected_image).permute(2, 0, 1).float()
    target_image_tensor = torch.from_numpy(target_image).permute(2, 0, 1).float()

    # Compute the mean squared error loss
    loss = torch.mean((projected_image_tensor - target_image_tensor)**2)
    
    return loss

# Optimization loop
max_iterations = 1000
for iteration in range(max_iterations):
    optimizer.zero_grad()  # Zero the gradients
    
    loss = loss_function(
        initial_intrinsic_params,
        initial_extrinsic_params,
        initial_optical_center,
        target_image
    )  # Compute the loss
    loss.requires_grad = True
    loss.backward()  # Compute gradients
    
    optimizer.step()  # Update parameters

    # Print loss for monitoring
    if iteration % 10 == 0:
        print(f'Iteration {iteration}: Loss = {loss.item()}')
        

# Extract optimized intrinsic, extrinsic parameters, and optical center
optimized_intrinsic_params = initial_intrinsic_params.detach().numpy()
optimized_extrinsic_params = initial_extrinsic_params.detach().numpy()
optimized_optical_center = initial_optical_center.detach().numpy()

# Use the optimized parameters for further processing
projected_image = project_point_cloud(point_cloud, optimized_intrinsic_params, optimized_extrinsic_params, optimized_optical_center, target_image.shape)

# Save the resulting image
cv2.imwrite('../data/projected_image.png', projected_image)
