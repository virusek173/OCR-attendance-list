import cv2
import numpy as np

def crop_numbers(image, oryg_image):
    final_cropped_numbers = []
    image_to_crop = oryg_image
    image_final = oryg_image
    contours, im2  = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # get rectangle bounding contour
    bounding_array = [cv2.boundingRect(contour) for contour in contours]
    np_bounding_array = np.array(bounding_array)
    center_of_gravity = np_bounding_array[:, 0].mean()
    for bounding in np_bounding_array:
        [x, y, w, h] = bounding
        add_rectangle = True

        # Don't plot small and huge false positives that aren't text.
        if (w >= 800 or h >= 400) or (w < 90 or h < 20 ) or x < center_of_gravity - 25:
            continue

        for find_bounding in np_bounding_array:
          [fx, fy, fw, fh] = find_bounding
          if (fw >= 800 or fh >= 400) or (fw < 90 or fh < 20 ):
            continue

          if ((y - 50 < fy and y + 50 > fy) and fx > x):
            add_rectangle = False
            break

        # draw rectangle around contour on original image
        if (add_rectangle):
          image_final = cv2.rectangle(oryg_image, (x, y), (x + w, y + h), (255, 0, 255), 2)
        else:
          continue

        cropped_number = image_to_crop[y :y +  h , x : x + w]
        final_cropped_numbers.append(cropped_number)


    return image_final, final_cropped_numbers

def crop_digits(cropped_numbers):
  final_cropped_digits = []

  for index, number_image in enumerate(cropped_numbers):
    final_cropped_digits.append([])
    contours, _  = cv2.findContours(number_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x_array = np.array([])

    for contour in contours:
      [x, y, w, h] = cv2.boundingRect(contour)
      if (w >= 100) or (w < 10 or h < 23 ):
        continue
      # print('[x, y, w, h]: {}'.format([x, y, w, h]))
      x_array = np.append(x_array, x)

      digit_image = number_image[y :y +  h , x : x + w]
      # temp_array_digits = np.append(temp_array_digits, number_image)
      final_cropped_digits[index].append(digit_image)

    # Sort digits based on x coordinate
    x_max_indexes = np.argsort(x_array)
    final_cropped_digits[index] = [final_cropped_digits[index][i] for i in x_max_indexes]

    # Temp sol. adding number to 0 index
    final_cropped_digits[index].insert(0, number_image)

  return final_cropped_digits
