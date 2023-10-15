import json
import socket
import threading
from src.utils import load_config


class DroneSocket:
    def __init__(self, tracker):
        self.tracker = tracker
        self.host, self.port = load_config.load_network_host()
        self.tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.drone_connections = []
        self.listener_thread = threading.Thread(target=self._accept_connections)
        self.shutdown_event = threading.Event()

    def start(self):
        self.tracker_socket.bind((self.host, self.port))
        self.tracker_socket.listen()

        print(f"[Socket] Listening on {self.host}:{self.port}")
        self.listener_thread.start()

    def stop(self):
        self.shutdown_event.set()
        self.tracker_socket.close()
        self.listener_thread.join()
        for drone_socket, drone_thread in self.drone_connections:
            if drone_socket:
                drone_socket.close()
            drone_thread.join()

    def _accept_connections(self):
        while not self.shutdown_event.is_set():
            try:
                drone_socket, drone_address = self.tracker_socket.accept()
                print(f"[Socket] Drone connected to port {drone_address[1]}")
                drone_thread = threading.Thread(target=self._handle_connection, args=(drone_socket,))
                drone_thread.start()
                self.drone_connections.append((drone_socket, drone_thread))
            except:
                if self.shutdown_event.is_set():
                    pass
                else:
                    raise

    def _handle_connection(self, drone_socket):
        try:
            while not self.shutdown_event.is_set():
                data = drone_socket.recv(1024)
                if not data:
                    break  # Connection closed
                data = json.loads(data.decode('utf-8'))
                self.tracker.update_drone(id=data['id'], tofs=data['tofs'])
        except Exception as e:
            if not self.shutdown_event.is_set():
                print(f"[Socket] Handler error: {str(e)}")
        finally:
            if drone_socket:
                drone_socket.close()
