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

    unprofiled_goal = DrivetrainGoals()
    unprofiled_goal.position = 0.0
    unprofiled_goal.v_s = 0.0
    unprofiled_goal.v_e = 0.0
    unprofiled_goal.angle = 0.0
    unprofiled_goal.angular_velocity = 0.0

    profiled_goal = DrivetrainGoals()
    profiled_goal.position = 0.0
    profiled_goal.velocity = 0.0
    profiled_goal.angle = 0.0
    profiled_goal.angular_velocity = 0.0

    max_accel = 0.0
    max_velocity = 0.0

    left_voltage = 0
    right_voltage = 0

    def __init__(self, pkP, pkI, pkD, akP, akI, akD, max_accel, max_velocity, dt):
        self.pkP = pkP
        self.pkI = pkI
        self.pkD = pkD

        self.akP = akP
        self.akI = akI
        self.akD = akD

        self.max_accel = max_accel
        self.max_velocity = max_velocity

        self.dt = dt

    def UpdateGoal(self, time):
        if (time < self.t_accel):
            self.profiled_goal.velocity += self.max_accel * self.dt
        elif (self.t_cruise > 0 and time < self.t_accel + self.t_cruise):
            self.profiled_goal.velocity = self.max_velocity
        elif (time < self.t_accel + self.t_cruise + self.t_deccel or self.profiled_goal.velocity > self.unprofiled_goal.v_e):
            self.profiled_goal.velocity -= self.max_accel * self.dt

        self.profiled_goal.position += self.profiled_goal.velocity * self.dt

    def Update(self, status):

        self.UpdateGoal(self.time)

        self.left_voltage = (self.profiled_goal.position - status.position) * self.pkP + (self.profiled_goal.velocity - status.velocity) * self.pkD
        self.right_voltage = (self.profiled_goal.position - status.position) * self.pkP + (self.profiled_goal.velocity - status.velocity) * self.pkD

        print(self.left_voltage, self.right_voltage, self.time)
        self.time += self.dt
        return self.left_voltage, self.right_voltage

    def SetGoal(self, goal):
        self.unprofiled_goal.position = goal.position
        self.unprofiled_goal.v_s = goal.v_s
        self.unprofiled_goal.v_e = goal.v_e

        self.profiled_goal.position = 0.0
        self.profiled_goal.velocity = goal.v_s

        # Calculate constants
        self.v_c = min(self.max_velocity, math.sqrt(((2.0 * self.unprofiled_goal.position * self.max_accel) - (self.unprofiled_goal.v_s * self.unprofiled_goal.v_s + self.unprofiled_goal.v_e * self.unprofiled_goal.v_e)) / 2.0))

        self.t_accel = (self.v_c - goal.v_s) / self.max_accel
        self.t_deccel = (self.v_c - goal.v_e) / self.max_accel
        self.t_cruise = (self.unprofiled_goal.position - ((self.v_c + self.unprofiled_goal.v_s) / 2 * self.t_accel + (self.v_c + self.unprofiled_goal.v_e) / 2 * self.t_deccel)) / self.v_c

        self.time = 0

    def log_status(self):
        with open("logs/profiled_controller_status.csv", "a") as logfile:
            logfile.write(str(self.left_voltage) + ", " + str(self.right_voltage) + ", " + str(self.unprofiled_goal.position) + ", " + str(self.unprofiled_goal.v_s) + ", " + str(self.v_c) + ", " + str(self.unprofiled_goal.v_e) + ", " + str(self.profiled_goal.position) + ", " + str(self.profiled_goal.velocity) + "\n")




time = 10

model = dt_model.DrivetrainModel()

controller = TrapController(0, 0, 0, 0, 0, 0, 1.0, 1.0, dt_model.constants.dt)

goal = DrivetrainGoals()

goal.position = 4
goal.v_s = 0
goal.v_e = 0

controller.SetGoal(goal)

with open("logs/profiled_controller_status.csv", "a") as logfile:
    logfile.write("Left Voltage, Right Voltage, Unprofiled Goal Position, Unprofiled Goal Velocity Start, Unprofiled Goal Velocity Cruise, Unprofiled Goal Velocity End, Profiled Goal Position, Profiled Goal Velocity\n")

for i in range(0, int(time / dt_model.constants.dt)):
    status = model.get_status()
    left_voltage, right_voltage = controller.Update(status)

    model.Update(left_voltage, right_voltage)

    model.log_status()
    controller.log_status()

