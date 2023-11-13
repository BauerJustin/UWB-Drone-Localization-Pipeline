import math
import time
from src.algorithms import Multilateration, Filter
from src.utils import Position
from src import constants as const
import numpy as np

class Drone:
    def __init__(self, id, anchor_network):
        self.id = id
        self.anchor_network = anchor_network

        self.multilaterator = Multilateration(anchor_network=self.anchor_network)
        if const.FILTER_ENABLED:
            self.filter = Filter(filter_type=const.FILTER_TYPE)

        self.has_ground_truth, self.ground_truth = None, None

        self.last_update_time = None
        self.update_count = 0
        self.update_frequency = 0

        self.active = False

    def update_pos(self, buffered_measurements, ground_truth):
        new_pos = self.multilaterator.calculate_position_buffered_measurements(buffered_measurements=buffered_measurements)
        if not const.FILTER_ENABLED or not hasattr(self, "pos"):
            self.pos = new_pos
        else:
            self.filter.update_pos(self.pos, new_pos)
        if ground_truth:
            self.has_ground_truth = True
            self.ground_truth = Position(**ground_truth)
        self._update_frequency()
        self.active = True
        
    def get_pos(self):
        return self.pos

    def get_update_frequency(self):
        return self.update_frequency

    def get_ground_truth(self):
        return self.ground_truth
    
    def get_euclid_dist(self):
        return math.sqrt((self.pos.x - self.ground_truth.x)**2 + (self.pos.y - self.ground_truth.y)**2 + (self.pos.z - self.ground_truth.z)**2)

    def _update_frequency(self):
        current_time = time.time()
        if self.last_update_time is not None:
            time_interval = current_time - self.last_update_time
            self.update_frequency = 1 / time_interval

        self.last_update_time = current_time
        self.update_count += 1
