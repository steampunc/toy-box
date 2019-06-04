import pygame
import numpy
import math
import time

class Pendulum():
    def __init__(self):
        self.length = 0.4
        self.cart_mass = 0.7
        self.pend_mass = 0.3
        self.x = 0.75
        self.dx = 0
        self.theta = 0.4
        self.dtheta = 0
        self.dt = 0.005

    def Update(self, u):
        accel = u
        self.dx += accel * self.dt
        self.x += self.dx * self.dt
        
        ang_accel = math.sin(self.theta) * 100 - accel
        self.dtheta += ang_accel * self.dt
        self.theta += self.dtheta * self.dt

    def Render(self, window):
        length_factor = 500
        width = 100
        height = 100

        center = (self.x * length_factor, 300)

        rc = self.length * self.pend_mass / (self.pend_mass + self.cart_mass)
        rp = self.length * self.cart_mass / (self.pend_mass + self.cart_mass)

        cart_center = (center[0] - length_factor * rc * math.sin(self.theta), center[1])

        cart1 = (cart_center[0] - (width / 2.0), cart_center[1] - (height / 2.0))
        cart2 = (cart_center[0] + (width / 2.0), cart_center[1] - (height / 2.0))
        cart3 = (cart_center[0] - (width / 2.0), cart_center[1] + (height / 2.0))
        cart4 = (cart_center[0] + (width / 2.0), cart_center[1] + (height / 2.0))

        pend = (cart_center[0] + self.length * length_factor * math.sin(self.theta), cart_center[1] - self.length * length_factor * math.cos(self.theta))


        window.fill((255, 255, 255))
        pygame.draw.polygon(window, (0, 0, 255), (cart1, cart2, cart4, cart3), 1)
        pygame.draw.line(window, (0, 0, 0), cart_center, pend)
        

window = pygame.display.set_mode((1280, 720))
pygame.font.init()

window.fill((255, 255, 255))
pendulum = Pendulum()

timer = 0

while timer < 10:
    timer += pendulum.dt
    u = pendulum.theta * 500 + pendulum.dtheta * 10 + (2-pendulum.x) * 1
    pendulum.Update(u)
    pendulum.Render(window)
    pygame.display.flip()
    time.sleep(0.01)
