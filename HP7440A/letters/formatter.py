
letters = ["period"]  
print(letters)
font_size = 0.5;

for char in letters:
    with open("letter-files-unformatted/" + str(char) + ".hpgl") as hpgl_file:
        with open("letter-files/" + str(char) + ".hpgl", "w+") as final_file:
            command_parts = hpgl_file.read().strip().split(";")
            for command_part in command_parts:
                if command_part == "IN":
                    final_file.write("IN;\n")
                elif command_part[:2] == "SP":
                    final_file.write(command_part + ";\n")
                elif command_part[:2] == "PU":
                    final_file.write("PU;\n")
                elif command_part[:2] == "PD":
                    final_file.write("PD;\n")
                coordinates = command_part[2:].split(",")
                if len(coordinates) > 1:
                    for i in range(0, len(coordinates), 2):
                        final_file.write("PA" + str(int(float(coordinates[i]) * font_size * 0.5)) + "," + str(int(float(coordinates[i+1]) * font_size * 0.5)) + ";\n")



