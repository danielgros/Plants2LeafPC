import os
import sys
import random
import numpy as np
import tensorflow as tf
import pickle
import cv2

# Root directory of the project
ROOT_DIR = os.path.abspath("../../../../")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
from mrcnn import visualize
from mrcnn.visualize import display_images
import mrcnn.model as modellib
from mrcnn.model import log

import importlib

module_name = "samples.plants_to_leaf_area.03-model.src.leaves_model"
leaves_model_module = importlib.import_module(module_name)
leaves_model = leaves_model_module
# from samples.plants_to_leaf_area.03-model.src.leaves_model import leaves_model

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Path to Ballon trained weights
# You can download this file from the Releases page
# https://github.com/matterport/Mask_RCNN/releases
LEAVES_MODEL_WEIGHTS_PATH = os.path.join(
    ROOT_DIR, "logs/leaves_model20230918T1246"
)  # TODO: update this path


config = leaves_model.LeavesConfig()
LEAVES_MODEL_DIR = os.path.join(ROOT_DIR, "samples/plants_to_leaf_area/03-model/data")


# Override the training configurations with a few
# changes for inferencing.
class InferenceConfig(config.__class__):
    # Run detection on one image at a time
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


config = InferenceConfig()
config.display()


# Device to load the neural network on.
# Useful if you're training a model on the same
# machine, in which case use CPU and leave the
# GPU for training.
DEVICE = "/cpu:0"  # /cpu:0 or /gpu:0

# Inspect the model in training or inference modes
# values: 'inference' or 'training'
# TODO: code for 'training' test mode not ready yet
TEST_MODE = "inference"


# Load validation dataset
dataset = leaves_model.LeavesDataset()
dataset.load_leaves(LEAVES_MODEL_DIR, "val")

# Must call before using the dataset
dataset.prepare()

print("Images: {}\nClasses: {}".format(len(dataset.image_ids), dataset.class_names))


# Create model in inference mode
with tf.device(DEVICE):
    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)


# Set path to leaves_model weights file
# weights_path = LEAVES_MODEL_WEIGHTS_PATH

# Or, load the last model you trained
weights_path = model.find_last()

# Load weights
print("Loading weights ", weights_path)
model.load_weights(weights_path, by_name=True)

# image_id = random.choice(dataset.image_ids)
image_ids = [1, 2, 6, 10]
for image_id in image_ids:
    image, image_meta, gt_class_id, gt_bbox, gt_mask = modellib.load_image_gt(
        dataset, config, image_id, use_mini_mask=False
    )
    info = dataset.image_info[image_id]
    print(
        "image ID: {}.{} ({}) {}".format(
            info["source"], info["id"], image_id, dataset.image_reference(image_id)
        )
    )

    imageName = info["id"]

    # Run object detection
    results = model.detect([image], verbose=1)

    r = results[0]
    rawMasks = r["masks"]
    print(type(rawMasks))
    print(rawMasks.shape)

    # define
    masks = {}
    numMasks = len(rawMasks[0][0])
    for i in range(0, numMasks):
        key = "mask_" + imageName + "_num_" + str(i)
        masks[key] = []

    listKeys = list(masks.keys())
    print(listKeys)
    print(masks)

    # populate
    for rowIndex, rowValue in enumerate(rawMasks):
        for key in listKeys:
            masks[key].append([])
        for columnIndex, columnValue in enumerate(rowValue):
            for key in listKeys:
                masks[key][rowIndex].append([])
            for numMask, maskValue in enumerate(columnValue):
                key = "mask_" + imageName + "_num_" + str(numMask)
                masks[key][rowIndex][columnIndex].append(maskValue)

    # resize mask
    height_mask, width_mask, _ = r["masks"].shape

    display_instances_rois = np.zeros((1, 4))
    display_instances_masks = np.zeros((height_mask, width_mask, 1))
    display_instances_class_ids = np.zeros((1))
    display_instances_class_names = dataset.class_names

    visualize.display_instances(
        image,
        display_instances_rois,
        display_instances_masks,
        display_instances_class_ids,
        display_instances_class_names,
    )

    # Save or display the image not cropped
    cv2.imwrite("../data/processed/resized_image_" + info["id"][:-4] + ".jpg", image)

    # CROP IMAGE

    # Convert the image to grayscale for easier processing
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Define a threshold to separate black bars from the content
    threshold = 20

    # Find the coordinates of the top and bottom black bars
    top_black_bar = np.argmax(np.sum(gray_image <= threshold, axis=1) < 1024)
    print("top_black_bar", top_black_bar)
    bottom_black_bar = gray_image.shape[0] - np.argmax(
        np.sum(gray_image[::-1] <= threshold, axis=1) < 1024)
    print("bottom_black_bar", bottom_black_bar)

    # Crop the image to remove the black bars
    cropped_image = image[top_black_bar:bottom_black_bar, :]

    # crop masks
    for mask_key in listKeys:
        print(mask_key)
        print(np.array(masks[mask_key]).shape)
        masks[mask_key] = masks[mask_key][top_black_bar:bottom_black_bar]
        print(np.array(masks[mask_key]).shape)


    # Save or display the cropped image for validation
    cv2.imwrite(
        "../data/processed/cropped_image_" + info["id"][:-4] + ".jpg", cropped_image
    )

    # output
    output_path = "../data/processed/masks_" + info["id"][:-4] + ".txt"
    with open(output_path, "wb") as f:
        pickle.dump(masks, f)
