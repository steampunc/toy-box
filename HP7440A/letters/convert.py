import random

input_string = open("letter.txt").read()
font_size = 0.80
(x_pos, y_pos) = (200, 300)

def get_adjust(char):
    if char == "a":
        return (160, 210)
    if char == "b":
        return (40, 200)
    if char == "c":
        return (160, 150)
    if char == "d":
        return (30, 200)
    if char == "e":
        return (160, 150)
    if char == "f":
        return (30, 120)
    if char == "g":
        return (160, 180)
    if char == "h":
        return (40, 190)
    if char == "i":
        return (160, 120)
    if char == "j":
        return (150, 110)
    if char == "k":
        return (40, 200)
    if char == "l":
        return (40, 150)
    if char == "m":
        return (160, 350)
    if char == "n":
        return (160, 270)
    if char == "o":
        return (160, 160)
    if char == "p":
        return (150, 190)
    if char == "q":
        return (160, 190)
    if char == "r":
        return (160, 160)
    if char == "s":
        return (170, 130)
    if char == "t":
        return (40, 150)
    if char == "u":
        return (160, 200)
    if char == "v":
        return (160, 200)
    if char == "w":
        return (160, 270)
    if char == "x":
        return (160, 220)
    if char == "y":
        return (160, 240)
    if char == "z":
        return (160, 180)
    if char == "A":
        return (50, 200)
    if char == "B":
        return (40, 170)
    if char == "C":
        return (50, 150)
    if char == "D":
        return (40, 250)
    if char == "E":
        return (50, 130)
    if char == "F":
        return (50, 200)
    if char == "G":
        return (50, 230)
    if char == "H":
        return (50, 200)
    if char == "I":
        return (50, 200)
    if char == "J":
        return (30, 140)
    if char == "K":
        return (50, 200)
    if char == "L":
        return (50, 220)
    if char == "M":
        return (50, 260)
    if char == "N":
        return (50, 220)
    if char == "O":
        return (50, 200)
    if char == "P":
        return (50, 150)
    if char == "Q":
        return (50, 230)
    if char == "R":
        return (50, 180)
    if char == "S":
        return (50, 180)
    if char == "T":
        return (50, 180)
    if char == "U":
        return (50, 190)
    if char == "V":
        return (50, 160)
    if char == "W":
        return (50, 250)
    if char == "X":
        return (40, 210)
    if char == "Y":
        return (50, 160)
    if char == "Z":
        return (50, 350)
    if char == "period":
        return (250, 60)
    if char == "comma":
        return (250, 60)
    if char == "apostrophe":
        return (50, 50)
    if char == "question":
        return (50, 50)
    if char == "exclamation":
        return (50, 100)
    else: return (0,150)


fancy_chars = {".":"period", ",":"comma", "'":"apostrophe", "?":"question", "!":"exclamation"}
print("SP1;")
for char in input_string:
    nice_char = char
    if char in fancy_chars.keys():
        nice_char = fancy_chars[char]
    if char == "\n" or (y_pos > 6000 and char == " "):
        (x_pos, y_pos) = (x_pos + 300 * font_size, 300)
    if char == " ":
        print("PU;");
        print("PA" + str(int(x_pos)) + "," + str(int(y_pos + get_adjust(char)[1] * font_size)) + ";") 
    elif char != "\n":
        with open("letter-files-real/" + str(nice_char) + ".hpgl") as char_data:
            for line in char_data.readlines():
                if line[:2] == "PA":
                    coords = line[2:].strip(";\n").split(",")
                    adjust_2 = 0
                    if nice_char == "apostrophe":
                        adjust_2 = 100
                    if nice_char == "period" or nice_char == "comma":
                        adjust_2 = 50
                    if nice_char == "exclamation" or nice_char == "question":
                        adjust_2 = 60
                    print("PA" + str(int(int(coords[0]) * font_size + x_pos + get_adjust(nice_char)[0] * font_size)) + "," + str(int(int(coords[1]) * font_size + y_pos + adjust_2 * font_size)) + ";")
                elif line[:2] != "SP":
                    print(line.strip("\n"))



    if char != "\n":
        y_pos += get_adjust(nice_char)[1] * font_size
