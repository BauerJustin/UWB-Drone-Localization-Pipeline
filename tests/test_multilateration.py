import unittest
from src.algorithms import MultilaterationTOF
from src.devices import AnchorNetwork

test_anchors = {
    "A1": {
        "x": 0,
        "y": 0,
        "z": 0
    },
    "A2": {
        "x": 5,
        "y": 0,
        "z": 5
    },
    "A3": {
        "x": 0,
        "y": 5,
        "z": 5
    },
    "A4": {
        "x": 5,
        "y": 5,
        "z": 5
    }
}

class TestMultilaterationTOF(unittest.TestCase):
    def setUp(self):
        self.anchor_network = AnchorNetwork()
        for anchor_id, pos in test_anchors.items():
            self.anchor_network.add_anchor(anchor_id, pos['x'], pos['y'], pos['z'])
        self.multilateration_tof = MultilaterationTOF(self.anchor_network)

    def test_calculate_position(self):
        tof_measurements = {
            "A1": 0,
            "A2": 0,
            "A3": 0,
            "A4": 0
        }
        x, y, z = self.multilateration_tof.calculate_position(tof_measurements)
        self.assertAlmostEqual(x, 0.5, places=6)
        self.assertAlmostEqual(y, 0.5, places=6)
        self.assertAlmostEqual(z, 0.0, places=6)

if __name__ == '__main__':
    unittest.main()
