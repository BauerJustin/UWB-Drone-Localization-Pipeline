from .drone_socket import DroneSocket
from src.devices import AnchorNetwork, Drone
from src.utils import load_config


class DroneTracker:
    def __init__(self):
        self.socket = DroneSocket(tracker=self)
        self.drones = {}
        self.anchor_network = AnchorNetwork()
        anchors = load_config.load_anchor_positions()
        for anchor_id, pos in anchors.items():
            self.anchor_network.add_anchor(anchor_id, pos['x'], pos['y'], pos['z'])

    def start(self):
        self.socket.start()
        print(f"[Tracker] Started")

    def stop(self):
        self.socket.stop()
        print("[Tracker] Terminated by user")

    def update_drone(self, id, measurements, ground_truth=None):
        if id not in self.drones:
            self._add_drone(id)
        self.drones[id].update_pos(measurements=measurements, ground_truth=ground_truth)

    def _add_drone(self, id):
        self.drones[id] = Drone(id=id, anchor_network=self.anchor_network)
