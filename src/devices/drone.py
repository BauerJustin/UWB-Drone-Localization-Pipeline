import math
from src.algorithms import Multilateration, Filter
from src.utils import Position
from src import constants as const

class Drone:
    def __init__(self, id, anchor_network):
        self.id = id
        self.anchor_network = anchor_network

        self.multilaterator = Multilateration(anchor_network=self.anchor_network)
        self.filter = Filter(filter_type=const.FILTER_TYPE)

        self.has_ground_truth, self.ground_truth = None, None

    def update_pos(self, measurements, ground_truth):
        new_pos = self.multilaterator.calculate_position(measurements=measurements)
        if not hasattr(self, "pos"):
            self.pos = new_pos
        self.filter.update_pos(self.pos, new_pos)
        if ground_truth:
            self.has_ground_truth = True
            self.ground_truth = Position(**ground_truth)

    def get_pos(self):
        return self.pos

    def get_ground_truth(self):
        return self.ground_truth
    
    def get_euclid_dist(self):
        return math.sqrt((self.pos.x - self.ground_truth.x)**2 + (self.pos.y - self.ground_truth.y)**2 + (self.pos.z - self.ground_truth.z)**2)
