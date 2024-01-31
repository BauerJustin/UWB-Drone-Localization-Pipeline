import sys
sys.path.append('.')
import time
from src.tracker import DroneTracker
from src.utils import Parser, StreamCapture, AccuracyAnalyzer

def main():
    args = Parser().parse()
    
    capture = StreamCapture(args.file_name, replay=True, live=False)

    tracker = DroneTracker(capture=capture)
    tracker.start()
    time.sleep(3)
    tracker.stop()

    analyzer = AccuracyAnalyzer(tracker, static=args.static, linear=args.linear)
    analyzer.evaluate_accuracy()

if __name__ == "__main__":
    main()
