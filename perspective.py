import cv2
import math
import numpy as np
import os

from tqdm import tqdm

data_dir = 'data'
out_dir = 'out'

def resize_image_ratio(image, ratio=0.3):
    old_hight, old_width = image.shape
    new_hight = math.floor(old_hight*ratio)
    new_width = math.floor(old_width*ratio)
    new_shape = (new_width, new_hight)
    image_to_show = cv2.resize(image, new_shape)

    return image_to_show

def resize_image_height(img, height=800):
    """ Resize image to given height """
    rat = height / img.shape[0]
    return cv2.resize(img, (int(rat * img.shape[1]), height))

def fourCornersSort(pts):
    """ Sort corners: top-left, bot-left, bot-right, top-right """

    # Używamy diff i sum z wartości x i y, aby określić kolejność wierzchołków
    diff = np.diff(pts, axis=1)
    summ = pts.sum(axis=1)
    
    return np.array([pts[np.argmin(summ)],  # Top-left ma min
                     pts[np.argmax(diff)],  # Top-right ma max diff
                     pts[np.argmax(summ)],  # Bot-right ma max sumę
                     pts[np.argmin(diff)]]) # Top-left ma min diff

def contourOffset(cnt, offset):
    """ Offset contour, by 5px border """
    # Matrix addition
    cnt += offset
    
    # if value < 0 => replace it by 0
    cnt[cnt < 0] = 0
    return cnt

def get_image(img_num):
    image_path = './{}/img_{}.jpg'.format(data_dir, img_num)
    image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    image_to_show = image

    return image_to_show

def save_image(img_num, image):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    image_path = './{}/img_{}.jpg'.format(out_dir, img_num)
    cv2.imwrite(image_path, image) 
    print('Saved to {}'.format(image_path))

def get_paper_edges(image):
  # Zmiana rozmiaru i przekonwertowanie do skali szarości.
  img = cv2.cvtColor(resize_image_height(image), cv2.COLOR_BGR2GRAY)
  # Bilateral filter do rozmazania obrazka - pozbycie się szumu.
  img = cv2.bilateralFilter(img, 9, 45, 45)
  # Stworzenie czarnobiałego obrazka na podstawie tresholdu.
  img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 4)
  # Median filter czyści jeśli nie są w grupie.
  img = cv2.medianBlur(img, 11)
  # Dodaje czarną ramkę 5x5, gdy kartka dotyka krawędzi zdjęcia.
  img = cv2.copyMakeBorder(img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=[0, 0, 0])
  # Canny filter - Wykrycie krawędzi.
  edges = cv2.Canny(img, 200, 250)

  return edges

def get_contour(edges):
      # Pobranie konturów na obrazku
  contours, im2  = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  # Znajdowanie konturu największego prostokąta.
  # W przeciwnym razie zwróć kontury oryginalnego obrazka nie zapominając o ramce 5x5.
  height = edges.shape[0]
  width = edges.shape[1]
  MAX_COUNTOUR_AREA = (width - 10) * (height - 10)

  # Jeśli prostokąt jest większy niż połowa obrazka to weź pod uwagę.
  maxAreaFound = MAX_COUNTOUR_AREA * 0.5

  # Początkowy kontur kartki
  pageContour = np.array([[[5, 5]], [[5, height-5]], [[width-5, height-5]], [[width-5, 5]]])

  # Iterowanie po konturach
  for cnt in contours:
      # Upraszczanie konturów
      perimeter = cv2.arcLength(cnt, True)
      approx = cv2.approxPolyDP(cnt, 0.03 * perimeter, True)
      
      # Jeśli strona ma 4 narożników i jest wypukła oraz jest większa niż maxAreaFound
      if (len(approx) == 4 and cv2.isContourConvex(approx) and maxAreaFound < cv2.contourArea(approx) < MAX_COUNTOUR_AREA):
          maxAreaFound = cv2.contourArea(approx)
          pageContour = approx

  return pageContour

def get_image_after_perspective_correction(pageContour, image):
      # Wycięcie kartki po preprocessingu

  pageContour = fourCornersSort(pageContour[:, 0])
  pageContour = contourOffset(pageContour, (-5, -5))

  # Przelicz do oryginalnego rozmiaru
  sPoints = pageContour.dot(image.shape[0] / 800)
    
  # Używając odległości euklidesowej oblicz max height
  height = max(np.linalg.norm(sPoints[0] - sPoints[1]),
              np.linalg.norm(sPoints[2] - sPoints[3]))
  width = max(np.linalg.norm(sPoints[1] - sPoints[2]),
              np.linalg.norm(sPoints[3] - sPoints[0]))

  # Docelowe punkty
  tPoints = np.array([[0, 0],
                      [0, height],
                      [width, height],
                      [width, 0]], np.float32)

  # getPerspectiveTransform() potrzebuje float32
  if sPoints.dtype != np.float32:
      sPoints = sPoints.astype(np.float32)

  # Zmiana perspektywy
  M = cv2.getPerspectiveTransform(sPoints, tPoints)
  newImage = cv2.warpPerspective(image, M, (int(width), int(height)))

  return newImage  

def perspective_operations(image):
    edges = get_paper_edges(image)
    contour = get_contour(edges)
    final_image = get_image_after_perspective_correction(contour, image)

    return final_image
