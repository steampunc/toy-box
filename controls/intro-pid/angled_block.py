import pygame
import math
import time

def RotatePoint(pivot, point, angle):
    s = math.sin(angle)
    c = math.cos(angle)

    x = point[0] - pivot[0]
    y = point[1] - pivot[1]

    new_x = x * c - y * s
    new_y = x * s + y * c

    return (new_x + pivot[0], new_y + pivot[1])

class Block():
    def __init__(self, center, width, height, angle):
        self.angle = angle
        self.center = center
        self.point1 = (center[0] - (width / 2.0), center[1] - (height / 2.0))
        self.point2 = (center[0] + (width / 2.0), center[1] - (height / 2.0))
        self.point3 = (center[0] - (width / 2.0), center[1] + (height / 2.0))
        self.point4 = (center[0] + (width / 2.0), center[1] + (height / 2.0))
        self.velocity = 0

        self.point1 = RotatePoint(self.center, self.point1, angle)
        self.point2 = RotatePoint(self.center, self.point2, angle)
        self.point3 = RotatePoint(self.center, self.point3, angle)
        self.point4 = RotatePoint(self.center, self.point4, angle)

        self.dt = 0.005


    def Translate(self, velocity):
        dx = velocity * math.cos(self.angle)
        dy = velocity * math.sin(self.angle) 
        self.center = (self.center[0] + dx * self.dt, self.center[1] + dy * self.dt)
        self.point1 = (self.point1[0] + dx * self.dt, self.point1[1] + dy * self.dt)
        self.point2 = (self.point2[0] + dx * self.dt, self.point2[1] + dy * self.dt)
        self.point3 = (self.point3[0] + dx * self.dt, self.point3[1] + dy * self.dt)
        self.point4 = (self.point4[0] + dx * self.dt, self.point4[1] + dy * self.dt)

    def Update(self, window, controller_input):

        accel = 1000

        self.velocity += (controller_input + accel) * self.dt
        self.Translate(self.velocity)

        pygame.draw.polygon(window, (0, 0, 255), (self.point1, self.point2, self.point4, self.point3), 1)
        pygame.draw.line(window, (0, 0, 0), (0,71), (1280, 809))
        pygame.draw.line(window, (255, 0, 0), (self.center[0] + math.sin(self.angle) * 70, self.center[1] - math.cos(self.angle) * 70), (goal, 390), 3) 
        window.blit(pygame.font.SysFont('Comic Sans MS', 30).render("Error:" + str(int(goal - self.center[0])), False, (0, 0, 0)),(int((self.center[0] + goal)/2),380))

window = pygame.display.set_mode((1280, 720))
pygame.font.init()



window.fill((255, 255, 255))
block = Block((500, 300), 100, 100, 0.52359877559)


timer = 0

integral = 0

while timer < 20:
    window.fill((255, 255, 255))
    timer += block.dt

    # Stuff we care about

    # PID Constants
    kP = 0 #-40
    kD = 0 #-10
    kI = 0 #-11

    goal = 800




    error = goal - block.center[0]
    integral += error * 0.005
    controller_input = error * 10 - 10 * block.velocity + 10 * integral
    
    
    
    
    
    block.Update(window, controller_input)
    pygame.display.flip()
    time.sleep(0.001)
