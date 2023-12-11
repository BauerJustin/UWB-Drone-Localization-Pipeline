import numpy as np
from src.utils import Position


class Buffer:
    def __init__(self, size, filter_outliers=False):
        self.buffer = []
        self.size = size
        self.filter_outliers = filter_outliers
        self.last_added = None
    
    def add(self, position):
        self.buffer.append(position)
        self.last_added = position
        if len(self.buffer) > self.size:
            self.buffer.pop(0)            

    def get_last_pos(self):
        if self.filter_outliers:
            pos = self._filter_outliers()[-1]
            if pos.unpack() != self.last_added.unpack():
                return None
            return pos
        else:
            return self.buffer[-1]
    
    def get_avg_pos(self):
        if self.filter_outliers:
            poses = np.array([p.unpack() for p in self._filter_outliers()])
            avg_pos = np.mean(poses, axis=0)
            return Position(*avg_pos)
        else:
            poses = np.array([p.unpack() for p in self.buffer])
            avg_pos = np.mean(poses, axis=0)
            return Position(*avg_pos)

    def _filter_outliers(self):
        pos_list = np.array([pos.unpack() for pos in self.buffer])
        median = np.median(pos_list, axis=0)
        deviation = np.median(np.abs(pos_list - median), axis=0)
        threshold = 3 * deviation
        filtered_buffer = [pos for pos in self.buffer if np.all(np.abs(np.array(pos.unpack()) - median) <= threshold)]
        return filtered_buffer
    