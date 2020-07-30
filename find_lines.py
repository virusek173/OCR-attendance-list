from PIL import ImageOps
import imutils
from words import *
from digits import *
from removeKartkens import *
from checkered import *
from perspective import *
import cv2
import math
import numpy as np
import os
import matplotlib as plot
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
    # get rectangle bounding contour
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
                    # if color == 100:
                    #     color = 200
                    # else:
                    #     color = 100
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

    #fig, ax = plot.pyplot.subplots(figsize=(18, 20))
    #ax.imshow(test_image, cmap='gray')

    test_image = np.uint8(test_image)

    # find all your connected components (white blobs in your image)
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(
        test_image, connectivity=8)
    # connectedComponentswithStats yields every seperated component with information on each of them, such as size
    # the following part is just taking out the background which is also considered a component, but most of the time we don't want that.
    sizes = stats[1:, -1]
    nb_components = nb_components - 1

    # minimum size of particles we want to keep (number of pixels)
    # here, it's a fixed value, but you can set it as you want, eg the mean of the sizes or whatever
    min_size = 1700
    #print("sizes", sizes)
    # your answer image

    # print(nb_components)
    #fig, ax = plot.pyplot.subplots(figsize=(18, 20))
    #ax.imshow(output, cmap='gray')

    # for every component in the image, you keep it only if it's above min_size
    x = 0
    for i in range(0, nb_components):
        if sizes[i] < min_size:
            x += 1
            final_image[output == i + 1] = 255
    #print("x", x)

    final_image[final_image == 255] = 0
    return final_image


def apply_mask(image, mask):

    mask = prepare_mask(mask)
    mask = mask.astype(np.uint8)

    # print(mask.shape)

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

    # width, height = mask.shape

    # Przelicz do oryginalnego rozmiaru
    #tPoints = contours.dot(mask.shape[0] / 800)

    # Używając odległości euklidesowej oblicz max height
    height = max(np.linalg.norm(tPoints[0] - tPoints[1]),
                 np.linalg.norm(tPoints[2] - tPoints[3]))
    width = max(np.linalg.norm(tPoints[1] - tPoints[2]),
                np.linalg.norm(tPoints[3] - tPoints[0]))

    # sPoints = np.array([[0, 0],
    #                     [0, height],
    #                     [width, height],
    #                     [width, 0]], np.float32)

    # tPoints = np.array(contours, np.float32)

    # getPerspectiveTransform() potrzebuje float32
    if sPoints.dtype != np.float32:
        sPoints = sPoints.astype(np.float32)

    print("sPoints: ", sPoints)
    print("tPoints", tPoints)

    M = cv2.getPerspectiveTransform(sPoints, tPoints)
    mask = cv2.warpPerspective(mask, M, (int(width), int(height)))

    new_image = apply_mask(new_image, mask)

    return new_image
