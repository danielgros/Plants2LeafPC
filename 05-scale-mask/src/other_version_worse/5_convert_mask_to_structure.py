import cv2
import numpy as np

def convert_mask_to_structure(mask):
    mask = mask.astype(np.uint8) * 255  # Convert boolean mask to binary image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(contours)

    mask_structure = []
    for contour in contours:
        points = contour.squeeze().astype(np.float32)  # Ensure points are float32
        mask_structure.append(points)

    return mask_structure

def check_float_in_mask(mask_structure, point):
    for structure in mask_structure:
        if cv2.pointPolygonTest(structure, point, False) >= 0:
            return True
    return False

# Example usage
mask = np.array([
    [False, False, True, False, False],
    [False, True, True, True, False],
    [False, False, True, True, False],
    [False, False, False, True, True],
    [False, False, False, False, False]
])

mask_structure = convert_mask_to_structure(mask)

print(mask_structure)

print(check_float_in_mask(mask_structure, (2.5, 2.5)))  # Check if (2.5, 2.5) is within the mask
print(check_float_in_mask(mask_structure, (0.2, 1.8)))  # Check if (0.2, 1.8) is within the mask



print(check_float_in_mask(mask_structure, (2.5, 2.5)))  # Check if (2.5, 2.5) is within the mask
print(check_float_in_mask(mask_structure, (0.2, 1.8)))  # Check if (0.2, 1.8) is within the mask
print(check_float_in_mask(mask_structure, (0.2, 0.2)))  # Check if (2.5, 2.5) is within the mask
print(check_float_in_mask(mask_structure, (4.5, 2.9)))  # Check if (0.2, 1.8) is within the mask
print(check_float_in_mask(mask_structure, (4.5, 2.1)))  # Check if (0.2, 1.8) is within the mask
print(check_float_in_mask(mask_structure, (4.5, 1.9)))  # Check if (0.2, 1.8) is within the mask
print(check_float_in_mask(mask_structure, (4.5, 3.5)))  # Check if (0.2, 1.8) is within the mask

