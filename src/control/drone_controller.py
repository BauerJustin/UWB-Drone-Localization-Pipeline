import threading
from djitellopy import Tello

class DroneController:
    def __init__(self):
        pass

    def start(self):
        print(f"[Controller] Started")
        drone_thread = threading.Thread(target=self._move_drone)
        drone_thread.start()

    def _move_drone(self):
        # Initialize the Tello object
        tello = Tello()

        # Connect to the drone
        tello.connect()
        print("Battery:", tello.get_battery(), "%")

        tello.takeoff()

        # Fly a pre-determined linear path
        tello.move_up(20)
        tello.move_forward(20)
        tello.move_back(20)
        tello.move_down(20)

        tello.land()
        tello.end()
