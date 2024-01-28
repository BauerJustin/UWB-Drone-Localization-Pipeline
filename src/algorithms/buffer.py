import numpy as np
from src.utils import Position, Measurements

class Buffer:
    def __init__(self, base_type, size):
        self.base_type = base_type
        self.buffer = []
        self.size = size
    
    def add(self, value):
        self.buffer.append(value)
        if len(self.buffer) > self.size:
            self.remove(0)
            
    def remove(self, index=0):
        self.buffer.pop(index)

    def get_value(self, index):
        return self.buffer[index] if self.buffer else None
    
    def get_last(self):
        return self.buffer[-1] if self.buffer else None

    def get_avg(self):
        values = np.array([p.unpack() for p in self.buffer])
        avg_value = np.mean(values, axis=0)
        if self.base_type == 'pos':
            return Position(*avg_value)
        elif self.base_type == 'measurement':
            return Measurements(*avg_value)
        else:
            raise Exception(f"Invalid buffer base: {self.base_type}")

    def get_variance(self):
        values = np.array([p.unpack() for p in self.buffer])
        median = np.median(values, axis=0)
        deviation = np.median(np.abs(values - median), axis=0)
        return deviation
    
    def __len__(self):
        return len(self.buffer)
    