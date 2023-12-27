from src import constants as const
from src.utils import load_config

kf_settings = load_config.load_kf_settings(const.BASE, const.FILTER_TYPE)

class Measurements:
    def __init__(self, d1, d2, d3, d4, d1_dot=0.0, d2_dot=0.0, d3_dot=0.0, d4_dot=0.0, covariance=kf_settings['INITIAL_COVARIANCE'], t=None):
        self.d1 = d1
        self.d2 = d2
        self.d3 = d3
        self.d4 = d4
        self.d1_dot = d1_dot
        self.d2_dot = d2_dot
        self.d3_dot = d3_dot
        self.d4_dot = d4_dot
        self.covariance = covariance
        self.t = t

    def unpack(self):
        return self.d1, self.d2, self.d3, self.d4
    
    def state(self):
        return self.d1, self.d2, self.d3, self.d4, self.d1_dot, self.d2_dot, self.d3_dot, self.d4_dot
    
    def update(self,d1, d2, d3, d4, d1_dot=None, d2_dot=None, d3_dot=None, d4_dot=None, covariance=None, t=None):
        self.d1 = d1
        self.d2 = d2
        self.d3 = d3
        self.d4 = d4
        if d1_dot is not None:
            self.d1_dot = d1_dot
        if d2_dot is not None:
            self.d2_dot = d2_dot
        if d3_dot is not None:
            self.d3_dot = d3_dot
        if d4_dot is not None:
            self.d4_dot = d4_dot
        if covariance is not None:
            self.covariance = covariance
        if t is not None:
            self.t = t
