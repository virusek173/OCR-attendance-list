# from 01_perspective import *
from checkered import checkered_operations
from perspective import perspective_operations
from words import detect_words_operations
from utils import get_image, save_image
from removeKartkens import removeLines
from digits import crop_numbers, crop_digits
from predict_model import predict_image
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
    image_crop_numbers, cropped_numbers = crop_numbers(image_detect_words, image_perspective_operations)
    # Podział na cyfry
    image_crop_digits = crop_digits(cropped_numbers, image)

    return image_crop_digits


image_range = range(1,2)

# for image_num in tqdm(image_range):
#   print('image num: {}'.format(image_num))
#   shoggoth(image_num)

image_crop_digits = []
for image_num in image_range:
  print('image num: {}'.format(image_num))
  image_crop_digits.append(shoggoth(image_num))

index_array = []
image_crop_digits

for page_number, page in tqdm(enumerate(image_crop_digits)):
    index_array.append([])
    for index_number, image_number in enumerate(page):
        index_array[page_number].append('')
        for index_digit, image_digit in enumerate(image_number):
            # image_digit = (255-image_digit)
            predicted_digit = predict_image(image_digit)
            index_array[page_number][index_number] += str(predicted_digit)
    index_array[page_number].reverse()

# indexes_list = []
for image_num, page in enumerate(index_array):
    # image = get_image(image_range[image_num])
    # cv2_imshow(cv2.cvtColor(resize_image_height(image, 800), cv2.COLOR_BGR2RGB))
    print('page: {}'.format(page))
  # filtered_page = [x for x in page if len(x) > 2]
    # for key, index in enumerate(page):
        # print('{}. {}'.format(key, index))
