import pygame
import time

class Block():
    def __init__(self, center, width, height):
        self.center = center
        self.point1 = (center[0] - (width / 2.0), center[1] - (height / 2.0))
        self.point2 = (center[0] + (width / 2.0), center[1] - (height / 2.0))
        self.point3 = (center[0] - (width / 2.0), center[1] + (height / 2.0))
        self.point4 = (center[0] + (width / 2.0), center[1] + (height / 2.0))
        self.velocity = 0

        self.dt = 0.005

    def Translate(self, velocity):
        self.center = (self.center[0] + velocity * self.dt, self.center[1])
        self.point1 = (self.point1[0] + velocity * self.dt, self.point1[1])
        self.point2 = (self.point2[0] + velocity * self.dt, self.point2[1])
        self.point3 = (self.point3[0] + velocity * self.dt, self.point3[1])
        self.point4 = (self.point4[0] + velocity * self.dt, self.point4[1])

    def Update(self, window, controller_input):

        self.velocity += controller_input * self.dt - self.velocity * self.dt * 2 
        self.Translate(self.velocity)

        pygame.draw.polygon(window, (0, 0, 255), (self.point1, self.point2, self.point4, self.point3), 1)
        pygame.draw.line(window, (0, 0, 0), (0,351), (1280, 351))
        pygame.draw.line(window, (255, 0, 0), (self.center[0], 370), (goal, 370), 3) 
        window.blit(pygame.font.SysFont('Comic Sans MS', 30).render("Error:" + str(int(goal - self.center[0])), False, (0, 0, 0)),(int((self.center[0] + goal)/2),380))

window = pygame.display.set_mode((1280, 720))
pygame.font.init()



window.fill((255, 255, 255))
block = Block((500, 300), 100, 100)

timer = 0

while timer < 10:
    window.fill((255, 255, 255))
    timer += block.dt

    # Stuff we care about:

    # P constant
    kP = 0



    goal = 800



    block.center[0]

    controller_input = 10 *(goal -  block.center[0])

    
    


    block.Update(window, controller_input)
    pygame.display.flip()
    time.sleep(0.001)
