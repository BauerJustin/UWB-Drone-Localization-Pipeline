import json


def load_anchor_positions(anchor_config='./config/anchor_config.json'):
    with open(anchor_config, 'r') as f:
        config = json.load(f)
    return config

def load_network_host(network_config='./config/network_config.json'):
    with open(network_config, 'r') as f:
        config = json.load(f)
    host = config['host']
    port = config['port']
    return host, port
