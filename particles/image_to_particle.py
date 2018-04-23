import particle
import math
import random
import numpy as np
import cv2
import argparse

def GetAccelFromGradient(image, particle_status):
    position = particle_status[0]
    velocity = particle_status[1]
    brightness = float(image.item(int(position["y"]) % np.size(image, 0), int(position["x"]) % np.size(image, 1)) + 1)
    return {"x": brightness * random.randint(-50, 50) - velocity["x"] * 10, "y": brightness * random.randint(-50, 50) - velocity["y"] * 10}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required = True, help = "Path to the image")
    args = vars(ap.parse_args())
 
    test_image = cv2.imread(args["image"], 0)
    cv2.imshow('test', test_image)

    screen_size = np.size(test_image, 1)
    point_cloud = [particle.Particle(screen_size) for i in range(1000)]
    counter = 0.0
    while counter < 100:
        counter += 0.005
        main_image = np.zeros((screen_size, screen_size, 3), np.uint8)
        for point in point_cloud:
            point_pos = point.GetStatus()[0]
            acceleration = GetAccelFromGradient(test_image, point.GetStatus())
            point.Update(acceleration)
            main_image[int(point_pos["y"]), int(point_pos["x"])] = (255, 255, 255)
        cv2.imshow('image', main_image)
        cv2.waitKey(1)

    cv2.destroyAllWindows()
