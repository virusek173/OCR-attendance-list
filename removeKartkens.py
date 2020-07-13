import cv2
import math
import numpy as np
import os
from tqdm import tqdm
from utils import get_image, save_image
from scipy.signal import convolve2d
import cv2

data_dir = 'out'
out_dir = 'out2'


def eight_neighbor_average_convolve2d_horizontal(x):
    kernel = np.ones((3, 3))
    kernel[0, 1] = 0
    kernel[1, 1] = 0
    kernel[2, 1] = 0

    neighbor_sum = convolve2d(
        x, kernel, mode='same',
        boundary='fill', fillvalue=0)

    num_neighbor = convolve2d(
        np.ones(x.shape), kernel, mode='same',
        boundary='fill', fillvalue=0)

    return neighbor_sum / num_neighbor


def eight_neighbor_average_convolve2d_vertical(x):
    kernel = np.ones((3, 3))
    kernel[1, 0] = 0
    kernel[1, 1] = 0
    kernel[1, 2] = 0

    neighbor_sum = convolve2d(
        x, kernel, mode='same',
        boundary='fill', fillvalue=0)

    num_neighbor = convolve2d(
        np.ones(x.shape), kernel, mode='same',
        boundary='fill', fillvalue=0)

    return neighbor_sum / num_neighbor


def removeLines(image):

    image = np.array(image)
    croppedImage = image[:, int(len(image[0])/2):]
    image = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)

    image_swaped_colors = cv2.bitwise_not(image)

    bw = cv2.adaptiveThreshold(image_swaped_colors, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                               cv2.THRESH_BINARY, 15, -2)

    horizontal = np.copy(bw)
    vertical = np.copy(bw)

    cols = horizontal.shape[1]
    horizontal_size = cols // 30
    # Create structure element for extracting horizontal lines through morphology operations
    horizontalStructure = cv2.getStructuringElement(
        cv2.MORPH_RECT, (horizontal_size, 1))
    # Apply morphology operations
    horizontal = cv2.erode(horizontal, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)

    rows = vertical.shape[0]
    verticalsize = rows // 30
    # Create structure element for extracting vertical lines through morphology operations
    verticalStructure = cv2.getStructuringElement(
        cv2.MORPH_RECT, (1, verticalsize))
    # Apply morphology operations
    vertical = cv2.erode(vertical, verticalStructure)
    vertical = cv2.dilate(vertical, verticalStructure)

    verticalTrue = [vertical > 128]
    horizontalTrue = [horizontal > 128]

    x_hor = eight_neighbor_average_convolve2d_horizontal(image)
    x_ver = eight_neighbor_average_convolve2d_vertical(image)

    lineindex = 0
    for line, trueLine in zip(image, verticalTrue[0]):
        index = 0
        for pix, shouldChange in zip(line, trueLine):
            if shouldChange:
                image[lineindex, index] = x_hor[lineindex, index]

            index += 1
        lineindex += 1

    lineindex = 0
    for line, trueLine in zip(image, horizontalTrue[0]):
        index = 0
        for pix, shouldChange in zip(line, trueLine):
            if shouldChange:
                image[lineindex, index] = x_ver[lineindex, index]

            index += 1
        lineindex += 1

    return image


if __name__ == "__main__":

    for image_num in range(1, 29):

        image = get_image(image_num)
        # Plot
