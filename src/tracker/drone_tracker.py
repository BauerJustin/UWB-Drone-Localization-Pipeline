import time
from .drone_socket import DroneSocket


class DroneTracker:
    def __init__(self):
        self.socket = DroneSocket()

    def start(self):
        self.socket.start()
        print(f"[Tracker] Started")
        self._track_drones()

    def stop(self):
        self.socket.stop()
        print("[Tracker] Terminated by user")

    def _track_drones(self):
        while True:
            print("[Tracker] Loop")
            time.sleep(0.1)
