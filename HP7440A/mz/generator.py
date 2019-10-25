import numpy
from numpy.random import randint as rand
import matplotlib.pyplot as pyplot

maze_size = (31, 31)
walls = numpy.ones(maze_size, dtype=bool)

pyplot.figure(figsize=(10, 5))
pyplot.xticks([]), pyplot.yticks([])

current_cell = [1, 1]
visited = [current_cell]
current_stack = [current_cell]
walls[current_cell[0], current_cell[1]] = 0 
walls[1, 0] = walls[maze_size[0] - 2, maze_size[1] - 1] = 0

directions = [[0, 1], [1, 0], [0,-1], [-1, 0]]

while len(current_stack) > 0:
    possible_directions = []
    for i in range(0, 4):
        cell = [current_cell[0] + 2 * directions[i][0], current_cell[1] + 2 * directions[i][1]]
        if cell[0] > 0 and cell[1] > 0 and cell[0] < maze_size[0] and cell[1] < maze_size[1] and walls[cell[0], cell[1]] == 1:
            possible_directions.append(directions[i])
    if len(possible_directions) > 0:
        direction = possible_directions[rand(0, len(possible_directions))]
        current_cell = [current_cell[0] + direction[0], current_cell[1] + direction[1]]
        walls[current_cell[0], current_cell[1]] = 0
        current_cell = [current_cell[0] + direction[0], current_cell[1] + direction[1]]
        walls[current_cell[0], current_cell[1]] = 0
        current_stack.append(current_cell)
    else:
        current_cell = current_stack.pop()

def drawline(x_i, y_i, x_f, y_f):
    print("PU;")
    print("PA" + str(int(x_i * square_size + 100)) + "," + str(int(y_i * square_size + 100)) + ";")
    print("PD;")
    print("PA" + str(int(x_f * square_size + 100)) + "," + str(int(y_f * square_size + 100)) + ";")

print("SP1;")
square_size = 7650 / maze_size[1] * 0.95
drawline(100, 100, 100, (maze_size[1] - 1) * square_size + 100)
drawline(square_size * 2 + 100, 100, (maze_size[0] - 1) * square_size + 100, 100)

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
        if cell[0] >= 0 and cell[1] >= 0 and cell[0] < maze_size[0] and cell[1] < maze_size[1] and walls[cell[0], cell[1]] == 1:
            adjacency.append(directions[i])
    return adjacency

for i in range(1, maze_size[0]):
    for j in range(1, maze_size[1]):
        if [i, j] not in visited and walls[i, j] == 1:
            generateLines([i,j], [i,j], [0, 1])
