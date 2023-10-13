from src.utils import arg_parser
from src.simulator import UWBNetworkSimulator
import time

def main():
    args = arg_parser.parse()

    if args.sim_uwb:
        print(f"Starting UWB simulator: {args.num_drones}")
        simulator = UWBNetworkSimulator(num_drones=args.num_drones)
        simulator.start()

    try:
        while True:
            print("Loop")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Terminated by user")
        if args.sim_uwb:
            simulator.stop()
            print("UWB Simulator stopped")

if __name__ == "__main__":
    main()