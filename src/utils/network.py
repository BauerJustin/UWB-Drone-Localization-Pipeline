import json

def load_network_host(network_config='./config/network_config.json'):
    with open(network_config, 'r') as f:
        config = json.load(f)
    host = config['host']
    port = config['port']
    return host, port
