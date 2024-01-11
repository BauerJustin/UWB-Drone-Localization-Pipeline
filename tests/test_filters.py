import unittest
import numpy as np
from src.algorithms import Filter
from src.algorithms.filters import MovingAverageFilter, KalmanFilter, ExtendedKalmanFilter
from src.utils import Position, Measurements


class TestFilter(unittest.TestCase):
    def test_filter_initialization(self):
        # Test initialization with MovingAverageFilter
        ma_filter = Filter("MA")
        self.assertIsInstance(ma_filter.filter, MovingAverageFilter)

        # Test initialization with KalmanFilter
        kf_filter = Filter("KF")
        self.assertIsInstance(kf_filter.filter, KalmanFilter)

        # Test initialization with ExtendedKalmanFilter
        ekf_filter = Filter("EKF")
        self.assertIsInstance(ekf_filter.filter, ExtendedKalmanFilter)


class TestMovingAverageFilter(unittest.TestCase):
    def test_initialization(self):
        filter_rate = 0.1
        moving_avg_filter = MovingAverageFilter(filter_rate)
        self.assertEqual(moving_avg_filter.filter_rate, filter_rate)

    def test_update(self):
        filter_rate = 0.1
        moving_avg_filter = MovingAverageFilter(filter_rate)
        
        initial_pos = Position(1.0, 2.0, 3.0)
        new_pos = Position(4.0, 5.0, 6.0)
        
        moving_avg_filter.update(initial_pos, new_pos)
        
        # Calculate the expected values after the update
        expected_x = (1.0 * (1 - filter_rate)) + (4.0 * filter_rate)
        expected_y = (2.0 * (1 - filter_rate)) + (5.0 * filter_rate)
        expected_z = (3.0 * (1 - filter_rate)) + (6.0 * filter_rate)
        
        self.assertAlmostEqual(initial_pos.x, expected_x, places=5)
        self.assertAlmostEqual(initial_pos.y, expected_y, places=5)
        self.assertAlmostEqual(initial_pos.z, expected_z, places=5)


