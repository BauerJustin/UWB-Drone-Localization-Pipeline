import json
import socket
import threading
import time
from .linear_trajectory import LinearTrajectory
from src.utils import load_config


class UWBNetworkSimulator:
    def __init__(self, num_drones=3):
        self.num_drones = num_drones
        self.sockets = []
        self.connection_lock = threading.Lock()

        self._init_threads()
        self._init_trajectories()

    def start(self):
        print(f"[Simulator] Starting for {self.num_drones} drones")
        for thread in self.threads:
            thread.start()

    def stop(self):
        self._stop_event.set()
        for thread in self.threads:
            thread.join()
        for socket in self.sockets:
            if socket:
                socket.close()
        print("[Simulator] Terminated by user")

    def _run(self):
        with self.connection_lock:
            if len(self.sockets) == 0:
                self._connect_to_sockets()
        while not self._stop_event.is_set():
            with self.lock:
                self._get_and_send_tofs()
                self.token = (self.token + 1) % self.num_drones
            time.sleep(0.1)

    def _connect_to_sockets(self):
        self.host, self.port = load_config.load_network_host()
        time.sleep(1)

        for i in range(self.num_drones):
            self.sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            connected = False
            while not connected:
                try:
                    self.sockets[i].connect((self.host, self.port))
                    connected = True
                except:
                    print(f'[Simulator] Failed to connect simulator to {self.host}:{self.port}')
                    time.sleep(1)

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

    def _get_and_send_tofs(self):
        msg = {
            'id': self.token,
            'tofs': self.trajectories[self.token].get_tofs()
        }
        try:
            msg_json = json.dumps(msg)
            self.sockets[self.token].send(msg_json.encode('utf-8'))
        except Exception as e:
            print(f"[Simulator] Error sending message: {str(e)}")
