# See the context for this code at https://steampunc.github.io//post/2018/01/07/chladni.html
# Generates approximations of Chladni patterns using some fun math

import math
import statistics as stat
import numpy as np
import cv2

x_screen_size = 100
y_screen_size = 100
emitter_matrix_size = 7 # can't modify this value yet

velocity = 300
#frequency = 15

def GetDistance(x, y, emitter_x, emitter_y):
    x_length = (3 - emitter_x) * x_screen_size - ((x_screen_size / 2.0) - x)
    y_length = (3 - emitter_y) * y_screen_size - ((y_screen_size / 2.0) - y)

    crosses = abs(3 - emitter_x) + abs(3 - emitter_y)

    return math.sqrt(x_length * x_length + y_length * y_length), crosses 

frequency = 10.0
counter = 0
while frequency <= 20:
    counter += 1
    wavelength = (velocity / frequency)
    main_image = np.zeros((y_screen_size, x_screen_size, 3), np.uint8)
    for x in range(x_screen_size):
        for y in range(y_screen_size):
            distances = []
            for emitter_x in range(emitter_matrix_size):
                for emitter_y in range(emitter_matrix_size):
                    point_distance = GetDistance(x, y, emitter_x, emitter_y)
                    effective_distance = math.fmod(point_distance[0], wavelength)
                    if point_distance[1] % 2 == 1:
                        effective_distance = wavelength - effective_distance
                    distances.append(effective_distance)

            brightness = 255 - stat.stdev(distances) * 100
            main_image[y, x] = (brightness, brightness, brightness)

    main_image = cv2.resize(main_image, (0, 0), fx = 4, fy = 4)
    cv2.imshow('image', main_image)
    cv2.imwrite('chladni-images/chladni_c' + str(counter).zfill(4) + 'f' + str(frequency) + 'v' + str(velocity) + '.png', main_image)
    print("done with image f" + str(frequency))
    frequency += 0.025
cv2.waitKey(0)

cv2.destroyAllWindows()
