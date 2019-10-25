import numpy
from numpy.random import randint as rand
from PIL import Image

img = Image.open("binaryImg.jpg")
walls = numpy.array(img)
maze_size = walls.shape

current_cell = [1, 1]
visited = [current_cell]

directions = [[0, 1], [1, 0], [0,-1], [-1, 0]]

square_size = 7650.0 / float(max(maze_size)) * 0.95
def drawline(x_i, y_i, x_f, y_f):
    print("PU;")
    print("PA" + str(int(x_i * square_size + 100)) + "," + str(int(y_i * square_size + 100)) + ";")
    print("PD;")
    print("PA" + str(int(x_f * square_size + 100)) + "," + str(int(y_f * square_size + 100)) + ";")

print("SP1;")

def generateLines(origin, point, current_dir):
    visited.append(point)
    adjacent_dirs = getAdjacent(point)
    all_visited = True
    for direction in adjacent_dirs:
        new_point = [point[0] + direction[0], point[1] + direction[1]]
        if new_point not in visited:
            visited.append(new_point)
            all_visited = False
            if direction != current_dir:
                if current_dir not in adjacent_dirs:
                    drawline(origin[0], origin[1], point[0], point[1]);
                generateLines(point, new_point, direction)
            else:
                generateLines(origin, new_point, direction)
    if all_visited:
        drawline(origin[0], origin[1], point[0], point[1]);
    return


def getAdjacent(point):
    adjacency = []
    for i in range(0, 4):
        cell = [point[0] + directions[i][0], point[1] + directions[i][1]]
        if cell[0] >= 0 and cell[1] >= 0 and cell[0] < maze_size[0] and cell[1] < maze_size[1] and walls[cell[0], cell[1]] < 150:
            adjacency.append(directions[i])
    return adjacency

for i in range(1, maze_size[0]):
    for j in range(1, maze_size[1]):
        if [i, j] not in visited and walls[i, j] < 150:
            generateLines([i,j], [i,j], [0, 1])
