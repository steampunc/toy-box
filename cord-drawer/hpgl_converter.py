from arduino_drawer import *

board = Drawer(0.01, 0.9425)

with open("input.txt", "r") as hpgl_file:
    i = 0
    for line in hpgl_file:
        if line[:2] == "PA":
            if i % 2 == 0:
                str_pos = line[2:].split(";")[0].split(",")
                pos = [float(str_pos[0]), float(str_pos[1])]
                board.move((pos[0] / 10300.0) * 0.6 + 0.15, (pos[1] / 10300.0) * 0.6 + 0.25)
            i += 1
