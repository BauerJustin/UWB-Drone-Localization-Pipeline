from src import constants as const
from src.utils import load_config
from djitellopy import Tello
import time
import socket
import multiprocessing


class DroneController:
    def __init__(self):
        if const.SWARM_MODE:
            self.drone_network, drone_wifi_ids = load_config.load_control_settings()
            self.drone_processes = []
            for i, wifi_id in enumerate(drone_wifi_ids):
                if const.DRONE_CALIBRATION:
                    self.drone_processes.append(multiprocessing.Process(target=self._drone_swarm_calibration, args=(wifi_id, i+1)))
                elif const.DRONE_STATIC:
                    self.drone_processes.append(multiprocessing.Process(target=self._drone_swarm_static, args=(wifi_id, i+1)))
                else:
                    self.drone_processes.append(multiprocessing.Process(target=self._drone_swarm_dynamic, args=(wifi_id, i+1)))

    def start(self):
        print(f"[Controller] Started")
        if const.SWARM_MODE:
            print(f"[Controller] Swarm mode activated")
            for process in self.drone_processes:
                process.start()
        else:
            print(f"[Controller] Single drone activated")
            if const.DRONE_CALIBRATION:
                self._drone_single_calibration()
            elif const.DRONE_STATIC:
                self._drone_single_static()
            else:
                self._drone_single_dynamic()


    def _drone_single_static(self):
        tello = Tello()
        tello.connect()
        print("Battery:", tello.get_battery(), "%")

        tello.takeoff()
        time.sleep(60)

        tello.land()
        tello.end()

    def _drone_single_dynamic(self):
        tello = Tello()
        tello.connect()
        print("Battery:", tello.get_battery(), "%")

        tello.takeoff()
        time.sleep(3) # Wait for system to stabalize localization

        tello.set_speed(10)

        for _ in range(3):
            # tello.move_forward(20)
            tello.send_rc_control(0, 20, 0, 0)
            time.sleep(2)
            tello.send_rc_control(0, 0, 0, 0)
            time.sleep(2)
        time.sleep(5)

        for _ in range(3):
#            tello.move_back(20)
            tello.send_rc_control(0, -20, 0, 0)
            time.sleep(2)
            tello.send_rc_control(0, 0, 0, 0)
            time.sleep(2)
        time.sleep(5)

        tello.land()
        tello.end()


    def _drone_swarm_static(self, wifi, num):
        print(f'Drone {num} Thread Started')
        drone_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        drone_socket.setsockopt(socket.SOL_SOCKET, 25, wifi.encode())
        
        self._drone_socket_send(drone_socket, 'command')
        self._drone_socket_send(drone_socket, 'takeoff')

        for _ in range(30):
            self._drone_socket_send(drone_socket, 'command')
            time.sleep(2)

        self._drone_socket_send(drone_socket, 'land')

        print(f'Drone {num} Thread Stopped')

    def _drone_swarm_dynamic(self, wifi, num):
        print(f'Drone {num} Thread Started')
        drone_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        drone_socket.setsockopt(socket.SOL_SOCKET, 25, wifi.encode())
        
        self._drone_socket_send(drone_socket, 'command')
        self._drone_socket_send(drone_socket, 'takeoff')

        time.sleep(2)   # Wait for all 3 drones to takeoff

        self._drone_socket_send(drone_socket, 'speed 10')
 
        for _ in range(3):
            self._drone_socket_send(drone_socket, 'rc 0 30 0 0')
            time.sleep(2)
            self._drone_socket_send(drone_socket, 'rc 0 0 0 0')
            time.sleep(1)
        time.sleep(5)

        for _ in range(3):
            self._drone_socket_send(drone_socket, 'rc 0 -30 0 0')
            time.sleep(2)
            self._drone_socket_send(drone_socket, 'rc 0 0 0 0')
            time.sleep(1)
        time.sleep(5)

        self._drone_socket_send(drone_socket, 'land')

        print(f'Drone {num} Thread Stopped')

    def _drone_swarm_calibration(self, wifi, num):
        print(f'Drone-tag {num} calibration started')
        drone_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        drone_socket.setsockopt(socket.SOL_SOCKET, 25, wifi.encode())

        self._drone_socket_send(drone_socket, 'command')
        self._drone_socket_send(drone_socket, 'takeoff')
        self._drone_socket_send(drone_socket, 'land')

        print(f'Drone-tag {num} calibration stopped')

    def _drone_single_calibration(self):
        tello = Tello()
        tello.connect()
        print("Battery:", tello.get_battery(), "%")
        tello.takeoff()
        tello.land()
        tello.end()

    def _drone_socket_send(self, drone_socket, command):
        drone_socket.sendto(command.encode("utf-8"), 0, self.drone_network)
