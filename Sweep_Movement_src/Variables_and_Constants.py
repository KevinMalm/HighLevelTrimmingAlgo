import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from VectorClass import Vector2
from skimage.draw import line, polygon, circle, ellipse

N = 512
M = 512

def get_brush(r = 6):
    img = np.zeros([(r*2) + 1, (r*2) + 1])
    x = r
    y = r 
    rr, cc = circle(x, y, r, img.shape)
    img[rr,cc] = -1

    return img, Vector2(x, y)