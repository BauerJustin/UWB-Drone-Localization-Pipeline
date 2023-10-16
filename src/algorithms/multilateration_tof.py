import numpy as np
from scipy.optimize import least_squares
from src import constants


# TODO: Validate algorithm

class MultilaterationTOF:
    def __init__(self, anchor_network):
        self.anchor_network = anchor_network
        self.anchor_ids = anchor_network.get_anchor_ids()

    def calculate_position(self, tof_measurements, method="LinearLSE"):
        if method == "LinearLSE":
            return self._linear_LSE(tof_measurements)
        elif method == "IterativeLSE":
            return self._iterative_LSE(tof_measurements)
        else:
            raise ValueError(f"Invalid multilateration method: {method}")
    
    def _linear_LSE(self, tof_measurements):
        num_anchors = len(self.anchor_ids)

        # Ensure the number of ToF measurements matches the number of anchors
        if len(tof_measurements) != num_anchors:
            raise ValueError("Number of ToF measurements must match the number of anchors.")

        # Initialize matrices for the linear equation system
        A = np.zeros((num_anchors - 1, 3))
        b = np.zeros((num_anchors - 1, 1))

        # Calculate the difference in anchor coordinates and time differences
        for i in range(1, num_anchors):
            A[i - 1] = 2 * (np.array(self.anchor_network.get_anchor_position(self.anchor_ids[i])) - np.array(self.anchor_network.get_anchor_position(self.anchor_ids[0])))
            b[i - 1] = (tof_measurements[self.anchor_ids[0]] - tof_measurements[self.anchor_ids[i]]) * constants.SPEED_OF_LIGHT

        # Solve the linear equation system using the least squares method
        estimated_position, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

        x, y, z = estimated_position
        return x.item(), y.item(), z.item()

    def _iterative_LSE(self, tof_measurements, method="LSE"):
        if len(self.anchor_ids) != 4 or len(tof_measurements) != 4:
            raise ValueError("There must be 4 anchors and 4 time-of-flight measurements.")

        tof = []
        anchor_positions = []
        for id in self.anchor_ids:
            tof.append(tof_measurements[id])
            anchor_positions.append(self.anchor_network.get_anchor_position(id))
        tof = np.array(tof)
        anchor_positions = np.array(anchor_positions)

        squared_distances = (tof ** 2) * (constants.SPEED_OF_LIGHT ** 2)

        def objective_function(object_position):
            return np.sum((np.linalg.norm(anchor_positions - object_position, axis=1) ** 2) - squared_distances)

        # Initial guess for object position
        initial_guess = np.mean(anchor_positions, axis=0)

        # Perform the least-squares optimization
        result = least_squares(objective_function, initial_guess)

        return result.x
        