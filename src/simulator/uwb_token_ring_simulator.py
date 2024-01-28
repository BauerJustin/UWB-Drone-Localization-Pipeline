import json
import socket
import threading
import time
import random
from .linear_trajectory import LinearTrajectory
from src.utils import load_config
from src import constants as const


class UWBTokenRingSimulator:
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

    def _run(self, i):
        while not self._stop_event.is_set():
            self._get_and_send_measurements(i)

    def _init_threads(self):
        self.threads = []
        for i in range(self.num_drones):
            self.threads.append(threading.Thread(target=self._run, args=(i,)))
        self._stop_event = threading.Event()

    def _init_trajectories(self):
        anchors = load_config.load_anchor_positions()
        self.trajectories = [LinearTrajectory(anchors) for _ in range(self.num_drones)]

    def _init_sockets(self):
        if not hasattr(self, 'sockets'):
            self.sockets = []
            self.host, self.port = load_config.load_network_host()
            for _ in range(self.num_drones):
                gcs_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                gcs_socket.connect((self.host, self.port))
                self.sockets.append(gcs_socket)

    def _get_and_send_measurements(self, i):
        measurements, ground_truth = self.trajectories[i].get_measurements()
        if random.random() < const.SIMULATOR_DROP_RATE:
            random_key = random.choice(list(measurements.keys()))
            del measurements[random_key]
        id = f"7{chr(ord('D')+i)}"
        msg = {
            'id': id,
            'measurements': measurements,
            'ground_truth': ground_truth,
            'timestamp': time.time()
        }
        try:
            msg_json = json.dumps(msg)
            self.sockets[i].sendall(msg_json.encode('utf-8'))
            self.sockets[i].recv(1024)
        except Exception as e:
            print(f"[Simulator] Reconnecting tag {id}")
            self.sockets[i] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sockets[i].connect((self.host, self.port))
        time.sleep(random.uniform(const.SIMULATOR_PROCESSING_MIN, const.SIMULATOR_PROCESSING_MAX))
