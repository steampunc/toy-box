from PIL import Image

im = Image.open('here.png') 
pix = im.load()
(width, height) = im.size

def drawsquare(x, y, size, darkness):
    if darkness > 0.01: 
        print("PA" + str(int(x + size/2)) + "," + str(int(y + size/2)) + ";") 
        print("PD;")
        print("PA" + str(int(x - size/2)) + "," + str(int(y + size/2)) + ";") 
        if darkness > 0.25:
            print("PA" + str(int(x - size/2)) + "," + str(int(y - size/2)) + ";") 
            if darkness > 0.5:
                print("PA" + str(int(x + size/2)) + "," + str(int(y - size/2)) + ";") 
                if darkness > 0.9:
                    print("PA" + str(int(x + size/2)) + "," + str(int(y + size/2)) + ";") 
        print("PU;")


#page dimensions are 10300x7650

#20 bits per pixel

print("PU;")
for i in range(2):
    print("SP" + str(i + 1) + ";") # 1 = red, 2 = green, 3 = blue
    for x in range(0, width):
        for y in range(0, height):
            darkness = 255 - pix[x,y][i]
            drawsquare(x * int(10300/width) + i * (10300*0.1/width), y * int(7650/height) + i * (7650*0.1/height), (10300/(3*width)), darkness / 255)


