import sys
import select
import tty
import termios
import math
import time
import random
from serial import Serial

ser = Serial(sys.argv[1])

def send_commands(commands):
    next_command = []
    chunks = []
    for command in commands:
        if len(("".join(next_command)).encode("utf-8")) + len(command.encode("utf-8")) < 56:
            next_command.append(command)
        else:
            chunks.append(("".join(next_command).encode("utf-8")))
            next_command = [command]

    chunks.append("".join(next_command).encode("utf-8"))
    for chunk in chunks:
        print(chunk.encode("utf-8"))
        ser.write(chunk.encode("utf-8"))
        ser.write("OA;".encode("utf-8"))
        response = ""
        while response != "\r":
            response = ser.read()
        

height = 7650
width = 10300

world_commands = []

world_commands.append("SP1;")

world = []

floor_dist = 2000

def create_arc(x, y, radius, initial_angle, d_angle):
    world_commands.append("PU;")
    resolution = 20
    world_commands.append("PA" + str(int(x + radius * math.cos(initial_angle))) + "," + str(int(y + radius * math.sin(initial_angle))) + ";")
    world_commands.append("PD;")
    for i in range(0, resolution):
        world_commands.append("PA" + str(int(x + radius * math.cos(d_angle * (i + 1) / resolution + initial_angle))) + "," + str(int(y + radius * math.sin(d_angle * (i + 1) / resolution + initial_angle))) + ";")

def draw_line(xi, yi, xf, yf):
    world_commands.append("PU;")
    world_commands.append("PA" + str(int(xi)) + "," + str(int(yi)) + ";")
    world_commands.append("PD;")
    world_commands.append("PA" + str(int(xf)) + "," + str(int(yf)) + ";")

class Obstacle:
    def __init__(self, angle, obs_height):
        self.angle = angle
        self.delta_angle = 0.1 * math.pi
        self.height = obs_height
    def check_collision(self, angle, radius):
        return (angle % (2 * math.pi) > self.angle) and (angle % (2 * math.pi) < self.angle + self.delta_angle) and (radius < self.height)
    def draw(self):
        initial_angle = self.angle
        delta_angle = self.delta_angle
        draw_line(width/2 + floor_dist * math.cos(initial_angle), height / 2 + floor_dist * math.sin(initial_angle), width / 2 + self.height * math.cos(initial_angle), height / 2 + self.height * math.sin(initial_angle))
        create_arc(width/2, height/2, self.height, initial_angle, delta_angle)
        initial_angle = initial_angle + delta_angle
        draw_line(width/2 + floor_dist * math.cos(initial_angle), height / 2 + floor_dist * math.sin(initial_angle), width / 2 + self.height * math.cos(initial_angle), height / 2 + self.height * math.sin(initial_angle))

class Cursor:
    def __init__(self):
        self.angle = 0
        self.d_angle = 0.14 * (1.0/3.0) * math.pi
        self.radius = 4000
        self.radial_velocity = 0
    def render(self):
        send_commands(["PA" + str(int(width/2 + self.radius * math.cos(self.angle))) + "," + str(int(height/2 + self.radius * math.sin(self.angle))) + ";"])
    def update(self, enter):
        if enter:
            self.radial_velocity = 450
        elif self.radius > 2300:
            self.radial_velocity -= 150
        else:
            self.radial_velocity = 0
            self.radius = 2300
        self.radius += self.radial_velocity
        self.angle += self.d_angle
        


create_arc(width / 2, height / 2, floor_dist, 0, 2 * math.pi)
num_obstacles = random.randint(3, 5)
obstacles = []
for i in range(0, num_obstacles):
    angle = i * 2 * math.pi / num_obstacles
    obstacles.append(Obstacle(angle, random.randint(floor_dist + 200, floor_dist + 1000)))
    obstacles[i].draw()

cursor = Cursor()

world_commands.append("SP2;")
send_commands(world_commands)

# Keyboard input

def playGame():
    def isData():
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())

        i = 0
        not_collided = True
        send_commands("PU;")
        cursor.render()

        send_commands("PD;")
        while not_collided:
            enter = False
            if isData():
                c = sys.stdin.read(1)
                print(c)
                if c == '\n':         
                    enter = True
            cursor.update(enter)
            cursor.render()
            for obstacle in obstacles:
                if obstacle.check_collision(cursor.angle, cursor.radius):
                    not_collided = False

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

i = 0
while i < 20:
    send_commands("PU;")
    cursor.radius = 4000
    cursor.angle = 0
    playGame()
    i += 1

