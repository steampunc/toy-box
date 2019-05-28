letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVXWYZ" 

for char in letters:
    with open("cursive-letters/" + str(char) + ".hpgl") as hpgl_file:
        with open("letter-files-real/" + str(char) + ".hpgl", "w+") as final_file:
            i = 0
            prev_line = ""
            for line in hpgl_file.readlines():
                if i % 2 == 0 and "SP" not in prev_line or "PD" in line or "PU" in prev_line or "PD" in prev_line:
                    final_file.write(prev_line)
                i = i + 1
                prev_line = line
