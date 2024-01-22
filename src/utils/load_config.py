import json
import logging
import os

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

def load_kf_settings(base='pos'):
    base = base.lower()
    if base != 'pos' and base != 'measurement':
        raise Exception(f"Invalid base for kalman filter: {base}")
    kf_config = f'./config/{base}_kf_config.json'
    with open(kf_config, 'r') as f:
        config = json.load(f)
    return config

def setup_logger(module_name):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    os.makedirs('./logs/', exist_ok=True)
    file_handler = logging.FileHandler('./logs/logfile.log')
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger