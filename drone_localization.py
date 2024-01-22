from src.simulator import UWBNetworkSimulator
from src.tracker import DroneTracker
from src.utils import Parser, StreamCapture
from src.visualization import Visualizer

def main():
    args = Parser().parse()

    if args.sim_uwb:
        simulator = UWBNetworkSimulator(num_drones=int(args.num_drones))
        simulator.start()
    
    capture = None
    if args.capture or args.replay:
        capture = StreamCapture(args.file_name, replay=args.replay)

    try:
        tracker = DroneTracker(capture=capture, orchestrator=False)
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