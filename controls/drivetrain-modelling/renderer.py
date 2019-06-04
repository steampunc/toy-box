import math
import csv
import time
import pygame

class Drivetrain(object):
    def __init__(self, center, width, height, angle):
        self.center = center
        self.point1 = (center[0] - (width / 2.0), center[1] - (height / 2.0))
        self.point2 = (center[0] + (width / 2.0), center[1] - (height / 2.0))
        self.point3 = (center[0] - (width / 2.0), center[1] + (height / 2.0))
        self.point4 = (center[0] + (width / 2.0), center[1] + (height / 2.0))
        self.angle = angle

        self.point1 = self.RotatePoint(self.center, self.point1, angle)
        self.point2 = self.RotatePoint(self.center, self.point2, angle)
        self.point3 = self.RotatePoint(self.center, self.point3, angle)
        self.point4 = self.RotatePoint(self.center, self.point4, angle)
        self.dt = 0.005
    
    def TranslateBox(self, velocity):
        c = math.cos(self.angle)
        s = math.sin(self.angle)

        dx = velocity * s * self.dt * 200
        dy = -velocity * c * self.dt * 200

        self.center = (self.center[0] + dx, self.center[1] + dy)
        self.point1 = (self.point1[0] + dx, self.point1[1] + dy)
        self.point2 = (self.point2[0] + dx, self.point2[1] + dy)
        self.point3 = (self.point3[0] + dx, self.point3[1] + dy)
        self.point4 = (self.point4[0] + dx, self.point4[1] + dy)

    def Update(self, window, velocity, angular_velocity):
        self.angle += angular_velocity * self.dt

        self.TranslateBox(velocity)

        self.point1 = self.RotatePoint(self.center, self.point1, angular_velocity * self.dt)
        self.point2 = self.RotatePoint(self.center, self.point2, angular_velocity * self.dt)
        self.point3 = self.RotatePoint(self.center, self.point3, angular_velocity * self.dt)
        self.point4 = self.RotatePoint(self.center, self.point4, angular_velocity * self.dt)

        pygame.draw.polygon(window, (0, 0, 255), (self.point1, self.point2, self.point4, self.point3), 1)

    def RotatePoint(self, pivot, point, angle):
        s = math.sin(angle)
        c = math.cos(angle)

        x = point[0] - pivot[0]
        y = point[1] - pivot[1]

        new_x = x * c - y * s
        new_y = x * s + y * c

        return (new_x + pivot[0], new_y + pivot[1])


window = pygame.display.set_mode((1024, 760))
window.fill((255, 255, 255))
drivetrain = Drivetrain((500, 300), 90, 120, 0)

with open("logs/model_status.csv", 'r') as logfile_reader:
    next(logfile_reader, None)
    data = csv.reader(logfile_reader, quoting=csv.QUOTE_NONNUMERIC)
    # 7 8 9 10 position, velocity, angle, angular velocity
    for row in data:
        window.fill((255, 255, 255))
        print(row)
        drivetrain.Update(window, row[7], row[9])
        pygame.display.flip()
        time.sleep(0.0001)
