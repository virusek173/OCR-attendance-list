from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform
import keras
import cv2

def load_image(image):
  image = (255-image)
  border_size = 10
  image = cv2.copyMakeBorder(image, border_size, border_size, border_size, border_size, cv2.BORDER_CONSTANT, value=0)
  image = cv2.resize(image, (28, 28)) 
  image = image.reshape(1, 28, 28, 1)
  image = image.astype('float32')
  image = image / 255.0

  return image
 
def predict_image(image, model):
  image = load_image(image)
  digit = model.predict_classes(image)

  return digit[0]


