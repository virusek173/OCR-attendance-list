import cv2
import os


def get_image(img_num, data_dir):
    image_path = './{}/img_{}.jpg'.format(data_dir, img_num)
    image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    image_to_show = image

    return image_to_show


def save_image(img_num, image, extension, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    image_path = './{}/img_{}.{}'.format(out_dir, img_num, extension)
    cv2.imwrite(image_path, image)
    print('Saved to {}'.format(image_path, ))
