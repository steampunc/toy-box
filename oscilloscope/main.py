import soundfile as sf
import numpy as np
import random
import cv2

screen_size = 300
main_image = np.zeros((screen_size, screen_size, 3), np.uint8)
data, samplerate = sf.read('other.ogg')
counter = 0
for sample in data:
    counter += 1
    main_image[int(screen_size / 2.0 + sample[0] * screen_size / 2.0), int(screen_size / 2.0 + sample[1] * screen_size / 2.0)] = [0, 255, 0]
    if counter % 100 == 0:
        for x in xrange(main_image.shape[0]):
            for y in xrange(main_image.shape[1]):
                if main_image[y,x][1] != 0:
                    main_image[y,x] = [0, main_image[y,x][1] - 50, 0]

        cv2.imshow('image',main_image)
        print(sample)
        cv2.waitKey(1)

cv2.destroyAllWindows()

