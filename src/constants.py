# Drone Tracker
BASE = "measurement"  # pos, measurement

FIRST_UPDATES_SKIPPED = 0

FILTER_ENABLED = True
FILTER_TYPE = "KF"  # MA (Moving Average), KF (Kalman Filter), EKF (Extended Kalman Filter)

BUFFER_ENABLED = True
BUFFER_MODE = 'last'  # avg, last
BUFFER_SIZE = 20
BUFFER_FILTER_OUTLIERS = True

OUTLIER_REPLACEMENT_ENABLED = False
OUTLIER_REJECTION_VERSION = "V2" # "V1", "V2"

MEASURE_VARIANCE = True
VARIANCE_SIZE = 20

# Multilateration settins
USE_LAST_POS = True

# MA settings
MOVING_AVG_FILTER_RATE = 0.9

# Simulator
SIMULATOR_FREQUENCY = 10
TRAJECTORY_PERCENTAGE_CHANGE = 0.01

ADD_GAUSSIAN_NOISE = True
GAUSSIAN_NOISE_MEAN = 0.0
GAUSSIAN_NOISE_STD = 0.1

OUTLIER_INJECTION_REALISTIC_ENABLED = True
OUTLIER_MIN = -327
OUTLIER_MAX = 327
OUTLIER_PROBABILITY = 0.30
OUTLIER_MULTIPLIER = 1.5

# Visualizer
PLOT_GROUND_TRUTH = True
