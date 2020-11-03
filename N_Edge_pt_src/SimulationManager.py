import matplotlib.pyplot as plt
import numpy as np
import math
from VectorClass import Vector2, PT_ZERO
import time
from ShapeGenerator import build_circle, build_rect
from Variables_and_Constants import get_brush, N,M



class SimulationManager:

    trimmer_brush = []
    trimmer_center = PT_ZERO

    img = None
    img_center = PT_ZERO

    trimmed_img = None

    def __init__(self, build_fn = build_rect):
        #build brush shape 
        self.trimmer_brush, self.trimmer_center  = get_brush(25)
        #build image with x,y center 
        self.img, x, y = build_fn()
        self.img_center = Vector2(x,y)
        #copy image to compare trimmed / original 
        self.trimmed_img = np.copy(self.img)

    #apply trim to X,Y point 
    def trim(self, pt: Vector2):
        starting_pt = pt.copy().Subtract(self.trimmer_center)
        img_range_low_x, image_range_low_y = starting_pt.x if starting_pt.x >= 0 else 0, starting_pt.y if starting_pt.y >= 0 else 0
        img_range_high_x, image_range_high_y = starting_pt.x + self.trimmer_brush.shape[0] if starting_pt.x + self.trimmer_brush.shape[0] < N else N -1, starting_pt.y + self.trimmer_brush.shape[1] if starting_pt.y + self.trimmer_brush.shape[1] < M else M - 1

        brush_range_low_x, brush_range_low_y = 0 if starting_pt.x >= 0 else abs(starting_pt.x), 0 if starting_pt.y >= 0 else abs(starting_pt.y)
        brush_range_high_x, brush_range_high_y = self.trimmer_brush.shape[0] if starting_pt.x + self.trimmer_brush.shape[0] < N else N - starting_pt.x -1, self.trimmer_brush.shape[1] if starting_pt.y + self.trimmer_brush.shape[1] < M else  M - starting_pt.y-1


        self.trimmed_img[0,img_range_low_x:img_range_high_x,image_range_low_y:image_range_high_y] = np.add(self.trimmed_img[0,img_range_low_x:img_range_high_x,image_range_low_y:image_range_high_y], self.trimmer_brush[brush_range_low_x:brush_range_high_x, brush_range_low_y:brush_range_high_y])
        self.trimmed_img[0] = np.clip(self.trimmed_img[0], 0, 5)
        return

    def display_trimmed_img(self):
        plt.figure()
        plt.imshow(np.add(self.trimmed_img[0], self.trimmed_img[1]))

    def display_original_img(self):
        plt.figure()
        plt.imshow(np.add(self.img[0], self.img[1]))

    def get_center(self, j = 12):
        return Vector2(self.img_center.x + np.random.randint(-1 * j, j), self.img_center.y + np.random.randint(-1 * j, j))

    def read_at_pt(self, pt):
        if(self.trimmed_img[0, pt.x, pt.y] == 0):
            return self.trimmed_img[1, pt.x, pt.y]
        return self.trimmed_img[0, pt.x, pt.y]


h =  SimulationManager(build_fn=build_rect)
