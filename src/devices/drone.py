import copy
import math
import time
from src.algorithms import Multilateration, Filter, Buffer
from src.utils import Position
from src import constants as const


class Drone:
    def __init__(self, id, anchor_network):
        self.id = id
        self.anchor_network = anchor_network

        self.multilaterator = Multilateration(anchor_network=self.anchor_network)
        if const.FILTER_ENABLED:
            self.filter = Filter(filter_type=const.FILTER_TYPE)
        if const.BUFFER_ENABLED:
            self.buffer = Buffer(base_type=const.BASE, size=const.BUFFER_SIZE, filter_outliers=const.BUFFER_FILTER_OUTLIERS)
        if const.MEASURE_VARIANCE:
            self.variance_buffer = Buffer(base_type="pos", size=const.VARIANCE_SIZE)

        self.has_ground_truth, self.ground_truth = None, None

        self.last_update_time = None
        self.update_count = 0
        self.update_frequency = 0

        self.variance = None

        self.active = False

    def update_pos(self, measurements, ground_truth):
        if const.BASE == 'pos':
            self._update_pos_base(measurements)
        elif const.BASE == 'measurement':
            self._update_measurement_base(measurements)
        else:
            raise Exception(f"Invalid base: {const.BASE}")

        if ground_truth:
            self.has_ground_truth = True
            self.ground_truth = Position(**ground_truth)

    def _update_measurement_base(self, measurements):
        if const.BUFFER_ENABLED:
            measurements = self._update_buffer(measurements)
            if measurements is None:
                return
            
        if not const.FILTER_ENABLED or not self.active:
            self.measurements = measurements
        else:
            self.filter.update(self.measurements, measurements)
        
        self.pos = self.multilaterator.calculate_position(self.measurements, last_pos=self.pos if self.active else None)

        self._update_stats()

    def _update_pos_base(self, measurements):
        new_pos = self.multilaterator.calculate_position(measurements, last_pos=self.pos if self.active else None)

        if const.BUFFER_ENABLED:
            new_pos = self._update_buffer(new_pos)
            if new_pos is None:
                return

        if not const.FILTER_ENABLED or not self.active:
            self.pos = new_pos
        else:
            self.filter.update(self.pos, new_pos)

        self._update_stats()

    def get_pos(self):
        return self.pos

    def get_update_frequency(self):
        return self.update_frequency
    
    def get_variance(self):
        return self.variance

    def get_ground_truth(self):
        return self.ground_truth
    
    def get_euclid_dist(self):
        return math.sqrt((self.pos.x - self.ground_truth.x)**2 + (self.pos.y - self.ground_truth.y)**2 + (self.pos.z - self.ground_truth.z)**2)
    
    def _update_buffer(self, value):
        self.buffer.add(value)
        if const.BUFFER_MODE == 'avg':
            new_value = self.buffer.get_avg()
        elif const.BUFFER_MODE == 'last':
            new_value = self.buffer.get_last()
        else:
            raise Exception(f"Invalid buffer mode: {const.BUFFER_MODE}")
        return new_value
    
    def _update_stats(self):
        self._update_variance()
        self._update_frequency()
        self.active = self.update_count > const.FIRST_UPDATES_SKIPPED

    def _update_frequency(self):
        current_time = time.time()
        if self.last_update_time is not None:
            time_interval = current_time - self.last_update_time
            self.update_frequency = 1 / time_interval

        self.last_update_time = current_time
        self.update_count += 1

    def _update_variance(self):
        self.variance_buffer.add(copy.copy(self.pos))
        self.variance = self.variance_buffer.get_buffer_variance()
        