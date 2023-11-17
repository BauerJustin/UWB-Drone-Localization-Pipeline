import json
import socket
import threading
import time
from src.utils import load_config


class DroneSocket:
    def __init__(self, tracker, capture=None):
        self.tracker = tracker
        self.capture = capture
        self.host, self.port = load_config.load_network_host()
        self.tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.drone_connections = []
        self.listener_thread = threading.Thread(target=self._accept_datagrams)
        self.shutdown_event = threading.Event()
        if self.capture:
            if self.capture.replay:
                self.replay_thread = threading.Thread(target=self._replay_capture)
                self.stream = self.capture.read_stream()
            else:
                self.capture_thread = threading.Thread(target=self._save_capture)
                self.captured_stream = []

    def start(self):
        self.tracker_socket.bind((self.host, self.port))

        print(f"[Socket] Listening on {self.host}:{self.port}")
        self.listener_thread.start()
        if self.capture:
            if self.capture.replay:
                self.replay_thread.start()
            else:
                self.capture_thread.start()

    def stop(self):
        self.shutdown_event.set()
        self.tracker_socket.close()
        self.listener_thread.join()
        if self.capture:
            if self.capture.replay:
                self.replay_thread.join()
            else:
                self.capture_thread.join()
                self._save_capture()

    def _accept_datagrams(self):
        while not self.shutdown_event.is_set():
            try:
                data, _ = self.tracker_socket.recvfrom(1024)
                data = json.loads(data.decode('utf-8'))
                self.tracker.update_drone(id=data['id'], measurements=data['measurements'], ground_truth=data['ground_truth'] if 'ground_truth' in data else None)
                if self.capture and not self.capture.replay:
                    self.captured_stream.append((time.time(), data))
            except Exception as e:
                if self.shutdown_event.is_set():
                    break
                else:
                    raise

    def _save_capture(self):
        if not self.shutdown_event.is_set():
            self.capture.write_stream(self.captured_stream)
            time.sleep(1)
            self._save_capture()

    def _replay_capture(self):
        for i in range(len(self.stream)):
            if self.shutdown_event.is_set():
                break
            curr_time, data = self.stream[i]
            if len(data['measurements']) != 4:  # Skip dropped packets
                continue
            self.tracker.update_drone(id=data['id'], measurements=data['measurements'], ground_truth=data['ground_truth'] if 'ground_truth' in data else None)
            if i+1 < len(self.stream):
                next_time, _ = self.stream[i+1]
                time.sleep(next_time - curr_time)
