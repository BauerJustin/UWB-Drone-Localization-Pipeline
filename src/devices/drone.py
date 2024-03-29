import copy
import math
import time
from src.algorithms import Multilateration, Filter, Buffer, OutlierRejection
from src.utils import Position, load_config
from src import constants as const


class Drone:
    def __init__(self, id, anchor_network):
        self.id = id
        self.anchor_network = anchor_network

        self.multilaterator = Multilateration(anchor_network=self.anchor_network)
        self.filter = Filter(filter_type=const.FILTER_TYPE)
        if const.MEASURE_VARIANCE:
            self.variance_buffer = Buffer(base_type="pos", size=const.VARIANCE_SIZE)
        if const.OUTLIER_REJECTION_ENABLED:
            self.outlier_rejection = OutlierRejection(const.OUTLIER_INTERPOLATION_ENABLED)

        self.has_ground_truth, self.ground_truth = None, None

        self.last_update_time = None
        self.update_frequency = 0
        self.update_frequencies = []
        self.variance = None
        self.active = False

        self.pos = None

        self.logger = load_config.setup_logger(__name__)

    def update_pos(self, measurements, ground_truth):
        self.logger.info(f'\n***DRONE {self.id}***')
        self.logger.info(f'Incoming measurement: {measurements.unpack()}')

        if const.OUTLIER_REJECTION_ENABLED:
            measurements = self.outlier_rejection.filter_outlier(measurements)
            if measurements is None:
                return

        if not self.active:
            self.measurements = measurements
            if None not in self.measurements.unpack():
                self.active = True
        else:
            self.filter.update(self.measurements, measurements)
        self.logger.info(f'*New Measurement: {self.measurements.unpack()}')

        if const.OUTLIER_INTERPOLATION_ENABLED and self.active:
            self.outlier_rejection.add_to_buffer(self.measurements)

        if self.active:
            self.pos = self.multilaterator.calculate_position(self.measurements, last_pos=self.pos)
            self.logger.info(f'*New Pos: {self.pos.unpack()}')

        self._update_stats()

        if ground_truth:
            self.has_ground_truth = True
            self.ground_truth = Position(**ground_truth)

    def get_pos(self):
        return self.pos

    def get_update_frequency(self):
        if const.UPDATE_FREQ_AVG and len(self.update_frequencies) > 0:
            return sum(self.update_frequencies) / len(self.update_frequencies)
        else:
            return self.update_frequency
    
    def get_variance(self):
        return self.variance

    def get_ground_truth(self):
        return self.ground_truth
    
    def get_euclid_dist(self):
        if self.pos is not None and self.ground_truth is not None:
            return math.sqrt((self.pos.x - self.ground_truth.x)**2 + (self.pos.y - self.ground_truth.y)**2 + (self.pos.z - self.ground_truth.z)**2)
        return None
    
    def _update_stats(self):
        if self.active:
            self._update_variance()
        self._update_frequency()

    def _update_frequency(self):
        current_time = time.time()
        if self.last_update_time is not None:
            time_interval = current_time - self.last_update_time
            if const.PRINT_TIME_INTERVALS:
                print(f"[Drone-{self.id}] Time interval: {time_interval}")
            self.update_frequency = 1 / time_interval
            self.update_frequencies.append(self.update_frequency)
            if len(self.update_frequencies) > const.UPDATE_FREQ_BUFFER_SIZE:
                self.update_frequencies.pop(0)

        self.last_update_time = current_time

    def _update_variance(self):
        self.variance_buffer.add(copy.copy(self.pos))
        self.variance = self.variance_buffer.get_variance()
