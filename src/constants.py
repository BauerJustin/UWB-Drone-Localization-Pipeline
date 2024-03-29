# Anchor positions
CONFIG_DATE = 'mar23'

# Drone Tracker
FILTER_DUPLICATE_MEASUREMENTS = True
DROP_PARTIAL_MEASUREMENTS = False

FILTER_TYPE = "KF"  # MA (Moving Average), KF (Kalman Filter) - to disable set MA with 1.0

NON_OUTLIER_MIN, NON_OUTLIER_MAX = 0, 5
OUTLIER_REJECTION_ENABLED = True
OUTLIER_INTERPOLATION_ENABLED = False  # True: Quad interpolation, False: Rely on Filter
OUTLIER_INTERPOLATION_BUFFER_SIZE = 20
OUTLIER_INTERPOLATION_MIN_BUFFER = 5

UPDATE_FREQ_AVG = True
UPDATE_FREQ_BUFFER_SIZE = 10
PRINT_TIME_INTERVALS = True
PRINT_RAW_MEASUREMENTS = True

MEASURE_VARIANCE = True
VARIANCE_SIZE = 5

ORCHESTRATOR = True
ORCHESTRATOR_TIMEOUT = 5.0

# Multilateration settings
USE_LAST_POS = True

# MA settings
MOVING_AVG_FILTER_RATE = 0.9

# Drone Control
SWARM_MODE = True
DRONE_CALIBRATION = False
DRONE_STATIC = True

# Simulator
SIMULATOR_PROCESSING_MIN, SIMULATOR_PROCESSING_MAX = 0.125, 0.25  # TokenRing
SIMULATOR_FREQUENCY = 10  # Network
SIMULATOR_DROP_RATE = 0.4

TRAJECTORY_PERCENTAGE_CHANGE = 0.05

ADD_GAUSSIAN_NOISE = True
GAUSSIAN_NOISE_MEAN = 0.0
GAUSSIAN_NOISE_STD = 0.1

OUTLIER_INJECTION_ENABLED = True
OUTLIER_INJECTION_MIN, OUTLIER_INJECTION_MAX = -327, 327
OUTLIER_INJECTION_PROBABILITY = 0.30

# Visualizer
PLOT_GROUND_TRUTH = True
PLOT_ERROR_MIN = 0.15  # 15 cm
