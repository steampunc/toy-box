
letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVXWYZ"  

for char in letters:
    with open("cursive-letters/" + str(char) + ".hpgl") as hpgl_file:
        with open("letter-files-real/" + str(char) + ".hpgl", "w+") as final_file:
            i = 0
            for line in hpgl_file.readlines():
                if i % 2 and "SP" not in line or "PU" in line or "PD" in line:
                    final_file.write(line)
                i = i + 1
