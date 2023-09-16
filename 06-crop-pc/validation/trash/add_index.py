import pickle
import numpy as np

with open("circle_mask.txt", 'rb') as f:
    mask = pickle.load(f)

mask_with_index = []

for x in range(0, len(mask)):
    mask_with_index.append([])
    for y in range(0, len(mask[x])):
        mask_with_index[x].append([mask[x][y]])

print(len(mask))
print(len(mask[0]))

print(len(mask_with_index))
print(len(mask_with_index[0]))
print(len(mask_with_index[0][0]))


print(np.array(mask_with_index).shape)

mask_with_dict = {"circle_mask": mask_with_index}


with open("circle_mask_dict.txt", "wb") as f:
    pickle.dump(mask_with_dict, f)