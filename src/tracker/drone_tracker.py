import copy
from .drone_socket import DroneSocket
from .drone_orchestrator import DroneOrchestrator
from src.devices import AnchorNetwork, Drone
from src.utils import load_config, Measurements
from src import constants as const


class DroneTracker:
    def __init__(self, capture=None, orchestrator=const.ORCHESTRATOR):
        if orchestrator:
            self.socket = DroneOrchestrator(tracker=self)
        else:
            self.socket = DroneSocket(tracker=self, capture=capture)
        self.drones = {}

        self.anchor_network = AnchorNetwork()
        anchors = load_config.load_anchor_positions()
        for anchor_id, pos in anchors.items():
            self.anchor_network.add_anchor(anchor_id, **pos)

        self.dropped_count = 0

        self.history = False
        if capture and not capture.live:
            self.history = True
            self.drones_history = {}

    def start(self):
        self.socket.start()
        print(f"[Tracker] Started")

    def stop(self):
        self.socket.stop()
        print("[Tracker] Terminated by user")

    def update_drone(self, id, measurements, timestamp, ground_truth=None):
        if len(measurements) == 4:
            if id not in self.drones:
                self._add_drone(id)
            self.drones[id].update_pos(measurements=Measurements(*[m for _, m in sorted(measurements.items(), key=lambda x: int(x[0]))], t=timestamp), ground_truth=ground_truth)
            if self.history and self.drones[id].active:
                self.drones_history[id].append(copy.copy(self.drones[id].pos))
        else:
            print(f'[Tracker] Drone {id} Invalid measurements len = {len(measurements)}, dropping packet')
            self.dropped_count += 1

    def _add_drone(self, id):
        self.drones[id] = Drone(id=id, anchor_network=self.anchor_network)
        if self.history:
            self.drones_history[id] = []
