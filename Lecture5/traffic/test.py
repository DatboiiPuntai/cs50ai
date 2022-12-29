import cv2
import numpy as np
import os
import sys
import tensorflow as tf

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))