import math
import unittest
from src import constants
from src.algorithms import MultilaterationTOF
from src.devices import AnchorNetwork


class TestMultilaterationTOF(unittest.TestCase):
    def setUp(self):
        test_anchors = {
            "A1": {"x": 1, "y": 0, "z": 0},
            "A2": {"x": 5, "y": 0, "z": 0},
            "A3": {"x": 0, "y": 2, "z": 0},
            "A4": {"x": 0, "y": 5, "z": 0}
        }
        self.anchor_network = AnchorNetwork()
        for anchor_id, pos in test_anchors.items():
            self.anchor_network.add_anchor(anchor_id, pos['x'], pos['y'], pos['z'])
        self.multilateration_tof = MultilaterationTOF(self.anchor_network)

    def test_calculate_position(self):
        tof_measurements = {
            "A1": math.sqrt(13) / constants.SPEED_OF_LIGHT,
            "A2": math.sqrt(13) / constants.SPEED_OF_LIGHT,
            "A3": math.sqrt(12) / constants.SPEED_OF_LIGHT,
            "A4": math.sqrt(13) / constants.SPEED_OF_LIGHT
        }
        x, y, z = self.multilateration_tof.calculate_position(tof_measurements, "IterativeLSE")
        print(x, y, z)
        self.assertAlmostEqual(x, 3.0)
        self.assertAlmostEqual(y, 3.0)
        self.assertAlmostEqual(z, 0.0)

if __name__ == '__main__':
    unittest.main()
