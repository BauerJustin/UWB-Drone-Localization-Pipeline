import time
from src.tracker import DroneTracker
from src.utils import Parser, StreamCapture
from src.visualization import Visualizer

def main():
    args = Parser().parse()
    
    capture = StreamCapture(args.file_name, replay=True, live=False)

    tracker = DroneTracker(capture=capture)
    tracker.start()
    time.sleep(3)
    tracker.stop()

    visualizer = Visualizer(tracker)
    visualizer.plot_history(plot_best_fit=True)

if __name__ == "__main__":
    main()