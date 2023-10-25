import numpy as np
from .kalman_filter import KalmanFilter
from src import constants as const

class ExtendedKalmanFilter(KalmanFilter):
    def __init__(self):
        super().__init__()

    def _kf_update(self, measurement):
        # Calculate the Jacobian matrix for the measurement model at the current state estimate
        self.observation_matrix = self._calculate_jacobian()

        # K = P(k) * H^T * (H * P(k) * H^T + R)^(-1)
        kalman_gain = np.dot(np.dot(self.covariance, self.observation_matrix.T), 
                             np.linalg.inv(np.dot(np.dot(self.observation_matrix, self.covariance), self.observation_matrix.T) + self.measurement_noise))

        # x(k) = x(k) + K * (Z - H * x(k))
        self.state = self.state + np.dot(kalman_gain, (measurement - self._calculate_measurement_model()))
        # P(k) = (I - K * H) * P(k)
        self.covariance = np.dot((np.eye(6) - np.dot(kalman_gain, self.observation_matrix)), self.covariance)

    def _calculate_jacobian(self):
        # TODO Currently linear
        return np.array(const.OBSERVATION_MATRIX)

    def _calculate_measurement_model(self):
        # TODO Currently linear
        return np.dot(self.observation_matrix, self.state)
