import json
import socket
import threading
from src.utils import load_config


class DroneSocket:
    def __init__(self, tracker):
        self.tracker = tracker
        self.host, self.port = load_config.load_network_host()
        self.tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.drone_connections = []
        self.listener_thread = threading.Thread(target=self._accept_datagrams)
        self.shutdown_event = threading.Event()

    def start(self):
        self.tracker_socket.bind((self.host, self.port))

        print(f"[Socket] Listening on {self.host}:{self.port}")
        self.listener_thread.start()

    def stop(self):
        self.shutdown_event.set()
        self.tracker_socket.close()
        self.listener_thread.join()

    def _accept_datagrams(self):
        while not self.shutdown_event.is_set():
            try:
                data, _ = self.tracker_socket.recvfrom(1024)
                data = json.loads(data.decode('utf-8'))
                self.tracker.update_drone(id=data['id'], measurements=data['measurements'], ground_truth=data['ground_truth'] if 'ground_truth' in data else None)
            except Exception as e:
                if self.shutdown_event.is_set():
                    break
                else:
                    raise
