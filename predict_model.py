# make a prediction for a new image.
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform
import tensorflow as tf 
import keras
import cv2

test_model_path = './final_model.h5'

# load and prepare the image
def load_image(img):
  img = (255-img)
  offset = 10
  img = cv2.copyMakeBorder(img, offset, offset, offset, offset, cv2.BORDER_CONSTANT, value=0)
  img = cv2.resize(img, (28, 28)) 
  img = img.reshape(1, 28, 28, 1)
  img = img.astype('float32')
  img = img / 255.0

  return img
 
# load an image and predict the class
def predict_image(image):
  img = load_image(image)
  model = tf.keras.models.load_model(test_model_path)
  digit = model.predict_classes(img)

  return digit[0]


