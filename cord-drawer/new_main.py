import math
import random
import numpy as np
import cv2
import copy
from canvas_objects import *

class Board:
    def __init__(self, l1, l2, canvas_x, canvas_y):
        self.canvas = np.zeros((canvas_y, canvas_x, 3), np.uint8)
        self.canvas_x = canvas_x
        self.canvas_y = canvas_y
        self.l1 = l1
        self.l2 = l2

    def move(self, l1, l2):
        if l1 + l2 > self.canvas_x:
            initial_l1 = self.l1
            initial_l2 = self.l2
            dl1 = abs(l1 - self.l1)
            dl2 = abs(l2 - self.l2)
            num_steps = int(max(dl1, dl2))
            for i in range(0, num_steps):
                self.l1 = self.l1 + (l1 - initial_l1)/num_steps
                self.l2 = self.l2 + (l2 - initial_l2)/num_steps
                self.render()
             
    def to_cartesian(self):
        l1 = self.l1
        l2 = self.l2
        gamma = (l1**2 + self.canvas_x**2 - l2**2)/(2*l1*self.canvas_x)
        y = l1 * math.sqrt(1 - (gamma)**2)
        x = l1 * gamma
        return (int(x), int(y))
        
        
    def render(self):
        copy_canvas = copy.deepcopy(self.canvas)

        (x, y) = self.to_cartesian()
        self.canvas[int(y), int(x)] = (255, 255, 255)

        for i in range(0, x):
            copy_canvas[int(y/x * i), i] = (0, 255, 0)
        for i in range(x, self.canvas_x):
            copy_canvas[int(y - y/(self.canvas_x - x)* (i-x)), i] = (0, 255, 0)
        cv2.imshow('image', copy_canvas)
        cv2.waitKey(1)

def to_radial(x, y):
    l1 = y/ math.cos(math.atan(x/y))
    l2 = y/ math.cos(math.atan((canvas_x- x)/ y))
    return (l1, l2)

canvas_x = 500
(init_l1, init_l2) = to_radial(300, 250)
board = Board(init_l1, init_l2, canvas_x, 500)
objects = [Arc(250, 250, 300, 250, 2* math.pi), Arc(150, 250, 200, 250, -math.pi)]

for item in objects:
    while item.state() != "DONE":
        (x, y) = item.draw()
        (l1, l2) = to_radial(x, y)
        board.move(l1, l2)


cv2.waitKey(0)

