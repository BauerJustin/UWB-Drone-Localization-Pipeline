import numpy as np
import json
import pprint

class MeasurementAnalyzer:
    def __init__(self, file_name):
        self.file_name = file_name
        self.measurements = self.load_data()
        self.total_data = len(self.measurements)

        self.outlier_data_info = {}
        self.incomplete_data_info = {}
        
        self.data_with_outliers = []
        self.data_without_outliers = []
        self.data_incomplete = []
        self.data_complete = []
        self.data_complete_without_outliers = []
        
        self.total_complete_data_without_outliers = 0
        self.total_outliers = 0
        self.total_incomplete_data = 0


    def load_data(self):
        try:
            with open(f'./captures/{self.file_name}', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("File not found. Please check the file path.")
            return []
        except json.JSONDecodeError as e:
            raise Exception(f"Error decoding JSON: {e}")
        
        anchor_distances = []
        for _, packet in data:
            distances = packet["measurements"]
            anchor_distances.append([distances.get("81", 0), distances.get("82", 0), distances.get("83", 0), distances.get("84", 0)])

        return np.array(anchor_distances)

    def analyze(self):
        self.data_with_outliers, self.data_without_outliers = self.extract_outliers()

        self.data_incomplete, self.data_complete = self.extract_incomplete_data()
        self.total_data_complete = len(self.data_complete)
        self.total_incomplete_data = len(self.data_incomplete)

        self.data_complete_without_outliers = self.remove_incomplete_and_outlier_data()
        self.total_complete_data_without_outliers = len(self.data_complete_without_outliers)

        self.extract_outlier_data_info()
        self.extract_incomplete_data_info()
        self.print_relevant_details()

    def extract_outliers(self):
        for distances in self.measurements:
            if any(value < 0 or value > 5 for value in distances):
                self.data_with_outliers.append(distances)
            else:
                self.data_without_outliers.append(distances)

        return np.array(self.data_with_outliers), np.array(self.data_without_outliers)

    def extract_incomplete_data(self):
        for distances in self.measurements:
            if any(value == 0 for value in distances):
                self.data_incomplete.append(distances)
            else:
                self.data_complete.append(distances)
        return np.array(self.data_incomplete), np.array(self.data_complete)

    def remove_incomplete_and_outlier_data(self):
        for distances in self.data_without_outliers:
            if not any(value == 0 for value in distances):
                self.data_complete_without_outliers.append(distances)
        return np.array(self.data_complete_without_outliers)

    def extract_outlier_data_info(self):
        anchor_ids = ['81', '82', '83', '84']
        for i in range(len(self.measurements)):
            for dist_idx, dist in enumerate(self.measurements[i]):
                temp = {'index': [], 'count': 0, 'anchor_id': set()}
                if dist < 0 or dist > 5:
                    self.outlier_data_info.setdefault(dist, temp)
                    self.outlier_data_info[dist]['count'] += 1
                    self.outlier_data_info[dist]['index'].append(i)
                    self.outlier_data_info[dist]['anchor_id'].add(anchor_ids[dist_idx])
                    self.total_outliers += 1

    def extract_incomplete_data_info(self):
        anchor_ids = ['81', '82', '83', '84']
        for i in range(len(self.measurements)):
            for dist_idx, dist in enumerate(self.measurements[i]):
                if dist == 0:
                    temp = {'anchor_id': [], 'incomplete_measurement': 0}
                    temp_str = f'measurement_idx_{i}'
                    self.incomplete_data_info.setdefault(temp_str, temp)
                    self.incomplete_data_info[temp_str]['anchor_id'].append(anchor_ids[dist_idx])
                    self.incomplete_data_info[temp_str]['incomplete_measurement'] = self.measurements[i]
                    self.total_incomplete_data += 1
                    break

    def print_relevant_details(self):
        print("**RELEVANT INFO**")
        print("total_data: ", self.total_data)
        print("total_outliers: ", self.total_outliers)
        print("total_data_complete: ", self.total_data_complete)
        print("total_incomplete_data: ", self.total_incomplete_data)
        print("total_complete_data_without_outliers: ", self.total_complete_data_without_outliers)
        print(f'Outliers: {(self.total_outliers/self.total_data) * 100}%')

        print(f'\nOutliers Info for {self.file_name} \n')
        pprint.PrettyPrinter(indent=4).pprint(self.outlier_data_info)