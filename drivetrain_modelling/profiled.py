import math
import model as dt_model

class DrivetrainGoals(object):
    pass

class TrapController(object):
    pkP = 0.0
    pkI = 0.0
    pkD = 0.0
    
    akP = 0.0
    akI = 0.0
    akD = 0.0

    goal = DrivetrainGoals()
    goal.unprofiled_position = 0.0
    goal.unprofiled_velocity = 0.0
    goal.unprofiled_angle = 0.0
    goal.unprofiled_angular_velocity = 0.0

    goal.profiled_position = 0.0
    goal.profiled_velocity = 0.0
    goal.profiled_angle = 0.0
    goal.profiled_angular_velocity = 0.0

    accel_time = 0.0

    max_accel = 0.0
    max_velocity = 0.0

    def __init__(self, pkP, pkI, pkD, akP, akI, akD, max_accel, max_velocity):
        self.pkP = pkP
        self.pkI = pkI
        self.pkD = pkD

        self.akP = akP
        self.akI = akI
        self.akD = akD

        self.max_accel = max_accel
        self.accel_time = max_velocity / max_accel

        self.max_velocity = max_velocity

    def Update(self, status):
        left_voltage = (self.goal.profiled_position - status.position) * self.pkP + (self.goal.profiled_velocity - status.velocity) * self.pkD + (self.goal.profiled_angle - status.angle) * self.akP + (self.goal.profiled_angular_velocity - status.angular_velocity) * self.akD
        right_voltage = (self.goal.profiled_position - status.position) * self.pkP + (self.goal.profiled_velocity - status.velocity) * self.pkD - (self.goal.profiled_angle - status.angle) * self.akP - (self.goal.profiled_angular_velocity - status.angular_velocity) * self.akD
        print(left_voltage, right_voltage, self.goal.position - status.position)
        return left_voltage, right_voltage

    def SetGoal(self, goal):
        self.goal.unprofiled_position = goal.unprofiled_position
        self.goal.unprofiled_velocity = goal.unprofiled_velocity
        self.goal.unprofiled_angle = goal.unprofiled_angle
        self.goal.unprofiled_angular_velocity = goal.unprofiled_angular_velocity

        # Calculate constants
        v_cruise = math.Min(max_velocity, v_cruise


    def UpdateGoal(self, controller_time):


time = 10

model = dt_model.DrivetrainModel()
controller = TrapController(0, 0, 0, 0, 0, 0, 1, 1)
goal = DrivetrainGoals()
goal.unprofiled_position = 0.75
goal.unprofiled_velocity = 0.0
goal.unprofiled_angle = -math.pi / 2
goal.unprofiled_angular_velocity = 0.0

controller.SetGoal(goal)

with open("logs/controller_status.csv", "a") as logfile:
    logfile.write("Left Voltage, Right Voltage, Goal Position, Goal Velocity, Goal Angle, Goal Angular Velocity\n")

for i in range(0, int(time / dt_model.constants.dt)):
    status = model.get_status()
    left_voltage, right_voltage = controller.Update(status)

    model.Update(left_voltage, right_voltage)

    model.log_status()

    with open("logs/unprofiled_controller_status.csv", "a") as logfile:
        logfile.write(str(left_voltage) + ", " + str(right_voltage) + ", " + str(goal.position) + ", " + str(goal.velocity) + ", " + str(goal.angle) + ", " + str(goal.angular_velocity) + "\n")
