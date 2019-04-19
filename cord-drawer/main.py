import math
import random
import numpy as np
import cv2
import copy
import canvas_objects

screen_size = 500

def draw_cables(x,y, main_image):
    main_image[y,x] = (255,0,0)

    for i in range(0, x):
        main_image[int(y/x * i), i] = (0, 255, 0)
    for i in range(x, screen_size):
        main_image[int(y - y/(screen_size - x)* (i-x)), i] = (0, 255, 0)
    
def find_ls(x, y):
    l1 = y/ math.cos(math.atan(x/y))
    l2 = y/ math.cos(math.atan((screen_size - x)/ y))
    return (l1, l2)


main_image = np.zeros((screen_size, screen_size, 3), np.uint8)


def render(l1,l2, on):
    if l1 + l2 > screen_size:
        
        gamma = (l1**2 + screen_size**2 - l2**2)/(2*l1*screen_size)
        y = l1 * math.sqrt(1 - (gamma)**2)
        x = l1 * gamma
        if on:
            main_image[int(y), int(x)] = (255, 255, 255)

        copy_image = copy.deepcopy(main_image)
        draw_cables(int(x), int(y), copy_image)

        cv2.imshow('image', copy_image)
        cv2.waitKey(1)


counter = 0.0
x_period = 8
y_period = 5

while counter <= 100:
    counter += 0.001
    y = 200 * math.sin(y_period * counter) + screen_size / 2.0
    x = 200 * math.sin(x_period * counter) + screen_size / 2.0
    (l1, l2) = find_ls(x, y)
    
    render(l1,l2)

cv2.destroyAllWindows()

