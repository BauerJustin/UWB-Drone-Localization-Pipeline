import copy
import threading
import time
from .drone_socket import DroneSocket
from .drone_orchestrator import DroneOrchestrator
from src.devices import AnchorNetwork, Drone
from src.utils import load_config, Measurements
from src import constants as const


class DroneTracker:
    def __init__(self, capture=None, orchestrator=const.ORCHESTRATOR):
        if orchestrator:
            self.socket = DroneOrchestrator(tracker=self)
        else:
            self.socket = DroneSocket(tracker=self)
        self.drones = {}

        self.anchor_network = AnchorNetwork()
        anchors = load_config.load_anchor_positions()
        for anchor_id, pos in anchors.items():
            self.anchor_network.add_anchor(anchor_id, **pos)

        self.dropped_count = 0

        self.capture = capture
        self.history = False
        if self.capture:
            self.shutdown_event = threading.Event()
            if self.capture.replay:
                self.replay_thread = threading.Thread(target=self._replay_capture)
                self.stream = self.capture.read_stream()
                if not self.capture.live:
                    self.history = True
                    self.drones_history = {}
            else:
                self.capture_thread = threading.Thread(target=self._save_capture)
                self.captured_stream = []            

    def start(self):
        self.socket.start()
        if self.capture:
            if self.capture.replay:
                self.replay_thread.start()
            else:
                self.capture_thread.start()
        print(f"[Tracker] Started")

    def stop(self):
        self.socket.stop()
        if self.capture:
            self.shutdown_event.set()
            if self.capture.replay:
                self.replay_thread.join()
            else:
                self.capture_thread.join()
                self._save_capture()
        print("[Tracker] Terminated by user")

    def update_drone(self, data):
        id, measurements, timestamp, ground_truth = data['id'], data['measurements'], data['timestamp'], data.get('ground_truth')
        if len(data['measurements']) == 4:
            if id not in self.drones:
                self._add_drone(id)
            self.drones[id].update_pos(measurements=Measurements(*[m for _, m in sorted(measurements.items(), key=lambda x: int(x[0]))], t=timestamp), ground_truth=ground_truth)
            if self.capture and not self.capture.replay:
                self.captured_stream.append((timestamp, data))
            if self.history and self.drones[id].active:
                self.drones_history[id].append(copy.copy(self.drones[id].pos))
        else:
            print(f'[Tracker] Drone {id} Invalid measurements len = {len(measurements)}, dropping packet')
            self.dropped_count += 1

    def _add_drone(self, id):
        self.drones[id] = Drone(id=id, anchor_network=self.anchor_network)
        if self.history:
            self.drones_history[id] = []

    def _save_capture(self):
        if not self.shutdown_event.is_set():
            self.capture.write_stream(self.captured_stream)
            time.sleep(1)
            self._save_capture()

    def _replay_capture(self):
        self.stream = sorted(self.stream, key=lambda x: x[0])
        for i in range(len(self.stream)):
            if self.shutdown_event.is_set():
                break
            curr_time, data = self.stream[i]
            data['timestamp'] = curr_time  # TODO: Temp fix
            self.update_drone(data)
            if self.capture.live and i+1 < len(self.stream):
                next_time, _ = self.stream[i+1]
                time.sleep(next_time - curr_time)
