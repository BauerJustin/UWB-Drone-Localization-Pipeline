from src import constants as const

class MovingAverageFilter:
    def __init__(self, filter_rate=const.MOVING_AVG_FILTER_RATE):
        self.filter_rate = filter_rate

    def update(self, state, measurement):
        state.update(*[
            s * (1 - self.filter_rate) + m * self.filter_rate
            for s, m in zip(state.unpack(), measurement.unpack())
        ])
