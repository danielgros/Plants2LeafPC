import os
import json

INPUT_DIR = os.path.abspath("../data")
OUTPUT_DIR = os.path.abspath("../../04-model/data")

# OLD FILES
ANNOT_TRAIN_DIR = os.path.join(INPUT_DIR, "annots/train")
ANNOT_VAL_DIR = os.path.join(INPUT_DIR, "annots/val")
ANNOT_TRAIN_FILES = os.listdir(ANNOT_TRAIN_DIR)
ANNOT_VAL_FILES = os.listdir(ANNOT_VAL_DIR)

# NEW FILES
TRAIN_DIR = os.path.join(OUTPUT_DIR, "train")
VAL_DIR = os.path.join(OUTPUT_DIR, "val")
TRAIN_DATA_FILE_DIR = os.path.join(TRAIN_DIR, "via_region_data.json")
VAL_DATA_FILE_DIR = os.path.join(VAL_DIR, "via_region_data.json")


# POPULATE TRAIN VIA REGION DATA FILE
train_data_dict = {}

for file_name in ANNOT_TRAIN_FILES:
    file = open(ANNOT_TRAIN_DIR + "/" + file_name, "r")
    file_contents = json.load(file)
    file.close()
    train_data_dict.update(file_contents["_via_img_metadata"])

if os.path.exists(TRAIN_DATA_FILE_DIR):
    os.remove(TRAIN_DATA_FILE_DIR)
train_data_file = open(TRAIN_DATA_FILE_DIR, "a")
json.dump(train_data_dict, train_data_file)
train_data_file.close()





# POPULATE VAL VIA REGION DATA FILE
val_data_dict = {}

for file_name in ANNOT_VAL_FILES:
    file = open(ANNOT_VAL_DIR + "/" + file_name, "r")
    file_contents = json.load(file)
    file.close()
    val_data_dict.update(file_contents["_via_img_metadata"])

if os.path.exists(VAL_DATA_FILE_DIR):
    os.remove(VAL_DATA_FILE_DIR)
val_data_file = open(VAL_DATA_FILE_DIR, "a")
json.dump(val_data_dict, val_data_file)
val_data_file.close()
