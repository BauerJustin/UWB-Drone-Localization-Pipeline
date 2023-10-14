import json
import socket
import threading
import time
import random
from src.utils import network

SPEED_OF_LIGHT = 3E8

MIN_TOF = 0
MAX_TOF = 10 / SPEED_OF_LIGHT  # 10 m

MAX_DRONE_SPEED = 8  # m / s
SYSTEM_DELAY = 10  # Hz

MAX_NEW_DIST = MAX_DRONE_SPEED * SYSTEM_DELAY / SPEED_OF_LIGHT

class UWBNetworkSimulator:
    def __init__(self, num_drones=3):
        self.num_drones = num_drones
        
        self._connect_to_sockets()
        self._init_threads()
        self._init_tofs()

    def start(self):
        for thread in self.threads:
            thread.start()

    def stop(self):
        self._stop_event.set()
        for thread in self.threads:
            thread.join()
        for socket in self.sockets:
            if socket:
                socket.close()

    def _run(self):
        while not self._stop_event.is_set():
            with self.lock:
                self._update_tofs()
                self._send_tofs()
                self.token = (self.token + 1) % self.num_drones
            time.sleep(0.1)

    def _connect_to_sockets(self):
        self.host, self.port = network.load_network_host()
        self.sockets = []

        for i in range(self.num_drones):
            self.sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            connected = False
            while not connected:
                try:
                    self.sockets[i].connect((self.host, self.port))
                    connected = True
                except:
                    print(f'Failed to connect simulator to {self.host}:{self.port}')
                    time.sleep(1)

    def _init_threads(self):
        self.threads = []
        for _ in range(self.num_drones):
            self.threads.append(threading.Thread(target=self._run))
        self._stop_event = threading.Event()
        self.lock = threading.Lock()
        self.token = 0

    def _init_tofs(self):
        self.tofs = []
        for _ in range(self.num_drones):
            self.tofs.append({
                "A1": random.uniform(MIN_TOF, MAX_TOF),
                "A2": random.uniform(MIN_TOF, MAX_TOF),
                "A3": random.uniform(MIN_TOF, MAX_TOF),
                "A4": random.uniform(MIN_TOF, MAX_TOF),
            })

    def _update_tofs(self):
        for anchor in self.tofs[self.token].keys():
            self.tofs[self.token][anchor] += random.uniform(-MAX_NEW_DIST, MAX_NEW_DIST)

    def _send_tofs(self):
        msg = {
            'id': self.token,
            'tofs': self.tofs[self.token]
        }
        try:
            msg_json = json.dumps(msg)
            self.sockets[self.token].send(msg_json.encode('utf-8'))
            response = self.socket.recv(1024)
            print(f"Sent message: {msg_json}, Received response: {response.decode('utf-8')}")
        except Exception as e:
            print(f"Error sending message: {str(e)}")
