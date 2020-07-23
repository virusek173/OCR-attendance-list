# from 01_perspective import *
from checkered import checkered_operations
from perspective import perspective_operations
from words import detect_words_operations
from utils import get_image, save_image
from removeKartkens import removeLines
from digits import crop_numbers, crop_digits
from tqdm import tqdm

def shoggoth(img_num):
    image = get_image(img_num)
    # Wykrycie narożników kartki, skorygowanie perspektywy oraz wycięcie kartki.
    image_perspective_operations = perspective_operations(image)
    # Usunięcie kratek z kartki tak, żeby zostały widoczne tylko słowa 
    image_remove_lines_operations = removeLines(image_perspective_operations)
    image_checkered_operations = checkered_operations(image_remove_lines_operations)
    # Wykrycie słów
    image_detect_words = detect_words_operations(image_checkered_operations)
    # Wykrycie indeksów
    image_crop_numbers, cropped_numbers = crop_numbers(image_detect_words, image_checkered_operations)
    # Podział na cyfry
    image_crop_digits = crop_digits(cropped_numbers)

    for index_number, image_number in enumerate(image_crop_digits):
        print('image_number index: {}'.format(index_number))
        for index_digit, image_digit in enumerate(image_number):
            save_image('{}_{}_{}'.format(img_num, index_number, index_digit), image_digit)


image_range = range(1,2)

for image_num in image_range:
  print('image num: {}'.format(image_num))
  shoggoth(image_num)
