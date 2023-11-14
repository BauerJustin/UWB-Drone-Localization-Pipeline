# Drone Tracker
FILTER_ENABLED = True
FILTER_TYPE = "KF"  # MA (Moving Average), KF (Kalman Filter), EKF (Extended Kalman Filter)

BUFFER_ENABLED = False
BUFFER_SIZE = 10
BUFFER_FILTER_OUTLIERS = True
BUFFER_MIN_FILTER_LEN = 5

# MA settings
MOVING_AVG_FILTER_RATE = 0.9

# KF settings
INITIAL_COVARIANCE = [
    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
]
PROCESS_NOISE = [
    [0.01, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.01, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.01, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.01, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.01, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.01]
]
MEASUREMENT_NOISE = [
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0]
]
TRANSITION_MATRIX = [
    [1.0, 0.0, 0.0, 1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0, 0.0, 0.0, 1.0],
    [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
]
OBSERVATION_MATRIX = [
    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
]

# Simulator
SIMULATOR_FREQUENCY = 10
TRAJECTORY_PERCENTAGE_CHANGE = 0.01  # 1%

ADD_GAUSSIAN_NOISE = True
GAUSSIAN_NOISE_MEAN = 0.0
GAUSSIAN_NOISE_STD = 0.01

OUTLIER_INJECTION_ENABLED = False
OUTLIER_PROBABILITY = 0.01  # Probability of injecting an outlier measurement
OUTLIER_MULTIPLIER_MIN = 0.5  # Minimum multiplier for outlier measurements
OUTLIER_MULTIPLIER_MAX = 2.0  # Maximum multiplier for outlier measurements

# Visualizer
PLOT_GROUND_TRUTH = True
