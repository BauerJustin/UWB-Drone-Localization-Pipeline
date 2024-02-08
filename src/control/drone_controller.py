import threading
from djitellopy import Tello
import time
import socket

class DroneController:
    def __init__(self):
        self.response = None

    def start(self):
        print(f"[Controller] Started")
        drone_thread1 = threading.Thread(target=self._drone_swarm('wlx00265a6b00ff', 1))
        drone_thread2 = threading.Thread(target=self._drone_swarm('wlx00265a6afa9d', 2))
        drone_thread3 = threading.Thread(target=self._drone_swarm('wlp3s0', 3))

        drone_thread1.start()
        drone_thread2.start()
        drone_thread3.start()


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

    def _get_response(self, socket, command):
        self.response = socket.recv(3000)
        print(f'Command: {command}; socket response: {self.response}')
        if self.response is None:
            self.response = "none response"
        else:
            self.response = self.response.decode("utf-8")
        print(f'Command: {command}; decoded response: {self.response}')
        self.response = None
        
    def _drone_swarm(self, wifi, num):
        print(f'Drone {num} Thread Started')
        drone1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        drone1.setsockopt(socket.SOL_SOCKET, 25, wifi.encode())
        
        drone1.sendto('command'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        drone1.sendto('takeoff'.encode("utf-8"), 0, ('192.168.10.1', 8889))
#        self._get_response(drone1, "takeoff")
        
        drone1.sendto('command'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        drone1.sendto('flip f'.encode("utf-8"), 0, ('192.168.10.1', 8889))
#        self._get_response(drone1, "forward 50")

        drone1.sendto('command'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        drone1.sendto('flip b'.encode("utf-8"), 0, ('192.168.10.1', 8889))
#        self._get_response(drone1, "back 50")

#        time.sleep(2)       
        drone1.sendto('command'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        drone1.sendto('land'.encode("utf-8"), 0, ('192.168.10.1', 8889))
#        self._get_response(drone1, "land")

#        time.sleep(2)
        print(f'Drone {num} Thread Stopped')
    
    def _drone_swarm_2(self):
        print("Drone 2 Thread Started")
        drone2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        drone2.setsockopt(socket.SOL_SOCKET, 25, 'wlx00265a6afa9d'.encode())
        
        drone2.sendto('command'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        drone2.sendto('takeoff'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        time.sleep(2)

#        drone2.sendto('command'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        drone2.sendto('land'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        time.sleep(2)
        print("Drone 2 Thread Stopped")
    
    def _drone_swarm_3(self):
        print("Drone 3 Thread Started")
        drone2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        drone2.setsockopt(socket.SOL_SOCKET, 25, 'wlp3s0'.encode())
        
        drone2.sendto('command'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        drone2.sendto('takeoff'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        time.sleep(2)

#        drone2.sendto('command'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        drone2.sendto('land'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        time.sleep(2)
        print("Drone 3 Thread Stopped")

