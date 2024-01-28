import json
import random
import socket
import threading
import time
from .linear_trajectory import LinearTrajectory
from src.utils import load_config
from src import constants as const


class UWBNetworkSimulator:
    def __init__(self, num_drones=3):
        self.num_drones = num_drones
        self._init_threads()
        self._init_trajectories()
        self.logger = load_config.setup_logger(__name__)

    def start(self):
        self._init_sockets()
        print(f"[Simulator] Starting for {self.num_drones} drone{'s' if self.num_drones > 1 else ''}")
        for thread in self.threads:
            thread.start()

    def stop(self):
        self._stop_event.set()
        for thread in self.threads:
            thread.join()
        print("[Simulator] Terminated by user")

    def _run(self):
        while not self._stop_event.is_set():
            with self.lock:
                self._get_and_send_measurements()
                self.token = (self.token + 1) % self.num_drones
            time.sleep(1 / const.SIMULATOR_FREQUENCY)

    def _init_threads(self):
        self.threads = []
        for _ in range(self.num_drones):
            self.threads.append(threading.Thread(target=self._run))
        self._stop_event = threading.Event()
        self.lock = threading.Lock()
        self.token = 0

    def _init_trajectories(self):
        anchors = load_config.load_anchor_positions()
        self.trajectories = [LinearTrajectory(anchors) for _ in range(self.num_drones)]

    def _init_sockets(self):
        self.sockets = []
        self.host, self.port = load_config.load_network_host()
        for _ in range(self.num_drones):
            self.sockets.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))

    def _get_and_send_measurements(self):
        measurements, ground_truth = self.trajectories[self.token].get_measurements()
        if random.random() < const.SIMULATOR_DROP_RATE:
            random_key = random.choice(list(measurements.keys()))
            del measurements[random_key]
        msg = {
            'id': self.token,
            'measurements': measurements,
            'ground_truth': ground_truth,
            'timestamp': time.time()
        }
        try:
            msg_json = json.dumps(msg)
            self.sockets[self.token].sendto(msg_json.encode('utf-8'), (self.host, self.port))
        except Exception as e:
            print(f"[Simulator] Error sending message: {str(e)}")
