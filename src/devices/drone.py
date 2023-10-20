import math
from src.algorithms import Multilateration
from src import constants as const

class Drone:
    def __init__(self, id, anchor_network):
        self.id = id
        self.anchor_network = anchor_network
        self.x, self.y, self.z = None, None, None
        self.has_ground_truth, self.ground_truth = None, None
        self.multilaterator = Multilateration(anchor_network=self.anchor_network)

    def update_pos(self, measurements, ground_truth):
        new_x, new_y, new_z = self.multilaterator.calculate_position(measurements=measurements)
        if not const.MOVING_AVG_FILTER_ENABLED or self.x is None:
            self.x, self.y, self.z = new_x, new_y, new_z
        if const.MOVING_AVG_FILTER_ENABLED:
            self.x = self.x * (1 - const.MOVING_AVG_FILTER_RATE) + new_x * const.MOVING_AVG_FILTER_RATE
            self.y = self.y * (1 - const.MOVING_AVG_FILTER_RATE) + new_y * const.MOVING_AVG_FILTER_RATE
            self.z = self.z * (1 - const.MOVING_AVG_FILTER_RATE) + new_z * const.MOVING_AVG_FILTER_RATE
        if ground_truth:
            self.has_ground_truth = True
            self.ground_truth = tuple(ground_truth.values())

    def get_pos(self):
        return self.x, self.y, self.z

    def get_ground_truth(self):
        return self.ground_truth
    
    def get_euclid_dist(self):
        return math.sqrt((self.x - self.ground_truth[0])**2 + (self.y - self.ground_truth[1])**2 + (self.z - self.ground_truth[2])**2)
