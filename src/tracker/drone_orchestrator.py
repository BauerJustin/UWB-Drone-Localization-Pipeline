import socket
import json
import time
import threading
from src.utils import load_config
from src import constants as const


class DroneOrchestrator:
    def __init__(self, tracker):
        self.tracker = tracker
        self.host, self.port = load_config.load_network_host()
        self.tag_address = {}
        self.start_time = time.time()
        self.previous_id = None
        self.shutdown_event = threading.Event()
        self.tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.orchestrator_thread = threading.Thread(target=self._orchestrate)

    def start(self):
        self.tracker_socket.bind((self.host, self.port))
        self.tracker_socket.settimeout(1)

        print(f"[Orchestrator] Listening on {self.host}:{self.port}")
        self.orchestrator_thread.start()

    def stop(self):
        self.shutdown_event.set()
        self.tracker_socket.close()
        self.orchestrator_thread.join()

    def _orchestrate(self):
        while not self.shutdown_event.is_set():
            try:
                data, (ip, port) = self.tracker_socket.recvfrom(1024)
            except socket.timeout:
                print("[Orchestrator] No drones found, trying again...")
                if self.previous_id is not None:
                    next_id = self._get_next_key(self.previous_id)
                    next_ip, next_port = self.tag_address[next_id]
                    self._request_measurements(next_ip, next_port)
                continue

            if not data:
                continue

            data = json.loads(data.decode('utf-8'))
            id = data['id']
            if id not in self.tag_address:
                print(f"[Orchestrator] New tag added. ID: {id} Address: {ip}:{port}")
                self.tag_address[id] = (ip, port)
                if self.previous_id is None:
                    self._request_measurements(ip, port)
                    self.start_time = time.time()
                    self.previous_id = id
            else:
                print(f"[Orchestrator] Received {len(data)} bytes from {ip}:{port}")
                print(f"[Orchestrator] Data: {data}")
                end_time = time.time()
                time_taken = end_time - self.start_time
                print(f"[Orchestrator] Time taken (ms): {time_taken}")
                self.start_time = time.time()

                self.tracker.update_drone(id=data['id'],
                                           measurements=data['measurements'],
                                           timestamp=data['timestamp'],
                                           ground_truth=data.get('ground_truth'))

                next_id = self._get_next_key(id)
                next_ip, next_port = self.tag_address[next_id]
                time.sleep(const.ORCHESTRATOR_DELAY)
                self._request_measurements(next_ip, next_port)
                self.previous_id = next_id

    def _get_next_key(self, current_key):
        keys = list(self.tag_address)
        current_index = keys.index(current_key)
        next_index = (current_index + 1) % len(keys)
        return keys[next_index]

    def _request_measurements(self, ip, port):
        self.tracker_socket.sendto(b"1", (ip, port))
        print(f"[Orchestrator] Sent req msg to {ip}:{port}")
