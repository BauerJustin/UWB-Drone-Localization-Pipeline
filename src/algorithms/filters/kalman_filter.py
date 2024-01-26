import numpy as np
from src import constants as const
from src.utils import load_config

class KalmanFilter:
    def __init__(self):
        kf_settings = load_config.load_kf_settings("measurement")
        self.process_noise = np.array(kf_settings['PROCESS_NOISE'])  # Q
        self.measurement_noise = np.array(kf_settings['MEASUREMENT_NOISE'])  # R
        self.transition_matrix = np.array(kf_settings['TRANSITION_MATRIX'])  # F
        self.observation_matrix = np.array(kf_settings['OBSERVATION_MATRIX'])  # H
    
    def update(self, state, measurement):
        self.state = np.array(state.state())  # x
        self.covariance = np.array(state.covariance)  # P
        self._update_transition_matrix(state, measurement)
        self._kf_predict()
        self._kf_update(measurement)
        state.update(*self.state, self.covariance, measurement.t)

    def _update_transition_matrix(self, state, measurement):
        self.delta_t = measurement.t - state.t
        for i in range(len(self.transition_matrix[0])//2):
            self.transition_matrix[i, i+len(self.transition_matrix[0])//2] = self.delta_t

    def _kf_predict(self):
        # x(k) = F * x(k-1)
        self.state = np.dot(self.transition_matrix, self.state)
        # P(k) = F * P(k-1) * F^T + Q
        self.covariance = np.dot(np.dot(self.transition_matrix, self.covariance), self.transition_matrix.T) + self.process_noise

    def _kf_update(self, measurement):
        mask = np.array([value is not None for value in measurement.unpack()])
        masked_observation_matrix = self.observation_matrix[mask, :]

        if np.any(mask):
            # K = P(k) * H^T * (H * P(k) * H^T + R)^(-1)
            kalman_gain = np.dot(np.dot(self.covariance, self.observation_matrix.T), np.linalg.inv(
                np.dot(np.dot(self.observation_matrix, self.covariance), self.observation_matrix.T) + self.measurement_noise))[:, mask]

            # x(k) = x(k) + K * (Z - H * x(k))
            self.state = self.state + np.dot(kalman_gain, (np.array(measurement.unpack())[mask] - np.dot(masked_observation_matrix, self.state)))

            # P(k) = (I - K * H) * P(k)
            self.covariance = np.dot(np.eye(len(self.state)) - np.dot(kalman_gain, masked_observation_matrix), self.covariance)
