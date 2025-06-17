import cv2
import numpy as np
import os

IMG_DIR = os.path.join(os.path.dirname(__file__), 'img')

def load_template(name):
    path = os.path.join(IMG_DIR, name)
    img = cv2.imread(path, 0)
    if img is None:
        print(f'[警告] テンプレート画像の読み込みに失敗: {path}')
    return img

def find_image_on_screen(template, img_gray, threshold=0.9):
    if template is None or img_gray is None:
        return None
    if not isinstance(img_gray, np.ndarray) or not isinstance(template, np.ndarray):
        return None
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val >= threshold:
        h, w = template.shape
        center = (max_loc[0] + w // 2, max_loc[1] + h // 2)
        return center
    return None
