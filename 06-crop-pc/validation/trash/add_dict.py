import pickle

with open("circle_mask.txt", 'rb') as f:
    mask = pickle.load(f)

mask_with_dict = {"circle_mask": mask}

with open("circle_mask_dict.txt", "wb") as f:
    pickle.dump(mask_with_dict, f)