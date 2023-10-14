from src.simulator import UWBNetworkSimulator
from src.tracker import DroneTracker
from src.utils import arg_parser

def main():
    args = arg_parser.parse()

    if args.sim_uwb:
        simulator = UWBNetworkSimulator(num_drones=int(args.num_drones))
        simulator.start()

    try:
        tracker = DroneTracker()
        tracker.start()
            
    except KeyboardInterrupt:
        if args.sim_uwb:
            simulator.stop()
        tracker.stop()

if __name__ == "__main__":
    main()