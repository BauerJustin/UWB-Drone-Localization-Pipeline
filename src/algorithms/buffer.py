import numpy as np
from src.utils import Position, Measurements
import copy

class Buffer:
    def __init__(self, base_type, size, filter_outliers=False, outlier_rejection_version="V2", outlier_replacement=False):
        self.base_type = base_type
        self.buffer = []
        self.filtered_buffer = []
        self.size = size
        self.filter_outliers = filter_outliers
        self.outlier_rejection_version = outlier_rejection_version
        self.outlier_replacement = outlier_replacement
        self.last_added = None
    
    def add(self, value):
        self.buffer.append(value)
        self.last_added = value
        if len(self.buffer) > self.size:
            self.buffer.pop(0)

    def _add_to_filtered_buffer(self, value):
        self.filtered_buffer.append(value)
        if len(self.filtered_buffer) > self.size:
            self.filtered_buffer.pop(0)

    def get_last(self):
        if self.filter_outliers:
            if self.outlier_rejection_version == "V1":
                self._filter_outliers_V1()
                if len(self.filtered_buffer) == 0:
                    return None
                value = self.filtered_buffer[-1]
                if value.unpack() != self.last_added.unpack():
                    return None
                return value
            elif self.outlier_rejection_version == "V2":
                self._filter_outliers_V2()
                if len(self.filtered_buffer) == 0:
                    return None
                return self.filtered_buffer[-1]
        else:
            return self.buffer[-1]
    
    def get_avg(self):
        if self.outlier_rejection_version == "V1":
            self._filter_outliers_V1()
        elif self.outlier_rejection_version == "V2":
            self._filter_outliers_V2()

        values = np.array([p.unpack() for p in (self.filtered_buffer if self.filter_outliers else self.buffer)])
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

    def _filter_outliers_V1(self):
        values = np.array([p.unpack() for p in self.buffer])
        median = np.median(values, axis=0)
        deviation = np.median(np.abs(values - median), axis=0)
        threshold = 3 * deviation
        self.filtered_buffer = [p for p in self.buffer if np.all(np.abs(np.array(p.unpack()) - median) <= threshold)]

    def _filter_outliers_V2(self):
        new_val = np.array(self.buffer[-1].unpack())
        if any(val < 0 or val > 5 for val in new_val):
            if self.outlier_replacement:
                replaced_measurements = self._replace_outlier(copy.copy(self.buffer[-1]))
                if replaced_measurements is not None:
                    self._add_to_filtered_buffer(replaced_measurements)
        else:
            self._add_to_filtered_buffer(self.buffer[-1])
        
    def _replace_outlier(self, measurements):
        # Currently only replaces values for measurements with single outliers
        #TODO: replace values of multiple outliers
        #TODO: Use historical values for better replacement

        outlier_data = np.array(measurements.unpack())
        num_outliers = len([val for val in outlier_data if val < 0 or val > 5]) 
        if num_outliers == 1:
            outlier_data[(outlier_data < 0) | (outlier_data > 5)] = np.nan
            missing_indices = np.isnan(outlier_data)
            indices = np.arange(len(outlier_data))
            known_indices = indices[~missing_indices]
            known_values = outlier_data[~missing_indices]

            interpolation_function = np.polyfit(known_indices, known_values, 2)

            interpolated_values = np.polyval(interpolation_function, indices)
            replaced_val = np.where(missing_indices, interpolated_values, outlier_data)

            measurements.update(*replaced_val)

            return measurements    
        else:
            return None