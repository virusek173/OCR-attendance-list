# from 01_perspective import *
from checkered import checkered_operations
from perspective import perspective_operations
from words import detect_words_operations
from utils import get_image, save_image
from removeKartkens import removeLines
from digits import crop_numbers
from tqdm import tqdm


def shoggoth(img_num):
    image = get_image(img_num)
    # Wykrycie narożników kartki, skorygowanie perspektywy oraz wycięcie kartki.
    image_perspective = perspective_operations(image)
    # Usunięcie kratek z kartki Tak, żeby zostały widoczne tylko słowa 
    image_remove_lines = removeLines(image_perspective)
    image_checkered = checkered_operations(image_remove_lines)
    # Znajdowanie wyrazów 
    image_detect_words = detect_words_operations(image_checkered)
    # Wykrycie indeksów
    image_crop_numbers = crop_numbers(image_detect_words, image_perspective)

    save_image(img_num, image_crop_numbers)

    # Wykrycie pojedynczych cyfr
    # Rozpoznanie cyfr


image_range = range(1, 30)

for image_num in tqdm(image_range):
    print('image num: {}'.format(image_num))
    shoggoth(image_num)
