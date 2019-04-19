import math

class Arc:
    def __init__(self, center_x, center_y, x_i, y_i, delta_angle):
        self.center_x = center_x
        self.center_y = center_y
        self.r = math.sqrt((center_x - x_i)**2 + (center_y - y_i)**2)
        self.theta = math.atan((y_i - center_y)/(x_i - center_x))
        self.delta_angle = delta_angle
        self.target_angle = self.theta + delta_angle

    def state(self):
        if abs(self.theta - self.target_angle) < abs(self.delta_angle / (2*self.r)):
            return "DONE"
        else:
            return "DRAWING"

    def draw(self):

        self.theta = self.theta + (self.delta_angle /(2*self.r))

        return (self.center_x + self.r*math.cos(self.theta), self.center_y + self.r * math.sin(self.theta))



