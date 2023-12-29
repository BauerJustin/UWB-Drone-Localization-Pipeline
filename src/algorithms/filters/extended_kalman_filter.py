import numpy as np
from .kalman_filter import KalmanFilter
from src.utils import load_config

class ExtendedKalmanFilter(KalmanFilter):
    def __init__(self):
        super().__init__()
        anchors = load_config.load_anchor_positions()
        self.anchor_positions = np.array([list(v.values()) for v in anchors.values()])

    def _kf_update(self, measurement):
        # Calculate the Jacobian matrix for the measurement model at the current state estimate
        self.observation_matrix = self._calculate_jacobian()

        # K = P(k) * H^T * (H * P(k) * H^T + R)^(-1)
        kalman_gain = np.dot(np.dot(self.covariance, self.observation_matrix.T), 
                             np.linalg.inv(np.dot(np.dot(self.observation_matrix, self.covariance), self.observation_matrix.T) + self.measurement_noise))

        # x(k) = x(k) + K * (Z - H * x(k))
        self.state = self.state + np.dot(kalman_gain, (measurement - self._calculate_measurement_model()))
        # P(k) = (I - K * H) * P(k)
        self.covariance = np.dot((np.eye(len(self.observation_matrix[0])) - np.dot(kalman_gain, self.observation_matrix)), self.covariance)

    def _calculate_jacobian(self):
        jacobian = np.zeros((len(self.anchor_positions), len(self.state)))
        for i, anchor in enumerate(self.anchor_positions):
            dx = self.state[0] - anchor[0]
            dy = self.state[1] - anchor[1]
            dz = self.state[2] - anchor[2]
            dist = np.sqrt(dx**2 + dy**2 + dz**2)
            
            if dist > 0:
                jacobian[i, 0] = dx / dist
                jacobian[i, 1] = dy / dist
                jacobian[i, 2] = dz / dist
        return jacobian

    def _calculate_measurement_model(self):
        measurement_model = np.zeros(len(self.anchor_positions))
        for i, anchor in enumerate(self.anchor_positions):
            measurement_model[i] = np.sqrt((self.state[0] - anchor[0])**2 + 
                                           (self.state[1] - anchor[1])**2 + 
                                           (self.state[2] - anchor[2])**2)
        return measurement_model
