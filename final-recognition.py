# from 01_perspective import *
from checkered import checkered_operations
from perspective import perspective_operations
from utils import get_image, save_image
from removeKartkens import removeLines
from tqdm import tqdm


def shoggoth(img_num):
    image = get_image(img_num)
    # Wykrycie narożników kartki, skorygowanie perspektywy oraz wycięcie kartki.
    image_perspective = perspective_operations(image)
    # Usunięcie kratek z kartki Tak, żeby zostały widoczne tylko słowa 
    image_checkered = removeLines(image_perspective)

    save_image(img_num, image_checkered)

    # Znajdowanie wyrazów 
    # Wykrycie pojedynczych cyfr
    # Rozpoznanie cyfr


# Etap 1:
# Nie działa dla:
# image_range = [7, 8, 11, 16, 17, 21, 22, 23, 26]
image_range = range(1, 30)

for image_num in tqdm(image_range):
    print('image num: {}'.format(image_num))
    shoggoth(image_num)
