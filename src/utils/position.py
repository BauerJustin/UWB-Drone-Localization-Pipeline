from src import constants as const

class Position:
    def __init__(self, x=None, y=None, z=None, x_dot=0.0, y_dot=0.0, z_dot=0.0, covariance=const.INITIAL_COVARIANCE):
        self.x = x
        self.y = y
        self.z = z
        self.x_dot = x_dot
        self.y_dot = y_dot
        self.z_dot = z_dot
        self.covariance = covariance

    def unpack(self):
        return self.x, self.y, self.z
    
    def state(self):
        return self.x, self.y, self.z, self.x_dot, self.y_dot, self.z_dot
    
    def update(self, x, y, z, x_dot=None, y_dot=None, z_dot=None, covariance=None):
        self.x = x
        self.y = y
        self.z = z
        if x_dot is not None:
            self.x_dot = x_dot
        if y_dot is not None:
            self.y_dot = y_dot
        if z_dot is not None:
            self.z_dot = z_dot
        if covariance is not None:
            self.covariance = covariance
    