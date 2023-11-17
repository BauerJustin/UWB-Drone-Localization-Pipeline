# UWB-Drone-Localization-Pipeline
ECE496 Capstone Indoor Drone Swarm Localization with UWB

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

Run the UWB drone localization pipeline with the following command:

```bash
python3 main.py [--sim_uwb] [--num_drones N] [--capture] [--replay] [--file_name FILE]
```

### Options

- `--sim_uwb`: Use this flag to enable UWB drone simulation.
- `--num_drones N`: Specify the number of drones for the simulation (default is 3 if not provided).
- `--capture`: Capture all incoming data.
- `--replay`: Replay capture file.
- `--file_name FILE`: Set the capture or replay file (default is capture.json).

### Examples

1. To run the UWB drone simulation with the default number of drones (3 drones):

   ```bash
   python3 main.py --sim_uwb
   ```

2. To run the UWB drone simulation with a custom number of drones (e.g., 5 drones):

   ```bash
   python3 main.py --sim_uwb --num_drones 5
   ```

3. To capture incoming data to default file (`capture.json`)

   ```bash
   python3 main.py --capture
   ```

4. To capture incoming data to specific file (e.g., `data_capture.json`)

   ```bash
   python3 main.py --capture --file_name data_capture.json
   ```

5. To replay data capture from default file (`capture.json`)
    
   ```bash
   python3 main.py --replay
   ```

6. To replay data capture from specific file (e.g., `data_capture.json`)

   ```bash
   python3 main.py --replay --file_name data_capture.json
   ```

## Drone Control

Install the DJITelloPy (https://github.com/damiafuentes/DJITelloPy) package using either of the following options:

### Install using pip

```bash
pip3 install djitellopy
```

### Install in developer mode
The below commands allow you modify the library locally for your purposes.

```bash
git clone https://github.com/damiafuentes/DJITelloPy.git
cd DJITelloPy
pip install -e .
```

### Usage
Drone control can be initiated by the same command used to run the UWB drone localization pipeline:
```bash
python3 main.py [--sim_uwb] [--num_drones N] [--capture] [--replay] [--file_name FILE]
```

## Tests

To run all unit tests use the following command:

```bash
python3 -m unittest discover
```
