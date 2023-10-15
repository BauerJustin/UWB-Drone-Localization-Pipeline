# UWB-Drone-Localization-Pipeline
ECE496 Capstone Indoor Drone Swarm Localization with UWB

## Prerequisites

Before running the simulation, make sure you have the following prerequisites installed on your system:

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

You can run the UWB drone simulation with the following command:

```bash
python3 main.py [--sim_uwb] [--num_drones N]
```

### Options

- `--sim_uwb`: Use this flag to enable UWB drone simulation.
- `--num_drones N`: Specify the number of drones for the simulation (default is 3 if not provided).

### Examples

1. To run the UWB drone simulation with the default number of drones (3 drones):

   ```bash
   python3 main.py --sim_uwb
   ```

2. To run the UWB drone simulation with a custom number of drones (e.g., 5 drones):

   ```bash
   python3 main.py --sim_uwb --num_drones 5
   ```

### Tests

To run all unit tests use the following command:

```bash
python3 -m unittest discover
```
