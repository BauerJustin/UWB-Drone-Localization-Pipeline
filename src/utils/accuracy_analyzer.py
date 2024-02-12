from src import constants as const
from src.utils import Position, load_config
import math
import matplotlib.pyplot as plt
import numpy as np

class AccuracyAnalyzer:
    def __init__(self, tracker, static=False, linear=False, plot_on=True):
        assert static ^ linear, "Error: static xor linear must be met"
        self.tracker = tracker
        self.static = static
        self.linear = linear
        self.plot_on = plot_on
        self.ground_truth = load_config.load_ground_truth()

    def evaluate_accuracy(self):
        if self.static:
            self._evaluate_static_accuracy()
        elif self.linear:
            self._evaluate_linear_accuracy()
        else:
            raise Exception("Invalid mode")
        
    def _evaluate_static_accuracy(self):
        drone_metrics = {}
        for drone_id, history in self.tracker.drones_history.items():
            ground_truth = Position(*self.ground_truth['static'][drone_id])
            errors, times = [], []
            for pos in history:
                error = self._get_euclid_dist(pos, ground_truth) * 100  # convert to cm
                errors.append(error)
                times.append(pos.t)
            
            mean = np.mean(errors)
            std = np.std(errors)
            print(f'{drone_id}: Error mean: {mean}, Error std: {std}')
            
            drone_metrics[drone_id] = {
                'errors': errors,
                'times': times
            }

        if self.plot_on:
            self._plot_metrics(drone_metrics)

    def _evaluate_linear_accuracy(self):
        drone_metrics = {}
        for drone_id, history in self.tracker.drones_history.items():
            start_point = np.array(self.ground_truth['linear'][drone_id][0])
            end_point = np.array(self.ground_truth['linear'][drone_id][1])

            errors, times = [], []
            for pos in history:
                closest_point = self._get_closest_point_on_line_segment(start_point, end_point, np.array(pos.unpack()))
                error = self._get_euclid_dist(pos, closest_point) * 100  # convert to cm
                errors.append(error)
                times.append(pos.t)

            mean = np.mean(errors)
            std = np.std(errors)

            print(f'{drone_id}: Error mean: {mean}, Error std: {std}')

            drone_metrics[drone_id] = {
                'errors': errors,
                'times': times
            }

        if self.plot_on:
            self._plot_metrics(drone_metrics)

    def _get_euclid_dist(self, pos, ground_truth):
        return math.sqrt((pos.x - ground_truth.x)**2 + (pos.y - ground_truth.y)**2 + (pos.z - ground_truth.z)**2)

    def _get_closest_point_on_line_segment(self, start_point, end_point, pos):
        line_dir = end_point - start_point
        t = np.dot(pos - start_point, line_dir) / np.dot(line_dir, line_dir)
        t = max(0, min(1, t))
        closest_point = start_point + t * line_dir
        return Position(*closest_point)
    
    def _plot_metrics(self, drone_metrics):
        plt.figure()
        for drone_id, data in drone_metrics.items():
            errors = data['errors']
            times = data['times']
            plt.plot(times, errors, label=f'{drone_id}')
        plt.xlabel('Time')
        plt.ylabel('Error [cm]')
        plt.title(f'Error Plot')
        plt.legend()
        plt.show()
