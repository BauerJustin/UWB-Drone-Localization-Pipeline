import copy
import math
import random


TRAJECTORY_PERCENTAGE_CHANGE = 0.01  # 1%

class LinearTrajectory:
    def __init__(self, anchors):
        self.anchors = anchors
        
        self.min_values = {
            "x": min(anchor["x"] for anchor in self.anchors.values()),
            "y": min(anchor["y"] for anchor in self.anchors.values()),
            "z": min(anchor["z"] for anchor in self.anchors.values())
        }

        self.max_values = {
            "x": max(anchor["x"] for anchor in self.anchors.values()),
            "y": max(anchor["y"] for anchor in self.anchors.values()),
            "z": max(anchor["z"] for anchor in self.anchors.values())
        }

        # Set random initial and final positions within their respective bounds
        self.initial_position = {
            "x": random.uniform(self.min_values["x"], self.max_values["x"]),
            "y": random.uniform(self.min_values["y"], self.max_values["y"]),
            "z": random.uniform(self.min_values["z"], self.max_values["z"])
        }
        self.position = copy.copy(self.initial_position)

        self.final_position = {
            "x": random.uniform(self.min_values["x"], self.max_values["x"]),
            "y": random.uniform(self.min_values["y"], self.max_values["y"]),
            "z": random.uniform(self.min_values["z"], self.max_values["z"])
        }

    def get_measurements(self):
        measurements = {}
        for anchor_name, anchor in self.anchors.items():
            distance = ((self.position["x"] - anchor["x"])**2 +
                        (self.position["y"] - anchor["y"])**2 +
                        (self.position["z"] - anchor["z"])**2)**0.5
            measurements[anchor_name] = distance

        ground_truth = copy.copy(self.position)

        # update pos each time by percentage
        for axis in ["x", "y", "z"]:
            difference = self.final_position[axis] - self.initial_position[axis]
            self.position[axis] += TRAJECTORY_PERCENTAGE_CHANGE * difference

        # randomize near position to move to
        squared_diffs = math.sqrt(sum([(self.final_position[key] - self.position[key]) ** 2 for key in self.position]))
        if squared_diffs < 0.001:
            self.initial_position = copy.copy(self.position)
            self.final_position = {
                "x": random.uniform(self.min_values["x"], self.max_values["x"]),
                "y": random.uniform(self.min_values["y"], self.max_values["y"]),
                "z": random.uniform(self.min_values["z"], self.max_values["z"])
            }

        return measurements, ground_truth
