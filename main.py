from src.control import DroneController
from src.simulator import UWBNetworkSimulator
from src.tracker import DroneTracker
from src.utils import arg_parser, StreamCapture
from src.visualization import Visualizer

def main():
    args = arg_parser.parse()

    if args.sim_uwb:
        simulator = UWBNetworkSimulator(num_drones=int(args.num_drones))
        simulator.start()
    
    capture = None
    if args.capture or args.replay:
        if args.capture and args.replay:
            raise Exception("Can not Capture and Replay at the same time")
        capture = StreamCapture(args.file_name, replay=args.replay)

    try:
        tracker = DroneTracker(capture=capture)
        tracker.start()
        
        controller = DroneController()
        controller.start()

        visualizer = Visualizer(tracker)
        visualizer.start()

    except KeyboardInterrupt:
        if args.sim_uwb:
            simulator.stop()
        tracker.stop()
        visualizer.stop()

if __name__ == "__main__":
    main()