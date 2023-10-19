import numpy as np
from scipy.optimize import minimize
from src import constants


class MultilaterationTOF:
    def __init__(self, anchor_network):
        self.anchor_ids = anchor_network.get_anchor_ids()
        self.anchor_positions = np.array([anchor_network.get_anchor_position(id) for id in self.anchor_ids])

    def calculate_position(self, tof_measurements):
        # based on https://github.com/glucee/Multilateration/tree/master

        distances_to_station = np.array([tof_measurements[id] * constants.SPEED_OF_LIGHT for id in self.anchor_ids])

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

        return result.x

        