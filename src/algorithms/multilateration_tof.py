import numpy as np
from src import constants


# TODO: Validate algorithm

class MultilaterationTOF:
    def __init__(self, anchor_network):
        self.anchor_network = anchor_network
        self.anchor_ids = anchor_network.get_anchor_ids()

    def calculate_position(self, tof_measurements):
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
    