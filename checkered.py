import cv2
import math
import numpy as np

def checkered_operations(image):
  treshold_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 40)
  kernel_ero = np.ones((3, 3), np.uint8)
  erode_image = cv2.erode(treshold_image, kernel_ero, cv2.BORDER_REFLECT) 

  return erode_image