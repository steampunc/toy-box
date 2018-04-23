import math
import random
import numpy as np
import cv2

class Particle(object):
    position = {}
    velocity = {}
    dt = 0.005
    image_size = 500

    def __init__(self, image_size):
        self.position = {"x": random.randint(0,image_size),"y": random.randint(0, image_size)}
        self.velocity = {"x": 0,"y": 0}
        self.image_size = image_size

    def Update(self, acceleration):
        self.velocity["x"] += float(acceleration["x"]) * self.dt
        self.velocity["y"] += float(acceleration["y"]) * self.dt
        
        self.position["x"] += self.velocity["x"] * self.dt
        self.position["y"] += self.velocity["y"] * self.dt

        self.position["x"] = math.fmod(self.position["x"], self.image_size)
        self.position["y"] = math.fmod(self.position["y"], self.image_size)

    def GetStatus(self):
        return self.position, self.velocity

if __name__ == "__main__":
    screen_size = 500
    point_cloud = [Particle(screen_size) for i in range(100)]
    counter = 0.0
    while counter < 100:
        counter += 0.005
        main_image = np.zeros((screen_size, screen_size, 3), np.uint8)
        for point in point_cloud:
            acceleration = {"x":random.randint(-200,200), "y":random.randint(-200,200)}
            point.Update(acceleration)
            point_pos = point.GetStatus()[0]
            main_image[int(point_pos["y"]), int(point_pos["x"])] = (255, 255, 255)
        cv2.imshow('image', main_image)
        cv2.waitKey(1)

    cv2.destroyAllWindows()

