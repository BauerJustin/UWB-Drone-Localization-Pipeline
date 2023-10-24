import unittest
from src.algorithms import Filter
from src.algorithms.filters import MovingAverageFilter, KalmanFilter
from src.utils import Position


class TestFilter(unittest.TestCase):
    def test_filter_initialization(self):
        # Test initialization with MovingAverageFilter
        ma_filter = Filter("MA")
        self.assertIsInstance(ma_filter.filter, MovingAverageFilter)

        # Test initialization with KalmanFilter
        kf_filter = Filter("KF")
        self.assertIsInstance(kf_filter.filter, KalmanFilter)


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

if __name__ == '__main__':
    unittest.main()
