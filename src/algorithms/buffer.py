import numpy as np
from src.utils import Position, Measurements


class Buffer:
    def __init__(self, base_type, size, filter_outliers=False):
        self.base_type = base_type
        self.buffer = []
        self.size = size
        self.filter_outliers = filter_outliers
        self.last_added = None
    
    def add(self, value):
        self.buffer.append(value)
        self.last_added = value
        if len(self.buffer) > self.size:
            self.buffer.pop(0)

    def get_last(self):
        if self.filter_outliers:
            filtered_buffer = self._filter_outliers()
            if len(filtered_buffer) == 0:
                return None
            value = filtered_buffer[-1]
            if value.unpack() != self.last_added.unpack():
                return None
            return value
        else:
            return self.buffer[-1]

    def get_avg(self):
        values = np.array([p.unpack() for p in (self._filter_outliers() if self.filter_outliers else self.buffer)])
        avg_value = np.mean(values, axis=0)
        if self.base_type == 'pos':
            return Position(*avg_value)
        elif self.base_type == 'measurement':
            return Measurements(*avg_value)
        else:
            raise Exception(f"Invalid buffer base: {self.base_type}")
        
    def get_buffer_variance(self):
        values = np.array([p.unpack() for p in self.buffer])
        median = np.median(values, axis=0)
        deviation = np.median(np.abs(values - median), axis=0)
        return deviation

    def _filter_outliers(self):
        values = np.array([p.unpack() for p in self.buffer])
        median = np.median(values, axis=0)
        deviation = np.median(np.abs(values - median), axis=0)
        threshold = 3 * deviation
        filtered_buffer = [p for p in self.buffer if np.all(np.abs(np.array(p.unpack()) - median) <= threshold)]
        return filtered_buffer
