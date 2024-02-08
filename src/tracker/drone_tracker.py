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

        self.dropped_measurements = 0
        self.last_measurements = {}

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
        
        self.logger = load_config.setup_logger(__name__)

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
        if id not in self.drones:
            self._add_drone(id)
        if const.FILTER_DUPLICATE_MEASUREMENTS:
            measurements = self._filter_measurements(measurements)
        if len(measurements) != 4:
            self.dropped_measurements += 4 - len(measurements)
            dropped_anchors = []
            for anchor_id in self.anchor_network.get_anchor_ids():
                if anchor_id not in measurements:
                    dropped_anchors.append(anchor_id)
            print(f'[Tracker] Drone {id} dropped anchors: {dropped_anchors}')
            if const.DROP_PARTIAL_MEASUREMENTS:
                print(f'[Tracker] Drone {id} Invalid measurements len = {len(measurements)}, dropping packet')
                return
        self.drones[id].update_pos(measurements=self._create_measurements(measurements, timestamp), ground_truth=ground_truth)
        if self.capture and not self.capture.replay:
            self.captured_stream.append((time.time(), data))
        if self.history and self.drones[id].active:
            self.drones_history[id].append(copy.copy(self.drones[id].pos))

    def _add_drone(self, id):
        self.drones[id] = Drone(id=id, anchor_network=self.anchor_network)
        if self.history:
            self.drones_history[id] = []

    def _create_measurements(self, measurements, timestamp):
        return Measurements(*[measurements[anchor_id] if anchor_id in measurements else None for anchor_id in self.anchor_network.get_anchor_ids()], t=timestamp)

    def _save_capture(self):
        try:
            if not self.shutdown_event.is_set():
                self.capture.write_stream(self.captured_stream)
                time.sleep(1)
                self._save_capture()
        except Exception as e:
            print(f"[Tracker] Save capture failed: {e}")

    def _filter_measurements(self, measurements):
        filtered_measurements = {}
        for anchor_id, measurement in measurements.items():
            if anchor_id not in self.last_measurements or self.last_measurements[anchor_id] != measurement:
                filtered_measurements[anchor_id] = measurement
            self.last_measurements[anchor_id] = measurement
        return filtered_measurements
    
    def _replay_capture(self):
        try:
            for i in range(len(self.stream)):
                if self.shutdown_event.is_set():
                    break
                curr_time, data = self.stream[i]
                if 'timestamp' not in data:
                    data['timestamp'] = curr_time
                self.update_drone(data)
                if self.capture.live and i+1 < len(self.stream):
                    next_time, _ = self.stream[i+1]
                    time.sleep(next_time - curr_time)
        except Exception as e:
            print(f"[Tracker] Replay capture failed: {e}")
