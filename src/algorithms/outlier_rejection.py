import numpy as np
from src import constants as const
from src.utils import load_config

class OutlierRejection:
    def __init__(self, outlier_replacement="V3"):
        self.outlier_replacement = outlier_replacement
        self.is_active = False
        self.logger = load_config.setup_logger(__name__)

    def _replace_outlier(self, plotted_values, outlier_measurements):
            plotted_values.append(outlier_measurements)
            data = np.array([np.array(val.unpack()) for val in plotted_values])
            data[-1, :][(data[-1, :] < const.REJECT_OUTLIER_MIN) | (data[-1, :] > const.REJECT_OUTLIER_MAX)] = np.nan
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

            outlier_measurements.update(*data[-1, :])

            return outlier_measurements

    def filter_outlier(self, incoming_value, active, plotted_values):
        self.is_active = active
        new_val = np.array(incoming_value.unpack())
        if any(val < const.REJECT_OUTLIER_MIN or val > const.REJECT_OUTLIER_MAX for val in new_val):
            self.logger.info(f'\t Outlier: {new_val}')
            if self.is_active:
                if self.outlier_replacement == "V1":
                    replaced_value = self._replace_outlier(plotted_values, incoming_value)
                    self.logger.info(f'\t Replaced val V1: {replaced_value.unpack()}')
                    return replaced_value
                elif self.outlier_replacement == "V2":
                    new_val_list = new_val.tolist()
                    new_val_list = [None if val < 0 or val > 5 else val for val in new_val_list]
                    incoming_value.update(*new_val_list)
                    return incoming_value
            else:
                return None
        else:
            return incoming_value