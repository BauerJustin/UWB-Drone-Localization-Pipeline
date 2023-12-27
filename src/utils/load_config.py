import json


def load_anchor_positions(anchor_config='./config/anchor_config.json'):
    with open(anchor_config, 'r') as f:
        config = json.load(f)
    config = {k: config[k] for k in sorted(config.keys())}  # sort based on key
    return config

def load_network_host(network_config='./config/network_config.json'):
    with open(network_config, 'r') as f:
        config = json.load(f)
    host = config['host']
    port = config['port']
    return host, port

def load_kf_settings(base='pos', filter_type='kf'):
    base, filter_type = base.lower(), filter_type.lower()
    if base != 'pos' and base != 'measurement':
        raise Exception(f"Invalid base for kalman filter: {base}")
    if filter_type != 'kf' and filter_type != 'ekf':
        raise Exception(f"Invalid kalman filter type: {filter_type}")
    kf_config = f'./config/{base}_{filter_type}_config.json'
    with open(kf_config, 'r') as f:
        config = json.load(f)
    return config
