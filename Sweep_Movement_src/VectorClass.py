import numpy as np
import math



class Vector2:
    
    x = 0
    y = 0
    def __init__(self,_x, _y):
        self.x = _x
        self.y = _y
        self.ROUND()
    def Add(self, v):
        self.x += v.x;
        self.y += v.y

        return self
    def Subtract(self, v):
        self.x -= v.x;
        self.y -= v.y
        return self
    def Distance(self, v, euclidean = True):
        x_d = self.x - v.x
        y_d = self.y - v.y
        if(euclidean):
            return (x_d**2 + y_d**2) ** (1/2)
        else:
            return x_d, y_d

    def set(self, pt):
        self.x = pt.x
        self.y = pt.y

    def copy(self):
        return Vector2(self.x, self.y)
    
    def REVERSE(self):
        return Vector2(self.x * -1, self.y * -1)
    def toString(self):
        return '(' + repr(self.x) + ', ' + repr(self.y) + ')'
    
    def step_to(self, V):
        x, y = self.Distance(V, euclidean= False)
        f = int(abs(x) / abs(y))
        if(f == 1):
            return Vector2(-1 if x > 0 else 1, -1 if y > 0 else 1)
        elif(f == 0):
            return Vector2(0, -1 if y > 0 else 1)
        else:
            return Vector2(-1 if x > 0 else 1, 0)
    def ROUND(self):
        self.x = int(self.x)
        self.y = int(self.y)
PT_ZERO = Vector2(0, 0)