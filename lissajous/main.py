import math
import random
import numpy as np
import cv2

screen_size = 500
main_image = np.zeros((screen_size, screen_size, 3), np.uint8)
counter = 0.0
x_period = 8
y_period = 5
while counter <= 100:
    counter += 0.001
    y = 200 * math.sin(y_period * counter) + screen_size / 2.0
    x = 200 * math.sin(x_period * counter) + screen_size / 2.0
    main_image[int(y),int(x)] = (255, 255, 255) 
    print(main_image)
    cv2.imshow('image', main_image)
    cv2.waitKey(1)

cv2.destroyAllWindows()

