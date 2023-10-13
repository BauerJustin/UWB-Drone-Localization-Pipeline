import time
from src.simulator import UWBNetworkSimulator
from src.utils import arg_parser

def main():
    args = arg_parser.parse()

    if args.sim_uwb:
        print(f"Starting UWB simulator with {args.num_drones} drones")
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
            print("UWB simulator stopped")

if __name__ == "__main__":
    main()