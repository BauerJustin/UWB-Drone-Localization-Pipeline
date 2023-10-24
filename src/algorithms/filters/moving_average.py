from src import constants as const

class MovingAverageFilter:
    def __init__(self, filter_rate=const.MOVING_AVG_FILTER_RATE):
        self.filter_rate = filter_rate

    def update(self, pos, new_pos):
        pos.x = pos.x * (1 - self.filter_rate) + new_pos.x * self.filter_rate
        pos.y = pos.y * (1 - self.filter_rate) + new_pos.y * self.filter_rate
        pos.z = pos.z * (1 - self.filter_rate) + new_pos.z * self.filter_rate
