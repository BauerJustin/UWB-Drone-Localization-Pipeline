import argparse

class Parser:
    def parse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--sim_uwb", help="Enable simulated drone input data", action="store_true")
        parser.add_argument("--num_drones", help="Specify number of drones", default=3)
        parser.add_argument("--capture", help="Capture all incoming data", action="store_true")
        parser.add_argument("--replay", help="Replay capture file", action="store_true")
        parser.add_argument("--file_name", help="Set capture file (default=capture.json)", default="capture.json")
        args = parser.parse_args()
        self._validate_args(args)
        return args

    def _validate_args(self, args):
        if args.sim_uwb and args.replay:
            raise Exception("Can not Simulate UWB and Replay at the same time")
        if args.capture and args.replay:
            raise Exception("Can not Capture and Replay at the same time")
        