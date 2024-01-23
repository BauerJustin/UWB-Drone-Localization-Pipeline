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
        self.tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener_thread = threading.Thread(target=self._accept_connections)
        self.shutdown_event = threading.Event()
        self.lock = threading.Lock()

    def start(self):
        self.tracker_socket.bind((self.host, self.port))
        self.tracker_socket.listen()

        print(f"[Orchestrator] Listening on {self.host}:{self.port}")
        self.listener_thread.start()

    def stop(self):
        self.shutdown_event.set()
        self.tracker_socket.close()
        self.listener_thread.join()

    def _accept_connections(self):
        while not self.shutdown_event.is_set():
            tag_socket, tag_address = self.tracker_socket.accept()

            client_thread = threading.Thread(target=self._handle_connection, args=(tag_socket, tag_address))
            client_thread.start()

    def _handle_connection(self, tag_socket, tag_address):
        print(f"[Orchestrator] Accepted connection from {tag_address}")

        data = tag_socket.recv(1024)
        if not data:
            print("[Orchestrator] Invalid Connection")
            tag_socket.close()
            return
        
        data = json.loads(data.decode('utf-8'))
        id = data['id']
        if 'measurements' in data:
            self.tracker.update_drone(id=data['id'],
                                      measurements=data['measurements'],
                                      timestamp=data['timestamp'],
                                      ground_truth=data.get('ground_truth'))
        tag_socket.settimeout(const.ORCHESTRATOR_TIMEOUT)

        while True:
            with self.lock:
                try:
                    tag_socket.sendall(b"1")
                    data = tag_socket.recv(1024)
                except:
                    print(f"[Orchestrator] {id} timed out")
                    break

                if not data:
                    break  # Connection closed by the client
                data = json.loads(data.decode('utf-8'))

            self.tracker.update_drone(id=data['id'],
                                      measurements=data['measurements'],
                                      timestamp=data['timestamp'],
                                      ground_truth=data.get('ground_truth'))

            time.sleep(const.ORCHESTRATOR_COOLDOWN)

        tag_socket.close()
        print(f"[Orchestrator] {id} connection at {tag_address} closed")
