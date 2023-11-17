# UWB-Drone-Localization-Pipeline
ECE496 Capstone Indoor Drone Swarm Localization and Control with UWB

## Prerequisites

Before running the pipeline, make sure you have the following prerequisites installed on your system:

- Python 3: You can download and install Python 3 from the [official website](https://www.python.org/downloads/).

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/BauerJustin/UWB-Drone-Localization-Pipeline.git
   ```

2. Navigate to the project directory:

   ```bash
   cd UWB-Drone-Localization-Pipeline
   ```

3. Install the required dependencies using pip:

   ```bash
   pip3 install -r requirements.txt
   ```

## Usage

### Localization

Run the UWB drone localization pipeline with the following command:

```bash
python3 drone_localization.py [--sim_uwb] [--num_drones N] [--capture] [--replay] [--file_name FILE]
```

#### Options:

- `--sim_uwb`: Use this flag to enable UWB drone simulation.
- `--num_drones N`: Specify the number of drones for the simulation (default is 3 if not provided).
- `--capture`: Capture all incoming data.
- `--replay`: Replay capture file.
- `--file_name FILE`: Set the capture or replay file (default is capture.json).

### Control

Run the UWB drone control pipeline with the following command:

```bash
python3 drone_control.py
```

## Tests

To run all unit tests use the following command:

```bash
python3 -m unittest discover
```
