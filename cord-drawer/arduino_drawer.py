import serial
import struct
import math
from canvas_objects import *


# initial starting point is at .84m for both

board_width = 0.95
pulley_circumference = 0.145
clicks_per_m = 200 / pulley_circumference
ser = serial.Serial('/dev/ttyACM0', 9600)

class Drawer:
    def __init__(self, right_cal, left_cal):
        self.len_r = right_cal
        self.len_l = left_cal
        self.dl_net = 0

    def to_radial(self, x, y):
        len_r = y/ math.cos(math.atan(x/y))
        len_l = y/ math.cos(math.atan((board_width- x)/ y))
        return (len_r, len_l)

    def to_cartesian(self, len_r, len_l):
        gamma = 1
        if abs(2*len_r*board_width) > 1e-5:
            gamma = (len_r**2 + board_width**2 - len_l**2)/(2*len_r*board_width)
        y = len_r * math.sqrt(1 - (gamma)**2)
        x = len_r * gamma
        return (x, y)

    def send_to_arduino(self, dlr, dll, i):
        message = str(int(-dlr * clicks_per_m)) + "," + str(int(dll * clicks_per_m)) + "\n"
        print(message)
        ser.write(message.encode())
        print("hi")
        not_done = True
        print(ser.read())

    def move(self, x, y):
        print("Moving to " + str(x) + ", " + str(y))
        (x_, y_) = self.to_cartesian(self.len_r, self.len_l)
        resolution = int(math.sqrt((x_ - x)**2 + (y_ - y)**2) * 30)
        dx = 0
        dy = 0

        if resolution != 0:
            dx = (x - x_) / resolution
            dy = (y - y_) / resolution

        for i in range(0, resolution):
            (len_r, len_l) = self.to_radial(x_, y_)
            (goal_lr, goal_ll) = self.to_radial(x_ + dx, y_ + dy)
            (x_, y_) = (x_ + dx, y_ + dy)
            (dlr, dll) = (goal_lr - len_r, goal_ll - len_l)
            self.send_to_arduino(dlr, dll, i)
            print(x_, y_)

        (self.len_r, self.len_l) = self.to_radial(x_, y_) 

        print("DONE, moved R to " + str(self.len_r) + " and L to " + str(self.len_l) + ", cartesian eq is " + str((x_, y_)))

    def draw_arc(self, center_x, center_y, x_i, y_i, delta_angle):
        print("Drawing arc with center at " + str((center_x, center_y)) + ", angle of " + str(delta_angle))
        r = math.sqrt((center_x - x_i)**2 + (center_y - y_i)**2)
        theta = math.pi/2
        if abs(x_i - center_x) > 1e-4:
            theta = math.atan2((y_i - center_y),(x_i - center_x))
        else:
            theta = math.pi/2 - math.atan2((x_i - center_x),(y_i - center_y))
        self.move(x_i, y_i) # move to starting position if not already there
        (x_, y_) = (x_i, y_i)

        resolution = int(abs(delta_angle) * r * 30) 
        print(resolution)
        for i in range(0, resolution):
            theta = theta + (delta_angle / resolution)
            (x, y) = (center_x + r*math.cos(theta), center_y + r * math.sin(theta))
            (len_r, len_l) = self.to_radial(x_, y_)
            (goal_lr, goal_ll) = self.to_radial(x, y)
            (self.len_r, self.len_l) = (goal_lr, goal_ll)
            (x_, y_) = (x, y)
            (dlr, dll) = (goal_lr - len_r, goal_ll - len_l)
            print(x_, y_, theta)
            self.send_to_arduino(dlr, dll, i)

        print("DONE, drew arc with radius " + str(r))


board = Drawer(0.01, 0.9425)
board.move(0.3,0.3)
board.move(0.3,0.4)
board.move(0.4,0.4)
board.move(0.4,0.3)
board.move(0.3,0.3)
