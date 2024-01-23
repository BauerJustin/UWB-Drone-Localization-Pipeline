from .uwb_network_simulator import UWBNetworkSimulator
from .uwb_token_ring_simulator import UWBTokenRingSimulator
from src import constants as const

simulator_mapping = {"Network": UWBNetworkSimulator, "TokenRing": UWBTokenRingSimulator}

class Simulator:
    def __init__(self, num_drones, simulator_type="TokenRing" if const.ORCHESTRATOR else "Network"):
        assert simulator_type in simulator_mapping, f"Simulator type {simulator_type} is not supported."
        self.simulator_type = simulator_type
        self.simulator = simulator_mapping[self.simulator_type](num_drones)

    def start(self):
        self.simulator.start()

    def stop(self):
        self.simulator.stop()
