import json
import socket
import threading
from src.utils import network


class DroneTracker:
    def __init__(self):
        self.host, self.port = network.load_network_host()
        self.tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.drone_connections = []
        self.shutdown_event = threading.Event()

    def start(self):
        self.tracker_socket.bind((self.host, self.port))
        self.tracker_socket.listen()

        print(f"[Tracker] Listening on {self.host}:{self.port}")
        self._accept_connections()

    def stop(self):
        self.shutdown_event.set() 
        self.tracker_socket.close()
        for drone_socket, drone_thread in self.drone_connections:
            if drone_socket:
                drone_socket.close()
            drone_thread.join()
        print("[Tracker] Terminated by user")

    def _accept_connections(self):
        while not self.shutdown_event.is_set():
            drone_socket, drone_address = self.tracker_socket.accept()
            print(f"[Tracker] Drone connected to port {drone_address[1]}")
            drone_thread = threading.Thread(target=self._handle_connection, args=(drone_socket,))
            drone_thread.start()
            self.drone_connections.append((drone_socket, drone_thread))

    def _handle_connection(self, drone_socket):
        try:
            while not self.shutdown_event.is_set():
                data = drone_socket.recv(1024)
                if not data:
                    break  # Connection closed
                data = json.loads(data.decode('utf-8'))
                print(f"[Tracker] Received data from drone {data['id']}: {data['tofs']}")
        except Exception as e:
            if not self.shutdown_event.is_set():
                print(f"[Tracker] Handler error: {str(e)}")
        finally:
            if drone_socket:
                drone_socket.close()
