import cv2
import numpy as np

def crop_numbers(image, image_perspective):
    image_to_crop = image_perspective
    image_final = image_perspective
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
            # print('[x, y]: {}'.format([x, y]))
            # print('[fx, fy]: {}'.format([fx, fy]))

            add_rectangle = False
            break

        # draw rectangle around contour on original image
        if (add_rectangle):
          image_final = cv2.rectangle(image_perspective, (x, y), (x + w, y + h), (255, 0, 255), 2)
        else:
          continue

        #you can crop image and send to OCR  , false detected will return no text :)

        # cropped_number = image_to_crop[y :y +  h , x : x + w]
        # s = file_name + '/crop_' + str(index) + '.jpg' 
        # cv2.imwrite(s , cropped)
        # index = index + 1

        # cv2_imshow(cropped_number)

    return image_final