from src.simulator import UWBNetworkSimulator
from src.tracker import DroneTracker
from src.utils import arg_parser
from src.visualization import Visualizer

def main():
    args = arg_parser.parse()

    if args.sim_uwb:
        simulator = UWBNetworkSimulator(num_drones=int(args.num_drones))
        simulator.start()

    try:
        tracker = DroneTracker()
        tracker.start()
        
        visualizer = Visualizer(tracker)
        visualizer.start()

    except KeyboardInterrupt:
        if args.sim_uwb:
            simulator.stop()
        tracker.stop()
        visualizer.stop()

if __name__ == "__main__":
    main()