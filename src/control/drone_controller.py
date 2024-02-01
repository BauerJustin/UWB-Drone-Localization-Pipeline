import threading
from djitellopy import Tello
import time
import socket

class DroneController:
    def __init__(self):
        pass

    def start(self):
        print(f"[Controller] Started")
        drone_thread1 = threading.Thread(target=self._drone_swarm)
        drone_thread2 = threading.Thread(target=self._drone_swarm)
        drone_thread3 = threading.Thread(target=self._drone_swarm)
        drone_thread1.start()
        drone_thread2.start()
        drone_thread3.start()

    def _move_drone(self):
        tello = Tello()
        tello.connect()
        print("Battery:", tello.get_battery(), "%")

        tello.takeoff()
        tello.move_up(40)
        tello.move_down(40)
        time.sleep(30)
        # tello.flip_right()
        # tello.move_left(20)
        # tello.move_forward(100)
        # tello.move_back(100)

        tello.land()
        tello.end()

    def _drone_swarm(self):
        drone = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        drone.sendto('command'.encode(), 0, ('192.168.10.1', 8889))
        drone.sendto('takeoff'.encode(), 0, ('192.168.10.1', 8889))
        time.sleep(5)
        drone.sendto('command'.encode(), 0, ('192.168.10.1', 8889))
        drone.sendto('land'.encode(), 0, ('192.168.10.1', 8889))
