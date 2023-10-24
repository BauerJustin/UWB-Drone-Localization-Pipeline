import math
import unittest
from src.algorithms import Multilateration
from src.devices import AnchorNetwork


class TestMultilateration(unittest.TestCase):
    def setUp(self):
        test_anchors = {
            "A1": {"x": 1, "y": 0, "z": 0},
            "A2": {"x": 5, "y": 0, "z": 0},
            "A3": {"x": 0, "y": 2, "z": 0},
            "A4": {"x": 0, "y": 5, "z": 0}
        }
        self.anchor_network = AnchorNetwork()
        for anchor_id, pos in test_anchors.items():
            self.anchor_network.add_anchor(anchor_id, **pos)
        self.multilateration = Multilateration(self.anchor_network)

    def test_calculate_position(self):
        measurements = {
            "A1": math.sqrt(13),
            "A2": math.sqrt(13),
            "A3": math.sqrt(12),
            "A4": math.sqrt(13)
        }
        pos = self.multilateration.calculate_position(measurements)
        self.assertAlmostEqual(pos.x, 3.0, 0)
        self.assertAlmostEqual(pos.y, 3.0, 0)
        self.assertAlmostEqual(pos.z, 0.0, 2)

if __name__ == '__main__':
    unittest.main()
