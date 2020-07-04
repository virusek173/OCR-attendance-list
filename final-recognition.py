# from 01_perspective import *
from perspective import *
from tqdm import tqdm

def shoggoth(img_num):
    image = get_image(img_num)
    # Wykrycie narożników kartki, skorygowanie perspektywy oraz wycięcie kartki.
    image_after_perspective_operations = perspective_operations(image)

    image_to_compare_01 = resize_image_height(image, 600)
    image_to_compare_02 = resize_image_height(image_after_perspective_operations, 600)

    numpy_horizontal_concat = np.concatenate((image_to_compare_01, image_to_compare_02), axis=1)
    save_image(img_num, numpy_horizontal_concat)


    # Usunięcie kratek z kartki Tak, żeby zostały widoczne tylko słowa 
    # Znajdowanie wierszy 
    # Znajdowanie wyrazów 
    # Wykrycie pojedynczych cyfr
    # Rozpoznanie cyfr

# Etap 1:
# Nie działa dla:
# image_range = [7, 8, 11, 16, 17, 21, 22, 23, 26] 
image_range = range(1,30)

for image_num in tqdm(image_range):
    print('image num: {}'.format(image_num))
    shoggoth(image_num)
    