class TestKalmanFilter(unittest.TestCase):
    def setUp(self):
        self.kalman_filter = KalmanFilter()

    def test_kf_predict(self):
        initial_state = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        initial_covariance = np.eye(6)
        transition_matrix = np.array([
            [1.0, 0.0, 0.0, 0.1, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0, 0.1, 0.0],
            [0.0, 0.0, 1.0, 0.0, 0.0, 0.1],
            [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        ])
        process_noise = np.array([
            [0.01, 0.0, 0.0, 0.01, 0.0, 0.0],
            [0.0, 0.01, 0.0, 0.0, 0.01, 0.0],
            [0.0, 0.0, 0.01, 0.0, 0.0, 0.01],
            [0.01, 0.0, 0.0, 0.01, 0.0, 0.0],
            [0.0, 0.01, 0.0, 0.0, 0.01, 0.0],
            [0.0, 0.0, 0.01, 0.0, 0.0, 0.01]
        ])

        self.kalman_filter.state = initial_state
        self.kalman_filter.covariance = initial_covariance
        self.kalman_filter.transition_matrix = transition_matrix
        self.kalman_filter.process_noise = process_noise
        self.kalman_filter._kf_predict()

        # Make assertions about the updated state and covariance after prediction
        expected_state = np.dot(transition_matrix, initial_state)
        expected_covariance = np.dot(np.dot(transition_matrix, initial_covariance), transition_matrix.T) + process_noise

        self.assertTrue(np.array_equal(self.kalman_filter.state, expected_state))
        self.assertTrue(np.array_equal(self.kalman_filter.covariance, expected_covariance))

    def test_kf_update(self):
        initial_state = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        initial_covariance = np.eye(6)
        measurement = Position(7.0, 8.0, 9.0)
        observation_matrix = np.array([
            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
        ])
        measurement_noise = np.array([
            [0.1, 0.0, 0.0],
            [0.0, 0.1, 0.0],
            [0.0, 0.0, 0.1]
        ])

        self.kalman_filter.state = initial_state
        self.kalman_filter.covariance = initial_covariance
        self.kalman_filter.observation_matrix = observation_matrix
        self.kalman_filter.measurement_noise = measurement_noise
        self.kalman_filter._kf_update(measurement)

        # Make assertions about the updated state and covariance after update
        kalman_gain = np.dot(np.dot(initial_covariance, observation_matrix.T), 
                             np.linalg.inv(np.dot(np.dot(observation_matrix, initial_covariance), observation_matrix.T) + measurement_noise))
        expected_state = initial_state + np.dot(kalman_gain, (measurement.unpack() - np.dot(observation_matrix, initial_state)))
        expected_covariance = np.dot((np.eye(6) - np.dot(kalman_gain, observation_matrix)), initial_covariance)

        self.assertTrue(np.allclose(self.kalman_filter.state, expected_state))
        self.assertTrue(np.allclose(self.kalman_filter.covariance, expected_covariance))
        
    def test_kf_missing_measurements_update(self):
        initial_state = np.array([1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 0.5])
        initial_covariance = np.eye(8)

        measurement = Measurements(d1=4.0, d2=None, d3=4.0, d4=4.0, t=1.0)

        self.kalman_filter.state = initial_state
        self.kalman_filter.covariance = initial_covariance

        self.kalman_filter._kf_update(measurement)

        expected_state = np.array([3.0, 1.0, 3.0, 3.0, 0.5, 0.5, 0.5, 0.5])
        expected_covariance = np.diag([0.33333, 1, 0.33333, 0.33333, 1, 1, 1, 1])

        self.assertTrue(np.allclose(list(self.kalman_filter.state), expected_state))
        self.assertTrue(np.allclose(self.kalman_filter.covariance, expected_covariance))

class TestExtendedKalmanFilter(unittest.TestCase):
    def setUp(self):
        self.kalman_filter = ExtendedKalmanFilter()

    def test_ekf_predict(self):
        initial_state = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
        initial_covariance = np.eye(8)
        transition_matrix = np.array([
            [1.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.1, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.1],
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        ])
        process_noise = np.array([
            [0.01, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0],
            [0.0, 0.01, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0],
            [0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.01, 0.0],
            [0.0, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.01],
            [0.01, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0],
            [0.0, 0.01, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0],
            [0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.01, 0.0],
            [0.0, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.01]
        ])

        self.kalman_filter.state = initial_state
        self.kalman_filter.covariance = initial_covariance
        self.kalman_filter.transition_matrix = transition_matrix
        self.kalman_filter.process_noise = process_noise
        self.kalman_filter._kf_predict()

        # Make assertions about the updated state and covariance after prediction
        expected_state = np.dot(transition_matrix, initial_state)
        expected_covariance = np.dot(np.dot(transition_matrix, initial_covariance), transition_matrix.T) + process_noise

        self.assertTrue(np.array_equal(self.kalman_filter.state, expected_state))
        self.assertTrue(np.array_equal(self.kalman_filter.covariance, expected_covariance))

    def test_ekf_update(self):
        initial_state = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
        initial_covariance = np.eye(8)
        measurement = np.array([7.0, 8.0, 9.0, 10.0])
        measurement_noise = np.array([
            [0.1, 0.0, 0.0, 0.0],
            [0.0, 0.1, 0.0, 0.0],
            [0.0, 0.0, 0.1, 0.0],
            [0.0, 0.0, 0.0, 0.1]
        ])

        self.kalman_filter.state = initial_state
        self.kalman_filter.covariance = initial_covariance
        observation_matrix = self.kalman_filter._calculate_jacobian()
        self.kalman_filter.observation_matrix = observation_matrix
        self.kalman_filter.measurement_noise = measurement_noise
        measurement_model = self.kalman_filter._calculate_measurement_model()
        self.kalman_filter._kf_update(measurement)

        # Make assertions about the updated state and covariance after update
        kalman_gain = np.dot(np.dot(initial_covariance, observation_matrix.T), 
                             np.linalg.inv(np.dot(np.dot(observation_matrix, initial_covariance), observation_matrix.T) + measurement_noise))
        expected_state = initial_state + np.dot(kalman_gain, (measurement - measurement_model))
        expected_covariance = np.dot((np.eye(len(observation_matrix[0])) - np.dot(kalman_gain, observation_matrix)), initial_covariance)

        self.assertTrue(np.allclose(self.kalman_filter.state, expected_state))
        self.assertTrue(np.allclose(self.kalman_filter.covariance, expected_covariance))

if __name__ == '__main__':
    unittest.main()
