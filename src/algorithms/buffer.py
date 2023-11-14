import numpy as np
from src.utils import Position


class Buffer:
    def __init__(self, size, filter_outliers=False, min_filter_len=0):
        self.buffer = []
        self.size = size
        self.filter_outliers = filter_outliers
        self.min_filter_len = min_filter_len
    
    def add(self, position):
        self.buffer.append(position)
        if len(self.buffer) > self.size:
            self.buffer.pop(0)
        if self.filter_outliers and len(self.buffer) >= self.min_filter_len:
            self._filter_outliers()

    def get_last_pos(self):
        return self.buffer[-1]
    
    def get_avg_pos(self):
        poses = np.array([p.unpack() for p in self.buffer])
        avg_pos = np.mean(poses, axis=0)
        return Position(*avg_pos)

    def _filter_outliers(self):
        pos_list = np.array([pos.unpack() for pos in self.buffer])
        median = np.median(pos_list, axis=0)
        deviation = np.median(np.abs(pos_list - median), axis=0)
        threshold = 3 * deviation
        self.buffer = [pos for pos in self.buffer if np.all(np.abs(np.array(pos.unpack()) - median) <= threshold)]
    