import numpy as np
from src import constants as const

class KalmanFilter:
    def __init__(self):
        self.process_noise = np.array(const.PROCESS_NOISE)  # Q
        self.measurement_noise = np.array(const.MEASUREMENT_NOISE)  # R
        self.transition_matrix = np.array(const.TRANSITION_MATRIX)  # F
        self.observation_matrix = np.array(const.OBSERVATION_MATRIX)  # H
    
    def update(self, pos, new_pos):
        self.state = np.array(pos.state())  # x
        self.covariance = np.array(pos.covariance)  # P
        self._update_transition_matrix(pos, new_pos)
        self._kf_predict()
        self._kf_update(measurement=new_pos.unpack())
        pos.update(*self.state, self.covariance, new_pos.t)

    def _update_transition_matrix(self, pos, new_pos):
        self.delta_t = new_pos.t - pos.t
        for i in range(3):
            self.transition_matrix[i, i+3] = self.delta_t

    def _kf_predict(self):
        # x(k) = F * x(k-1)
        self.state = np.dot(self.transition_matrix, self.state)
        # P(k) = F * P(k-1) * F^T + Q
        self.covariance = np.dot(np.dot(self.transition_matrix, self.covariance), self.transition_matrix.T) + self.process_noise

    def _kf_update(self, measurement):
        # K = P(k) * H^T * (H * P(k) * H^T + R)^(-1)
        kalman_gain = np.dot(np.dot(self.covariance, self.observation_matrix.T), 
                             np.linalg.inv(np.dot(np.dot(self.observation_matrix, self.covariance), self.observation_matrix.T) + self.measurement_noise))

        # x(k) = x(k) + K * (Z - H * x(k))
        self.state = self.state + np.dot(kalman_gain, (measurement - np.dot(self.observation_matrix, self.state)))
        # P(k) = (I - K * H) * P(k)
        self.covariance = np.dot((np.eye(6) - np.dot(kalman_gain, self.observation_matrix)), self.covariance)
