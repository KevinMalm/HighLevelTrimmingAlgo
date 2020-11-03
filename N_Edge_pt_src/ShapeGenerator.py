import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math as m
import random 
from skimage.draw import line, polygon, circle, ellipse

from Variables_and_Constants import N,M

edge_padding = 4
image_size = max(N, M)
min_object_size = 180
max_object_size = 400

min_grass_padding = 10
max_grass_padding = 60

def get_random_box():
    foreground = np.full([image_size, image_size], 1)
    background = np.full([image_size, image_size], 1)

    #random size
    w, h = np.random.randint(min_object_size, max_object_size, size = 2)
    #random anchor 
    x = np.random.randint(edge_padding, image_size - w - edge_padding)
    y = np.random.randint(edge_padding, image_size - h - edge_padding)
    #apply
    background[x:x+w, y:y+h] = -1 # define where item is 

    #add grass
    grass_width_a = np.random.randint(min_grass_padding, max_grass_padding)
    grass_width_b = np.random.randint(min_grass_padding, max_grass_padding)
    grass_width_c = np.random.randint(min_grass_padding, max_grass_padding)
    grass_width_d = np.random.randint(min_grass_padding, max_grass_padding)

    foreground[x+grass_width_a:x+w-grass_width_b, y+grass_width_c:y+h-grass_width_d] = 0

    return [foreground, background], x + int(w/2), y + int(h/2)

def draw_circle(v = 1, f = 1, r = None, x = None, y = None):

    canvas = np.full([image_size, image_size], f)
    if(r == None):
        r = int(0.5 * np.random.randint(min_object_size, max_object_size, size = 1)[0])
    #random anchor 
    if(x == None or y == None):
        x = np.random.randint(r + edge_padding, image_size - r - edge_padding)
        y = np.random.randint(r + edge_padding, image_size - r - edge_padding)
    rr, cc = circle(x, y, r, canvas.shape)
    canvas[rr,cc] = v

    return canvas, x, y, r




def get_jitter(v = [1, 10, 15]):
    blank = np.zeros([image_size, image_size])
    for x in range(image_size):
        for y in range(image_size):
            if(np.random.randint(0, 30) == 1):
                blank[x, y] = (np.random.randint(v[0], v[1]) / v[2])
    return blank

def add_figures(A, B):
    added = np.add(A, B)
    return added



def build_rect():
    img, x, y = get_random_box()
    jitter = get_jitter()

    img[0] = add_figures(img[0], jitter) # add noise to top layer 

    return img, x, y

def build_circle():
    background,x,y,r = draw_circle(v = -1, f = 1)

    foreground,r,_,_ = draw_circle(r = (r - np.random.randint(min_grass_padding, max_grass_padding)),v = 0, x = x, y = y)
    jitter = get_jitter()

    foreground = add_figures(foreground, jitter) # add noise to top layer 


    return [foreground, background], x, y