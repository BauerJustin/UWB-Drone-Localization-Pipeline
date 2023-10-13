import argparse

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sim_uwb", help="Enable simulated drone input data", action="store_true")
    parser.add_argument("--num_drones", help="Specify number of drones", default=3)
    args = parser.parse_args()
    return args
