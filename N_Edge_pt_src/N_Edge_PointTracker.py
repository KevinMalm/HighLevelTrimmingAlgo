import matplotlib.pyplot as plt
import numpy as np
import math
from VectorClass import Vector2, PT_ZERO
import time
from SimulationManager import SimulationManager
from ShapeGenerator import build_circle, build_rect
from Variables_and_Constants import get_brush, N,M

CIRCLE = True
#constants
RIGHT = Vector2(0,-1)
LEFT = Vector2(0,1)
UP = Vector2(1,0)
DOWN = Vector2(-1,0)

ABS = -1
GRASS = 1

N_8_moves = [
    [RIGHT],
    [RIGHT, UP],
    [UP],
    [UP, LEFT],
    [LEFT],
    [LEFT, DOWN],
    [DOWN],
    [DOWN, RIGHT]
]

class N_EdgePointTracker:

    simulation_class: SimulationManager
    assumed_center: Vector2
    current_trimmer_pos: Vector2
    trimmer_moves = []
    edge_pts = []

    last_read_value = ABS

    def __init__(self):
        self.simulation_class = SimulationManager(build_fn=build_circle if CIRCLE else build_rect)
        self.assumed_center = self.simulation_class.get_center()
        #set trimmer head in center
        self.current_trimmer_pos = self.assumed_center.copy()
        self.LOG_MOVE()
        self.edge_pts = []
        self.trimmer_moves = []

    def FIND_EDGE_PTS(self):
        #step 1: find N edges away from center

        for move_array in N_8_moves:
            self.run_to_edge(move_array)
            self.reset_to_center()


        return
    def reset_to_center(self):
        self.current_trimmer_pos = self.assumed_center.copy()
        self.LOG_MOVE()

    def run_to_edge(self, moves):
        self.last_read_value = ABS
        #moves = self.compute_line(angle)
        #print('angle', angle, ' moves ', [m.toString() for m in moves])
        while(self.last_read_value != GRASS):
            for m in moves:
                if(self.able_to_move(m)):
                    self.current_trimmer_pos.Add(m)
                    self.LOG_MOVE()
                else:
                    return
            self.update_sensor()
        self.edge_pts.append(self.current_trimmer_pos)

    def update_sensor(self):
        self.last_read_value = self.simulation_class.read_at_pt(pt = self.current_trimmer_pos)
        return

    #computes path from current_pos to at given angle
    def compute_line(self, angle):
        move_list = []

        d_y = math.sin(angle * math.radians(angle)) #assume h = 1
        d_x = math.cos(angle * math.radians(angle))
        plt.plot([self.assumed_center.x, self.assumed_center.x + (d_x * 100)], [self.assumed_center.y, self.assumed_center.y + (d_y * 100)], label = repr(angle))

        print('angle: ', angle, ' y: ', d_y, ' x: ', d_x)
        if(d_y == 0):
            return [RIGHT] if d_x < 0 else [LEFT]
        if(d_x == 0):
            return [UP] if d_y < 0 else [DOWN]
        y_steps = int(d_y / d_x)
        if(y_steps == 0): # need to start moving up
            x_steps = int(d_x / d_y)
            move_list.append(UP if (d_y < 0) else DOWN)
            for _ in range(x_steps):
                move_list.append(RIGHT if d_x < 0 else LEFT)
            return move_list
        #add x moves
        move_list.append(RIGHT if (d_x < 0) else LEFT)
        for _ in range(y_steps):
            move_list.append(UP if d_y < 0 else DOWN)
    
        return move_list


    def LOG_MOVE(self):
        #save move
        self.trimmer_moves.append(self.current_trimmer_pos.copy())
        #trim
        self.simulation_class.trim(self.current_trimmer_pos)

    def plot_path(self):
        img_seq = np.zeros([N, M])
        i = 1
        for pt in self.trimmer_moves:
            img_seq[pt.x, pt.y] = i
            i += 1
        plt.figure()
        plt.imshow(img_seq)
        print('TOTAL MOVES: ', i)
        plt.figure()
        x, y = [], []
        for pt in self.edge_pts:
            x.append(pt.x)
            y.append(pt.y)
        plt.scatter(x, y)
        plt.xlim(0, N)
        plt.ylim(0, M)


    def able_to_move(self, pt):
        possible_move = self.current_trimmer_pos.copy().Add(pt)
        if(possible_move.x < 0 or possible_move.x >= N or possible_move.y < 0 or possible_move.y >= M):
            return False
        return True

    def chaikin_smooth(self, n):
        for _ in range(n):
            #Chaikin Algo
            temp_list = self.edge_pts
            new_list = []
            for i in range(-1, len(temp_list) - 1):
                a = temp_list[i]
                b = temp_list[i+1]
                ab = Vector2( (3/4) *  a.x + (1/4) * b.x, (3/4) *  a.y + (1/4) * b.y )
                ba = Vector2( (3/4) *  b.x + (1/4) * a.x, (3/4) *  b.y + (1/4) * a.y )

                new_list.append(ab)
                new_list.append(ba)

            self.edge_pts = new_list
        return

    def follow_circle_path(self, refine = 5):  
        #smooth path
        self.chaikin_smooth(refine)
        for pt in self.edge_pts:
            self.current_trimmer_pos = pt
            self.LOG_MOVE()

        return

        self.chaikin_smooth(refine)
        tmp_list = self.edge_pts.copy()
        current_pt = tmp_list.pop().copy()
        while(len(tmp_list) > 0):
            next_pt = tmp_list[-1]
            while(current_pt.Distance(next_pt) > 0.01):
                pt = self.current_trimmer_pos.copy().Add(current_pt.step_to(next_pt))
                if(self.able_to_move(pt)):
                    self.current_trimmer_pos.Add(current_pt.step_to(next_pt))
                    self.LOG_MOVE()
                else:
                    return
            current_pt = tmp_list.pop().copy()
        
    def follow_rect_path(self):
        max_x, max_y, min_x, min_y = 0, 0, 0, 0
        
        

        
if __name__ == "__main__":       

    process = N_EdgePointTracker()
    process.simulation_class.display_original_img()
    plt.show()
    process.follow_circle_path()
    process.simulation_class.display_trimmed_img()
    process.plot_path()
    plt.show()




