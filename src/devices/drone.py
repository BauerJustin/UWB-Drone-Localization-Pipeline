from src.algorithms import Multilateration

FILTER_ENABLED = False
FILTER_RATE = 0.9

class Drone:
    def __init__(self, id, anchor_network):
        self.id = id
        self.anchor_network = anchor_network
        self.x, self.y, self.z = None, None, None
        self.multilaterator = Multilateration(anchor_network=self.anchor_network)

    def update_pos(self, measurements):
        new_x, new_y, new_z = self.multilaterator.calculate_position(measurements=measurements)
        if not FILTER_ENABLED or self.x is None:
            self.x, self.y, self.z = new_x, new_y, new_z
        if FILTER_ENABLED:
            self.x = self.x * FILTER_RATE + new_x * (1 - FILTER_RATE)
            self.y = self.y * FILTER_RATE + new_y * (1 - FILTER_RATE)
            self.z = self.z * FILTER_RATE + new_z * (1 - FILTER_RATE)

    def get_pos(self):
        return self.x, self.y, self.z
