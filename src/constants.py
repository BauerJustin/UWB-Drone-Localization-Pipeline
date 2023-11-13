# Drone Tracker Filters
FILTER_ENABLED = True
FILTER_TYPE = "KF"  # MA (Moving Average), KF (Kalman Filter), EKF (Extended Kalman Filter)

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
TRAJECTORY_PERCENTAGE_CHANGE = 0.001  # 0.1%

# Visualizer
PLOT_GROUND_TRUTH = True

# Outlier settings
OUTLIER_PROBABILITY = 0.15  # Probability of injecting an outlier measurement (adjust as needed)
OUTLIER_MULTIPLIER_MIN = 0.5  # Minimum multiplier for outlier measurements (adjust as needed)
OUTLIER_MULTIPLIER_MAX = 2.0  # Maximum multiplier for outlier measurements (adjust as needed)