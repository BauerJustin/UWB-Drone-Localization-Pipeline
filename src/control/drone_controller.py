import threading
from djitellopy import Tello
import time
import socket

class DroneController:
    def __init__(self):
        pass

    def start(self):
        print(f"[Controller] Started")
        drone_thread1 = threading.Thread(target=self._drone_swarm_1)
        drone_thread2 = threading.Thread(target=self._drone_swarm_2)
#        drone_thread3 = threading.Thread(target=self._drone_swarm)
        drone_thread1.start()
        drone_thread2.start()
#        drone_thread3.start()

    def _move_drone(self):
        tello = Tello()
        tello.connect()
        print("Battery:", tello.get_battery(), "%")

        tello.takeoff()
#        tello.move_up(40)
#        tello.move_down(40)
#        time.sleep(30)
        # tello.flip_right()
        # tello.move_left(20)
        # tello.move_forward(100)
        # tello.move_back(100)

        tello.land()
        tello.end()

    def _drone_swarm_1(self):
        drone2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      
        drone2.setsockopt(socket.SOL_SOCKET, 2, 'wlx00265a6b00ff'.encode("utf-8"))
        drone2.sendto('command'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        
        drone2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        drone2.setsockopt(socket.SOL_SOCKET, 2, 'wlx00265a6b00ff'.encode("utf-8"))
        drone2.sendto('takeoff'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        time.sleep(5)

        drone2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        drone2.setsockopt(socket.SOL_SOCKET, 2, 'wlx00265a6b00ff'.encode("utf-8"))        
        drone2.sendto('command'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        
        drone2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        drone2.setsockopt(socket.SOL_SOCKET, 2, 'wlx00265a6b00ff'.encode("utf-8"))
        drone2.sendto('land'.encode("utf-8"), 0, ('192.168.10.1', 8889))
    
    def _drone_swarm_2(self):
        drone = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        drone.setsockopt(socket.SOL_SOCKET, 2, 'wlx00265a6afa9d'.encode("utf-8"))
        drone.sendto('command'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        
        drone = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        drone.setsockopt(socket.SOL_SOCKET, 2, 'wlx00265a6afa9d'.encode("utf-8"))
        drone.sendto('takeoff'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        time.sleep(5)

        drone = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        drone.setsockopt(socket.SOL_SOCKET, 2, 'wlx00265a6afa9d'.encode("utf-8"))        
        drone.sendto('command'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        
        drone = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        drone.setsockopt(socket.SOL_SOCKET, 2, 'wlx00265a6afa9d'.encode("utf-8"))
        drone.sendto('land'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        
    
