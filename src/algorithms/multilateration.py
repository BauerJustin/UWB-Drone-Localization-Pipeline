import numpy as np
from scipy.optimize import minimize
from src.utils import Position
from scipy.spatial.distance import mahalanobis


class Multilateration:
    def __init__(self, anchor_network):
        self.anchor_ids = anchor_network.get_anchor_ids()
        self.anchor_positions = np.array([anchor_network.get_anchor_pos(id).unpack() for id in self.anchor_ids])

    def _calculate_position_single_set(self, measurements):
        # based on https://github.com/glucee/Multilateration

        distances_to_station = np.array([measurements[id] for id in self.anchor_ids])

        l = len(self.anchor_positions)
        S = sum(distances_to_station)
    
        # Compute the weight vector for the initial guess
        W = ((l - 1) * S) / (S - distances_to_station)
        
        # Calculate the initial guess of the point location
        x0 = np.dot(W, self.anchor_positions)
        
        # Define the error function for optimization
        def error(x, anchor_positions, distances_to_station):
            return np.sum((np.linalg.norm(anchor_positions - x, axis=1) - distances_to_station) ** 2)
        
        # Optimize the distance from the signal origin to the border of spheres
        result = minimize(error, x0, args=(self.anchor_positions, distances_to_station), method='Nelder-Mead')

        return Position(*result.x)

    def _filter_outliers(self, buffer):
        if not buffer:
            return []

        median = np.median(buffer)
        deviation = np.median([abs(x - median) for x in buffer])
        threshold = 3 * deviation
        return [x for x in buffer if abs(x - median) <= threshold]
    
    def calculate_position_buffered_measurements(self, buffered_measurements):
        filtered_measurements = {anchor_id: self._filter_outliers(buffered_measurements[anchor_id]) for anchor_id in buffered_measurements}

        all_positions = []

        # Iterate over each set of measurements in the buffer
        for measurements in zip(*filtered_measurements.values()):
            measurement_dict = dict(zip(self.anchor_ids, measurements))
            position = self._calculate_position_single_set(measurement_dict)
            all_positions.append(position)

        # Convert all_positions to a 2D NumPy array for averaging
        positions_array = np.array([p.unpack() for p in all_positions])

        # Average the calculated positions
        avg_position = np.mean(positions_array, axis=0)
        return Position(*avg_position)