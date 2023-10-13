import threading
import time
import random

SPEED_OF_LIGHT = 3E8

MIN_TOF = 0
MAX_TOF = 10 / SPEED_OF_LIGHT  # 10 m

MAX_DRONE_SPEED = 8  # m / s

SYSTEM_DELAY = 10  # Hz
MAX_NEW_DIST = MAX_DRONE_SPEED * SYSTEM_DELAY / SPEED_OF_LIGHT

class UWBNetworkSimulator:
    def __init__(self, num_drones=3):
        self.threads = []
        for _ in range(num_drones):
            self.threads.append(threading.Thread(target=self.run))
        self._stop_event = threading.Event()
        self.lock = threading.Lock()
        self.token = 0

        self.num_drones = num_drones
        self.tofs = []
        for _ in range(self.num_drones):
            self.tofs.append({
                "A1": random.uniform(MIN_TOF, MAX_TOF),
                "A2": random.uniform(MIN_TOF, MAX_TOF),
                "A3": random.uniform(MIN_TOF, MAX_TOF),
                "A4": random.uniform(MIN_TOF, MAX_TOF),
            })

    def start(self):
        for thread in self.threads:
            thread.start()

    def run(self):
        while not self._stop_event.is_set():
            with self.lock:
                for anchor in self.tofs[self.token].keys():
                    self.tofs[self.token][anchor] += random.uniform(-MAX_NEW_DIST, MAX_NEW_DIST)
                self.token = (self.token + 1) % self.num_drones
            time.sleep(0.1)

    def stop(self):
        self._stop_event.set()
        for thread in self.threads:
            thread.join()
        