class constants(object):
    dt = 0.005

    wheel_radius = 0.03
    robot_radius = 0.25

    stall_current = 133
    stall_torque = 2.42
    torque_constant = stall_torque / stall_current
    back_emf_constant = torque_constant
    
    gear_ratio = 1.0 / 7.0
    resistance = 12.0 / stall_current
    moment_of_intertia = 120.0 * (0.4 * 0.4 + 0.35 * 0.35) / 12.0

class DrivetrainStatus(object):
    pass

class DrivetrainModel(object):
    status = DrivetrainStatus()
    def __init__(self):
        self.status.left_position = 0.0
        self.status.right_position = 0.0

        self.status.left_velocity = 0.0
        self.status.right_velocity = 0.0
        self.status.left_angular_velocity = 0.0
        self.status.right_angular_velocity = 0.0

        self.status.velocity = 0.0
        self.status.position = 0.0
    
        self.status.angle = 0.0
        self.status.angular_velocity = 0.0

        with open("logs/model_status.csv", "a") as logfile:
            logfile.write("Left Position, Right Position, Left Velocity, Right Velocity, Left Angular Velocity, Right Angular Velocity, Position, Velocity, Angle, Angular Velocity\n")

    def Update(self, left_voltage, right_voltage):

        status = self.status

        left_angular_accel = (constants.torque_constant / (constants.moment_of_intertia * constants.resistance * constants.gear_ratio)) * left_voltage - (constants.torque_constant * constants.back_emf_constant / (constants.moment_of_intertia * constants.resistance * constants.gear_ratio * constants.gear_ratio)) * status.left_angular_velocity

        right_angular_accel = (constants.torque_constant / (constants.moment_of_intertia * constants.resistance * constants.gear_ratio)) * right_voltage - (constants.torque_constant * constants.back_emf_constant / (constants.moment_of_intertia * constants.resistance * constants.gear_ratio * constants.gear_ratio)) * status.right_angular_velocity

        status.left_angular_velocity += left_angular_accel * constants.dt
        status.right_angular_velocity += right_angular_accel * constants.dt

        status.left_velocity = status.left_angular_velocity * constants.wheel_radius
        status.right_velocity = status.right_angular_velocity * constants.wheel_radius

        status.left_position += status.left_velocity * constants.dt
        status.right_position += status.right_velocity * constants.dt

        status.velocity = (status.left_velocity + status.right_velocity) / 2
        status.position += status.velocity * constants.dt

        status.angular_velocity = (status.left_velocity - status.right_velocity) / constants.robot_radius
        status.angle += status.angular_velocity * constants.dt

        self.status = status

    def Reset(self):
        self.status.left_position = 0.0
        self.status.right_position = 0.0
        self.status.position = 0.0

        self.status.left_velocity = 0.0
        self.status.right_velocity = 0.0
        self.status.left_angular_velocity = 0.0
        self.status.right_angular_velocity = 0.0
    
        self.status.angle = 0.0
        self.status.angular_velocity = 0.0

    def get_status(self):
        return self.status

    def log_status(self):
        status = self.status
        with open("logs/model_status.csv", "a") as logfile:
            logfile.write(str(status.left_position) + ", " + str(status.right_position) + ", " + str(status.left_velocity) + ", " + str(status.right_velocity) + ", " + str(status.left_angular_velocity) + ", " + str(status.right_angular_velocity) + ", " + str(status.position) + ", " + str(status.velocity) + ", " + str(status.angle) + ", " + str(status.angular_velocity) + "\n")


