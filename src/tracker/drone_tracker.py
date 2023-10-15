import time
from .drone_socket import DroneSocket
from src.devices import Drone


class DroneTracker:
    def __init__(self):
        self.socket = DroneSocket(tracker=self)
        self.drones = {}

    def start(self):
        self.socket.start()
        print(f"[Tracker] Started")
        self._track_drones()

    def stop(self):
        self.socket.stop()
        print("[Tracker] Terminated by user")

    def update_drone(self, id, tofs):
        if id not in self.drones:
            self._add_drone(id)
        self.drones[id].update_pos(tofs=tofs)

    def _add_drone(self, id):
        self.drones[id] = Drone(id=id)

    def _track_drones(self):
        while True:
            time.sleep(5)
