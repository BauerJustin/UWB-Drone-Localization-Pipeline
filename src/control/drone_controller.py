import threading
from djitellopy import Tello
import time
import socket
import multiprocessing

class DroneController:
    def __init__(self):
        self.response = None

        self.drone_process_1 = multiprocessing.Process(target=self._drone_swarm_test, args=('wlx00265a6b00ff', 1))
        self.drone_process_2 = multiprocessing.Process(target=self._drone_swarm_test, args=('wlx00265a6afa9d', 2))
        self.drone_process_3 = multiprocessing.Process(target=self._drone_swarm_test,  args=('wlp3s0', 3))

        # self.drone_process_1 = multiprocessing.Process(target=self._drone_swarm)
        # self.drone_process_2 = multiprocessing.Process(target=self._drone_swarm_2)
        # self.drone_process_3 = multiprocessing.Process(target=self._drone_swarm_3)

        # self.drone_thread1 = threading.Thread(target=self._drone_swarm_test('wlx00265a6b00ff', 1))
        # self.drone_thread2 = threading.Thread(target=self._drone_swarm_test('wlx00265a6afa9d', 2))
        # self.drone_thread3 = threading.Thread(target=self._drone_swarm_test('wlp3s0', 3))

        # self.drone_thread1 = threading.Thread(target=self._drone_swarm())
        # self.drone_thread2 = threading.Thread(target=self._drone_swarm_2())
        # self.drone_thread3 = threading.Thread(target=self._drone_swarm_3())

    def start(self):
        print(f"[Controller] Started")
        self.drone_process_1.start()
        self.drone_process_2.start()
        self.drone_process_3.start()

        # self.drone_thread1.start()
        # self.drone_thread2.start()
        # self.drone_thread3.start()

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
        if self.response is None:
            self.response = "none response"
        else:
            self.response = self.response.decode("utf-8")
            self.response = self.response.rstrip("\r\n")
        print(f'Command: {command} \n\t decoded response: {self.response}')
        self.response = None

    def _drone_tag_calibration(self, wifi, num):
        print(f'Drone-tag {num} calibration started')
        drone1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        drone1.setsockopt(socket.SOL_SOCKET, 25, wifi.encode())
        
        drone1.sendto('command'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        drone1.sendto('takeoff'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        drone1.sendto('land'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        print(f'Drone-tag {num} calibration stopped')

    def _drone_swarm_test(self, wifi, num):
        print(f'Drone {num} Thread Started')
        drone1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        drone1.setsockopt(socket.SOL_SOCKET, 25, wifi.encode())
        
        drone1.sendto('command'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        drone1.sendto('takeoff'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        time.sleep(2) # Wait for all 3 drones to takeoff

        command = "speed 10"
        drone1.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
        
        for i in range(3):
            command = f'rc 0 30 0 0'
            drone1.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
            time.sleep(2)
            command = "rc 0 0 0 0"
            drone1.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
            time.sleep(1)
        time.sleep(5)

        for i in range(3):
            command = f'rc 0 -30 0 0'
            drone1.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
            time.sleep(2)
            command = "rc 0 0 0 0"
            drone1.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
            time.sleep(1)
        time.sleep(5)

        drone1.sendto('land'.encode("utf-8"), 0, ('192.168.10.1', 8889))

        print(f'Drone {num} Thread Stopped')
    
    def _drone_swarm(self):
        print(f'Drone 1 Thread Started')
        drone1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        drone1.setsockopt(socket.SOL_SOCKET, 25, 'wlx00265a6b00ff'.encode())
        
        drone1.sendto('command'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        drone1.sendto('takeoff'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        time.sleep(2) # Wait for all 3 drones to takeoff

        command = "speed 10"
        drone1.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
        
        for i in range(3):
            command = f'rc 0 30 0 0'
            drone1.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
            time.sleep(2)
            command = "rc 0 0 0 0"
            drone1.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
            time.sleep(1)
        time.sleep(5)

        for i in range(3):
            command = f'rc 0 -30 0 0'
            drone1.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
            time.sleep(2)
            command = "rc 0 0 0 0"
            drone1.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
            time.sleep(1)
        time.sleep(5)

        # command = "rc 0 70 0 0" 
        # drone1.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
        # time.sleep(2)

        # command = "rc 0 0 0 0"
        # drone1.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
        # time.sleep(7)

        # command = "rc 0 0 0 0"
        # drone1.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
        # time.sleep(3) # localization pause
        
        # command = "rc 0 -70 0 0"
        # drone1.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
        # time.sleep(7)

        # command = "rc 0 0 0 0"
        # drone1.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
        # time.sleep(3) # localization pause

    #    command = "rc 0 -50 0 0"
    #    drone1.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))

    #    time.sleep(2)
    #    command = "rc 0 0 0 0"
    #    drone1.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))

        drone1.sendto('land'.encode("utf-8"), 0, ('192.168.10.1', 8889))

        print(f'Drone 1 Thread Stopped')
    
    def _drone_swarm_2(self):
        print("Drone 2 Thread Started")
        drone2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        drone2.setsockopt(socket.SOL_SOCKET, 25, 'wlx00265a6afa9d'.encode())
        
        drone2.sendto('command'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        drone2.sendto('takeoff'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        time.sleep(2) # Wait for all 3 drones to takeoff

        command = "speed 10"
        drone1.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))

        for i in range(3):
            command = f'rc 0 30 0 0'
            drone2.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
            time.sleep(2)
            command = "rc 0 0 0 0"
            drone2.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
            time.sleep(1)
        time.sleep(5)

        for i in range(3):
            command = f'rc 0 -30 0 0'
            drone2.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
            time.sleep(2)
            command = "rc 0 0 0 0"
            drone2.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
            time.sleep(1)
        time.sleep(5)

        # command = "rc 0 0 75 0"
        # drone2.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
        # time.sleep(2)
        
        # command = "rc 0 0 0 0"
        # drone2.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))

        # command = "rc 0 50 0 0"
        # drone2.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
        # time.sleep(2)

        # command = "rc 0 0 0 0"
        # drone2.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))

        # command = "rc 0 -50 0 0"
        # drone2.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
        # time.sleep(2)
        
        # command = "rc 0 0 0 0"
        # drone2.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))

        drone2.sendto('land'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        print("Drone 2 Thread Stopped")
    
    def _drone_swarm_3(self):
        print("Drone 3 Thread Started")
        drone3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        drone3.setsockopt(socket.SOL_SOCKET, 25, 'wlp3s0'.encode())
        
        drone3.sendto('command'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        drone3.sendto('takeoff'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        time.sleep(2) # Wait for all 3 drones to takeoff

        command = "speed 10"
        drone1.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))

        for i in range(3):
            command = f'rc 0 30 0 0'
            drone3.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
            time.sleep(2)
            command = "rc 0 0 0 0"
            drone3.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
            time.sleep(1)
        time.sleep(5)

        for i in range(3):
            command = f'rc 0 -30 0 0'
            drone3.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
            time.sleep(2)
            command = "rc 0 0 0 0"
            drone3.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
            time.sleep(1)
        time.sleep(5)

        # command = "rc 0 0 75 0"
        # drone3.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
        # time.sleep(2)
                
        # command = "rc 0 0 0 0"
        # drone3.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))

        # command = "rc 0 50 0 0"
        # drone3.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
        # time.sleep(2)
        
        # command = "rc 0 0 0 0"
        # drone3.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))

        # command = "rc 0 -50 0 0"
        # drone3.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))
        # time.sleep(2)
        
        # command = "rc 0 0 0 0"
        # drone3.sendto(command.encode("utf-8"), 0, ('192.168.10.1', 8889))

        drone3.sendto('land'.encode("utf-8"), 0, ('192.168.10.1', 8889))
        print("Drone 3 Thread Stopped")
