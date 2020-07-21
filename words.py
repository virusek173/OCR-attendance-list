# Basic word position detection
import cv2
import math
import numpy as np

def detect_words_operations(image):
    kernel_ero = np.ones((3, 3), np.uint8) 
    treshold_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 40)
    blur_image = cv2.medianBlur(treshold_image, 5)
    input_image_to_morphological_transformations = blur_image
    erode_image = cv2.erode(input_image_to_morphological_transformations, kernel_ero, cv2.BORDER_REFLECT) 
    
    kernel_erode_hor = np.ones((20, 40), np.uint8) 
    erode_image_hor = cv2.erode(blur_image, kernel_erode_hor, iterations=1) 

    final_image = erode_image_hor

    return final_image