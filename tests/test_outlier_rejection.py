import unittest
import numpy as np
from src.algorithms import OutlierRejection, Buffer
from src import constants as const
from src.utils import MeasurementAnalyzer, Measurements

class TestOutlierRejection(unittest.TestCase):
    def setUp(self):
        self.outlier_rejection_KF = OutlierRejection(outlier_replacement=False)
        self.outlier_rejection_interp = OutlierRejection(outlier_replacement=True)

    def test_outlier_replacement_interpolation(self):
        data = np.array([
            [1.6052181512462043, 3.2755388898841376, 3.559540043732787, 2.3299715182015692],
            [1.606994116504938, 3.196743735615047, 3.5717090818041655, 2.339728642784736],
            [1.611613924761454, 3.1382444811787225, 3.6130426179411788, 2.3469992597819935],
            [1.6148873749807084, 3.096678365347832, 3.643000276875539, 2.352139905062431],
            [1.607386519143341, 3.063941655549736, 3.655990232829687, 2.3562109275131684]
        ])
        buffer = np.array([Measurements(*val) for val in data])

        for elem in buffer:
            self.outlier_rejection_interp.add_to_buffer(elem)

        outlier_measurement = Measurements(1.590000033, 2.400000095, 3.700000048, -31.84000015)
        clean_measurement = self.outlier_rejection_interp.filter_outlier(outlier_measurement)
        interpolated_measurement = self._interpolate_and_replace_outlier(buffer, outlier_measurement)
        self.assertEqual(clean_measurement.unpack(), interpolated_measurement.unpack())
    
    def _interpolate_and_replace_outlier(self, buffer, value):
        data = np.array([val.unpack() for val in buffer])
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

    def test_outlier_replacement_single_outlier(self):
        outlier_measurement = Measurements(1.61000001, 3.16000009, 3.5999999, -11.11999989)
        clean_measurement = self.outlier_rejection_KF.filter_outlier(outlier_measurement)
        self.assertEqual(clean_measurement.unpack(), (1.61000001, 3.16000009, 3.5999999, None))

    def test_outlier_replacement_multiple_outliers(self):
        outlier_measurement = Measurements(1.64999998, 193.0200043, 3.82999992, -290.6099854)
        clean_measurement = self.outlier_rejection_KF.filter_outlier(outlier_measurement)
        self.assertEqual(clean_measurement.unpack(), (1.64999998, None, 3.82999992, None))

if __name__ == '__main__':
    unittest.main()
