import copy
import numpy as np
from src import constants as const
from src.algorithms import Buffer
from src.utils import load_config

class OutlierRejection:
    def __init__(self, outlier_replacement=False):
        self.outlier_replacement = outlier_replacement
        self.buffer = Buffer(base_type="measurement", size=const.OUTLIER_INTERPOLATION_BUFFER_SIZE)
        self.logger = load_config.setup_logger(__name__)

    def filter_outlier(self, value):
        if any(val and (val < const.NON_OUTLIER_MIN or val > const.NON_OUTLIER_MAX) for val in value.unpack()):
            self.logger.info(f'\t Outlier: {value.unpack()}')
            if self.outlier_replacement and len(self.buffer) >= const.OUTLIER_INTERPOLATION_MIN_BUFFER:
                value = self._replace_outlier(value)
                self.logger.info(f'\t Replaced value: {value.unpack()}')
            else:
                filtered_value = [
                    None if val and (val < const.NON_OUTLIER_MIN or val > const.NON_OUTLIER_MAX) else val
                    for val in value.unpack()
                ]
                value.update(*filtered_value)
        return value
    
    def add_to_buffer(self, value):
        if self.outlier_replacement:
            self.buffer.add(copy.copy(value))

    def _replace_outlier(self, value):
        data = np.array([val.unpack() for val in self.buffer.buffer])
        data = np.vstack((data, value.unpack()))
        data = np.where(
            (data < const.NON_OUTLIER_MIN) | (data > const.NON_OUTLIER_MAX),
            np.nan,
            data
        )
        num_rows, num_cols = data.shape

        for col_index in range(num_cols):
            missing_indices = np.isnan(data[:, col_index])
            indices = np.arange(num_rows)
            known_indices = indices[~missing_indices]
            known_values = data[:, col_index][~missing_indices]

            interpolation_function = np.polyfit(known_indices, known_values, 2)
            interpolated_values = np.polyval(interpolation_function, indices)

            if np.any(interpolated_values[missing_indices] < 0):
                interpolated_values[interpolated_values < 0] = np.nan
                nan_indices = np.isnan(interpolated_values)
                interpolated_values[nan_indices] = np.interp(indices[nan_indices], indices[~nan_indices], interpolated_values[~nan_indices])

            data[:, col_index] = np.where(missing_indices, interpolated_values, data[:, col_index])

        value.update(*data[-1, :])
        return value
