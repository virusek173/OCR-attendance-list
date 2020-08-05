import cv2
import math
import os
import numpy as np

from words import *
from digits import *
from removeKartkens import *
from checkered import *
from perspective import *
from tqdm import tqdm


import sys


def crop_small_rectangles(image):

    bordersize = 1
    image = cv2.copyMakeBorder(
        image,
        top=bordersize,
        bottom=bordersize,
        left=bordersize,
        right=bordersize,
        borderType=cv2.BORDER_CONSTANT,
        value=[255]
    )

    image_final = image

    contours, im2 = cv2.findContours(
        image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    bounding_array = [cv2.boundingRect(contour) for contour in contours]
    np_bounding_array = np.array(bounding_array)
    center_of_gravity = np_bounding_array[:, 0].mean()

    rect_areas = []

    for bounding in np_bounding_array:
        [x, y, w, h] = bounding
        if (w >= 800 or h >= 400) or (w < 90 or h < 20) or x < center_of_gravity - 25:
            continue
        else:
            rect_areas.append(w * h)

    avg_area = np.mean(rect_areas)

    t = int(bordersize / 2) + 1
    for bounding in np_bounding_array:
        [x, y, w, h] = bounding

        cnt_area = w * h
        if cnt_area < 0.2 * avg_area:
            image_final[y:y + h, x:x + w] = 255

    return image_final


def paint_lines(image):

    black_counts = []

    final_image = np.zeros(image.shape)
    final_image[final_image == 0] = 255

    for index, line in enumerate(image):
        # Line has black color somewhere
        if np.mean(line) != 255:
            black_counts.append((index, np.mean(line)))

    values = [count for _, count in black_counts]

    mean_black_color = np.mean(values)

    color = 1

    old_line = None

    minLineThiccness = 40

    currentLineThiccness = 0
    lines = []

    for line, value in black_counts:

        if value < mean_black_color * 1.2:
            # black line
            if old_line == None or old_line == line - 1:
                currentLineThiccness += 1
                lines.append(line)
            else:
                if len(lines) > minLineThiccness:
                    for l in lines:
                        for index, pixel in enumerate(image[l]):
                            if pixel == 0:
                                final_image[l, index] = color

                    color += 1
                currentLineThiccness = 0
                lines = []

            old_line = line
        else:
            # white line
            pass

    if len(lines) > minLineThiccness:
        for l in lines:
            for index, pixel in enumerate(image[l]):
                if pixel == 0:
                    final_image[l, index] = color

    test_image = np.zeros(final_image.shape)

    test_image[final_image < 255] = 255

    test_image = np.uint8(test_image)

    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(
        test_image, connectivity=8)
    sizes = stats[1:, -1]
    nb_components = nb_components - 1

    min_size = 1700
    x = 0
    for i in range(0, nb_components):
        if sizes[i] < min_size:
            x += 1
            final_image[output == i + 1] = 255
    final_image[final_image == 255] = 0
    return final_image


def apply_mask(image, mask):
    mask = mask.astype(np.uint8)

    for line_index, mask_line in enumerate(mask):
        for index, mask_element in enumerate(mask_line):
            if(mask_element != 0):
                image[line_index, index] = mask_element

    return image


def prepare_mask(mask):
    mask = np.delete(mask, 0, 0)  # delete first row of mask
    mask = np.delete(mask, len(mask) - 1, 0)  # delete last row of mask

    mask = np.delete(mask, 0, 1)  # delete first column of mask
    mask = np.delete(mask, len(mask[0]) - 1, 1)  # delete last column of mask

    return mask


def move_to_original_coords(mask, tPoints, sPoints, original_size):
    new_image = np.zeros(original_size)

    height = max(np.linalg.norm(tPoints[0] - tPoints[1]),
                 np.linalg.norm(tPoints[2] - tPoints[3]))
    width = max(np.linalg.norm(tPoints[1] - tPoints[2]),
                np.linalg.norm(tPoints[3] - tPoints[0]))

    if sPoints.dtype != np.float32:
        sPoints = sPoints.astype(np.float32)

    M = cv2.getPerspectiveTransform(sPoints, tPoints)
    mask = cv2.warpPerspective(mask, M, (int(width), int(height)))

    new_image = apply_mask(new_image, mask)

    return new_image
