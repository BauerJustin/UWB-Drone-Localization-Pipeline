from .filters import MovingAverageFilter, KalmanFilter, ExtendedKalmanFilter

filter_mapping = {"MA": MovingAverageFilter, "KF": KalmanFilter, "EKF": ExtendedKalmanFilter}

class Filter:
    def __init__(self, filter_type):
        assert filter_type in filter_mapping, f"Filter type {filter_type} is not supported."
        self.filter_type = filter_type
        self.filter = filter_mapping[self.filter_type]()

    def update_pos(self, pos, new_pos):
        self.filter.update(pos, new_pos)
