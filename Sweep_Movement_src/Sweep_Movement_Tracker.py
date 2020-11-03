import matplotlib.pyplot as plt
import numpy as np
import math
from VectorClass import Vector2, PT_ZERO
import time
from SimulationManager import SimulationManager
from ShapeGenerator import build_circle, build_rect
from Variables_and_Constants import get_brush, N,M

CIRCLE = False


#constants
RIGHT = Vector2(0,-1)
LEFT = Vector2(0,1)
UP = Vector2(1,0)
DOWN = Vector2(-1,0)
ABS = -1
GRASS = 1

STEPS = 5

class Sweep_Tracker:

    simulation_class: SimulationManager
    assumed_center: Vector2
    current_trimmer_pos: Vector2
    trimmer_moves = []
    edge_pts = []

    last_read_value = ABS


    def __init__(self, circle = True):
        self.simulation_class = SimulationManager(build_fn=build_circle if circle else build_rect)
        self.assumed_center = self.simulation_class.get_center()
        #set trimmer head in center
        self.current_trimmer_pos = self.assumed_center.copy()
        self.LOG_MOVE()
        self.edge_pts = []
        self.trimmer_moves = []

    #draws a line of from center -> to dir edge -> dir.REVERSE() edge
    #this function implements the step and check sensor method 
    def MOVE_TO_EDGE(self, direction: Vector2, y = True):
        h, l = 0, 0
        current_move = direction

        #set sensor to ABS
        self.update_sensor()
        valid_move = True

        #move until we hit abs
        while(self.last_read_value != ABS and valid_move):
            for _ in range(STEPS):
                if(self.able_to_move(current_move)):
                    self.current_trimmer_pos.Add(current_move)
                else:
                    valid_move = False
            if(valid_move):
                self.LOG_MOVE()
                self.update_sensor()
        
        #move in dir
        self.last_read_value = ABS
        self.valid_move = True
        while(self.last_read_value != GRASS and valid_move):
            for _ in range(STEPS):
                if(self.able_to_move(current_move)):
                    self.current_trimmer_pos.Add(current_move)
                else:
                    valid_move = False
            if(valid_move):
                self.LOG_MOVE()
                self.update_sensor()
        ta = self.current_trimmer_pos.y if y else self.current_trimmer_pos.x

        #reset valid move and sensor - then go to other side
        current_move = direction.REVERSE()

        #set sensor to ABS
        self.last_read_value = ABS
        valid_move = True

        while(self.last_read_value != GRASS and valid_move):
            for _ in range(STEPS):
                if(self.able_to_move(current_move)):
                    self.current_trimmer_pos.Add(current_move)
                else:
                    valid_move = False
            if(valid_move):
                self.LOG_MOVE()
                self.update_sensor()

        tb = self.current_trimmer_pos.y if y else self.current_trimmer_pos.x
        #get bounds
        h = max(ta, tb)
        l = min(ta, tb)
        return tb, ta

    def RUN(self):
        #find first edge
        l, h = self.MOVE_TO_EDGE(UP, y = False)
        #lets assume we're starting the lower bounds
        self.current_trimmer_pos.x = l

        while(self.current_trimmer_pos.x + STEPS < h):
            #move down
            self.current_trimmer_pos.Add(Vector2(UP.x * STEPS, UP.y * STEPS))
            self.LOG_MOVE()
            #sweep 
            self.MOVE_TO_EDGE(RIGHT)



    
    def LOG_MOVE(self):
        #save move
        self.trimmer_moves.append(self.current_trimmer_pos.copy())
        #trim
        self.simulation_class.trim(self.current_trimmer_pos)

    def update_sensor(self):
        self.last_read_value = self.simulation_class.read_at_pt(pt = self.current_trimmer_pos)
        return

    def able_to_move(self, pt):
        possible_move = self.current_trimmer_pos.copy().Add(pt)
        if(possible_move.x < 0 or possible_move.x >= N or possible_move.y < 0 or possible_move.y >= M):
            return False
        return True
    
    def plot_path(self):
        img_seq = np.zeros([N, M])
        pt_x, pt_y = [], []
        i = 1
        for pt in self.trimmer_moves:
            pt_x.append(pt.x)
            pt_y.append(pt.y)
            img_seq[pt.x, pt.y] = i
            i += 1
        plt.figure()
        plt.imshow(img_seq)
        print('TOTAL MOVES: ', i)
        plt.figure()
        plt.plot(pt_x, pt_y)



if __name__ == "__main__":
    Tracker = Sweep_Tracker()
    Tracker.simulation_class.display_trimmed_img()
    Tracker.RUN()
    Tracker.simulation_class.display_trimmed_img()
    Tracker.plot_path()
    plt.show()