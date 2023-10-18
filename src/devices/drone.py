from src.algorithms import MultilaterationTOF

class Drone:
    def __init__(self, id, anchor_network):
        self.id = id
        self.anchor_network = anchor_network
        self.x, self.y, self.z = None, None, None
        self.multilaterator = MultilaterationTOF(anchor_network=self.anchor_network)

    def update_pos(self, tofs):
        self.x, self.y, self.z = self.multilaterator.calculate_position(tof_measurements=tofs)

    def get_pos(self):
        return self.x, self.y, self.z
