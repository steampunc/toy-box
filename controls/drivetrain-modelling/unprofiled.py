import math
import os
import model as dt_model

class DrivetrainGoals(object):
    pass

class UnprofiledController(object):
    pkP = 1.0
    pkI = 0.0
    pkD = 1.0
    
    akP = 0.0
    akI = 0.0
    akD = 0.0

    goal = DrivetrainGoals()
    goal.position = 0.0
    goal.velocity = 0.0
    goal.angle = 0.0
    goal.angular_velocity = 0.0

    def __init__(self, pkP, pkI, pkD, akP, akI, akD):
        self.pkP = pkP
        self.pkI = pkI
        self.pkD = pkD

        self.akP = akP
        self.akI = akI
        self.akD = akD

    def Update(self, status):
        left_voltage = (self.goal.position - status.position) * self.pkP + (self.goal.velocity - status.velocity) * self.pkD + (self.goal.angle - status.angle) * self.akP + (self.goal.angular_velocity - status.angular_velocity) * self.akD
        right_voltage = (self.goal.position - status.position) * self.pkP + (self.goal.velocity - status.velocity) * self.pkD - (self.goal.angle - status.angle) * self.akP - (self.goal.angular_velocity - status.angular_velocity) * self.akD
        print(left_voltage, right_voltage, self.goal.position - status.position)
        return left_voltage, right_voltage

    def SetGoal(self, goal):
        self.goal.position = goal.position
        self.goal.velocity = goal.velocity
        self.goal.angle = goal.angle
        self.goal.angular_velocity = goal.angular_velocity


os.remove("logs/controller_status.csv")
os.remove("logs/model_status.csv")
os.remove("logs/unprofiled_controller_status.csv")
time = 20

model = dt_model.DrivetrainModel()
controller = UnprofiledController(200, 0, 180, 10, 0, 15)
goal = DrivetrainGoals()
goal.position = 0.75
goal.velocity = 0.0
goal.angle = -math.pi / 2
goal.angular_velocity = 0.0

controller.SetGoal(goal)

with open("logs/controller_status.csv", "a") as logfile:
    logfile.write("Left Voltage, Right Voltage, Goal Position, Goal Velocity, Goal Angle, Goal Angular Velocity\n")


for i in range(0, int(time / dt_model.constants.dt)):
    status = model.get_status()
    left_voltage, right_voltage = controller.Update(status)
    if i == 1000:
        goal.position = 0.25
        goal.velocity = 0.0
        goal.angle = -math.pi / 2
        goal.angular_velocity = 0.0
        controller.SetGoal(goal)

    if i == 2000:
        goal.position = 1.5
        goal.velocity = 0.0
        goal.angle = 0
        goal.angular_velocity = 0.0
        controller.SetGoal(goal)

    if i == 3000:
        goal.position = -1
        goal.velocity = 0.0
        goal.angle = math.pi/2
        goal.angular_velocity = 0.0
        controller.SetGoal(goal)


    model.Update(left_voltage, right_voltage)

    model.log_status()

    with open("logs/unprofiled_controller_status.csv", "a") as logfile:
        logfile.write(str(left_voltage) + ", " + str(right_voltage) + ", " + str(goal.position) + ", " + str(goal.velocity) + ", " + str(goal.angle) + ", " + str(goal.angular_velocity) + "\n")
