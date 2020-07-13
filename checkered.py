import cv2
import math
import numpy as np

def checkered_operations(image):
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  treshold_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 50)
  kernel_ero = np.ones((3, 3), np.uint8) 
  erode_image = cv2.erode(treshold_image, kernel_ero, cv2.BORDER_REFLECT) 

  return erode_image