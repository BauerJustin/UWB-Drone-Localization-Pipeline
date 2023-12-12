import numpy as np
from scipy.optimize import minimize
from src.utils import Position
from src import constants as const


class Multilateration:
    def __init__(self, anchor_network):
        self.anchor_ids = anchor_network.get_anchor_ids()
        self.anchor_positions = np.array([anchor_network.get_anchor_pos(id).unpack() for id in self.anchor_ids])

    def calculate_position(self, measurements, timestamp, last_pos=None):
        # based on https://github.com/glucee/Multilateration

        distances_to_station = np.array([measurements[id] for id in self.anchor_ids])

        l = len(self.anchor_positions)
        S = sum(distances_to_station)
    
        # Compute the weight vector for the initial guess
        W = ((l - 1) * S) / (S - distances_to_station)
        
        # Calculate the initial guess of the point location
        if const.USE_LAST_POS and last_pos:
            x0 = np.array(last_pos.unpack())
        else:
            x0 = np.dot(W, self.anchor_positions)
        
        # Define the error function for optimization
        def error(x, anchor_positions, distances_to_station):
            return np.sum((np.linalg.norm(anchor_positions - x, axis=1) - distances_to_station) ** 2)
        
        # Optimize the distance from the signal origin to the border of spheres
        result = minimize(error, x0, args=(self.anchor_positions, distances_to_station), method='Nelder-Mead')

        return Position(*result.x, t=timestamp)
