import matplotlib
matplotlib.use('TkAgg')


import os
import sys
import random
import math
import re
import time
import numpy as np
import cv2
#import matplotlib
#import matplotlib.pyplot as plt

from actionCLSS_config import actionCLSS_Config
from actionCLSS_dataset import actionCLSS_Dataset
import utils
import config
import model as modellib
import visualize
from model import log
from PIL import Image

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0"

# Root directory of the project
ROOT_DIR = os.getcwd()

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

config = actionCLSS_Config()
config.display()

# training dataset
dataset_train = actionCLSS_Dataset()
dataset_train.load_dataset(20, config.IMAGE_SHAPE[0], config.IMAGE_SHAPE[1])
dataset_train.prepare()

# Validation dataset
dataset_val = actionCLSS_Dataset()
dataset_val.load_dataset(20, config.IMAGE_SHAPE[0], config.IMAGE_SHAPE[1])
dataset_val.prepare()

class InferenceConfig(actionCLSS_Config):
	GPU_COUNT = 1
	IMAGES_PER_GPU = 1

inference_config = InferenceConfig()

# Recreate the model in inference mode
model = modellib.MaskRCNN(mode="inference", 
                          config=inference_config,
                          model_dir=MODEL_DIR)

model_path = model.find_last()[1]
model.load_weights(model_path, by_name=True)
# Test on a random image
image_id = random.choice(dataset_val.image_ids)
original_image, image_meta, gt_class_id, gt_bbox, gt_mask =\
    modellib.load_image_gt(dataset_val, inference_config, 
                           image_id, use_mini_mask=False)
'''
log("original_image", original_image)
log("image_meta", image_meta)
log("gt_class_id", gt_class_id)
log("gt_bbox", gt_bbox)
log("gt_mask", gt_mask)

visualize.display_instances(original_image, gt_bbox, gt_mask, gt_class_id, 
                            dataset_train.class_names, figsize=(8, 8))
'''
#log("gt_bbox", gt_bbox)
#visualize.draw_box(original_image, gt_bbox, (0,0,0))
dataset_train.draw_box(original_image, gt_bbox, gt_class_id)
