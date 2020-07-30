# from 01_perspective import *
import tensorflow as tf 

from checkered import checkered_operations
from perspective import perspective_operations
from words import detect_words_operations
from utils import get_image, save_image, save_txt
from removeKartkens import removeLines
from digits import crop_numbers, crop_digits
from predict_model import predict_image
from tqdm import tqdm
from find_lines import crop_small_rectangles, paint_lines, prepare_mask, move_to_original_coords
from keras.models import load_model

local_in_dir = 'data'
local_out_dir = 'out'
local_image_range = range(1,2)
pretict_model_path = './final_model.h5'

def all_operations(in_dir, image_range, out_dir):
    def shoggoth(img_num):
        image = get_image(img_num, in_dir)
        # Wykrycie narożników kartki, skorygowanie perspektywy oraz wycięcie kartki.
        image_perspective_operations, sPoints, tPoints = perspective_operations(image)
        # Usunięcie kratek z kartki tak, żeby zostały widoczne tylko słowa 
        image_remove_lines_operations = removeLines(image_perspective_operations)
        image_checkered_operations = checkered_operations(image_remove_lines_operations)
        # Wykrycie słów
        image_detect_words = detect_words_operations(image_checkered_operations)
        # Wykrycie indeksów
        image_crop_numbers, cropped_numbers = crop_numbers(image_detect_words, image_perspective_operations)
        # Podział na cyfry
        image_crop_digits = crop_digits(cropped_numbers, image)

        cropped_rectangles = crop_small_rectangles(image_detect_words)
        mask = paint_lines(cropped_rectangles)
        mask = prepare_mask(mask)
        new_img = move_to_original_coords(mask, sPoints, tPoints, image.shape[:2])
        save_image(img_num, new_img, "png", out_dir)

        return image_crop_digits



    image_crop_digits = []
    for image_num in tqdm(image_range):
        image_crop_digits.append(shoggoth(image_num))

    index_array = []
    model = tf.keras.models.load_model(pretict_model_path)

    for page_number, page in tqdm(enumerate(image_crop_digits)):
        index_array.append([])
        for index_number, image_number in enumerate(page):
            index_array[page_number].append('')
            for index_digit, image_digit in enumerate(image_number):
                predicted_digit = predict_image(image_digit, model)
                index_array[page_number][index_number] += str(predicted_digit)
        index_array[page_number].reverse()

    for image_num, page in enumerate(index_array):
        save_txt((image_num + 1), page, out_dir)
        print('page: {}'.format(page))

# all_operations(local_in_dir, local_image_range, local_out_dir)
