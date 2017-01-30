from enum import Enum
import os

class PointVal(Enum):
    BLANK = 0
    CROSS = 1
    NAUGHT = 2

field_data = [[PointVal.BLANK for i in range(3)] for j in range(3)]

def render_field(x, y, type_of_element):
    global field_data
    field_data[y][x] = type_of_element
    for line_vals in field_data:
        line = '|'
        for val in line_vals:
            if val == PointVal.CROSS:
                line += "x|"
            elif val == PointVal.NAUGHT:
                line += "o|"
            else:
                line += " |"
        print(line)

def complete_game(field_data):
    for row in field_data:
        if len(set(row)) == 1 and row[0] != PointVal.BLANK:
            return (True, row[0])
    for num in range(len(field_data)):
        column = []
        for row in field_data:
            column.append(row[num])
        if len(set(column)) == 1 and column[0] != PointVal.BLANK:
            return (True, column[0])
    angle = []
    back_angle = []
    for num in range(len(field_data)):
        angle.append(field_data[num][num])
        back_angle.append(field_data[len(field_data) - num - 1][num])
    if len(set(angle)) == 1 and angle[0] != PointVal.BLANK:
        return (True, angle[0])
    if len(set(back_angle)) == 1 and back_angle[0] != PointVal.BLANK:
        return (True, back_angle[0])
    return False

os.system('clear')
render_field(0,0,PointVal.BLANK)
game_done = False
while not game_done:
    global field_data

    x = int(raw_input("Enter x coord: ")) % 3
    y = int(raw_input("Enter y coord: ")) % 3

    os.system('clear')
    render_field(x,y, PointVal.CROSS)

    game_done = complete_game(field_data)

print("Winner is " + str(game_done[1]))
