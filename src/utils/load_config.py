import json
import logging
import os
import socket
from src import constants as const


def load_anchor_positions(anchor_config=f'./config/{const.ANCHOR_CONFIG}'):
    with open(anchor_config, 'r') as f:
        config = json.load(f)
    config = {k: config[k] for k in sorted(config.keys())}  # sort based on key
    return config

def load_network_host(network_config='./config/network_config.json'):
    with open(network_config, 'r') as f:
        config = json.load(f)
    host = config['host']
    port = config['port']
    if host == '127.0.0.1':
        host = get_local_ip()
    return host, port

def load_kf_settings():
    kf_config = f'./config/kf_config.json'
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

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        return local_ip
    except socket.error as e:
        print(f"Get Local IP Error: {e}")
        return None
    