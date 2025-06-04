"""
utils.py - Funciones auxiliares para el bot SMC-LIT
"""

import logging
import yaml
import os

def load_config(config_path: str = '../config.yaml') -> dict:
    """
    Carga configuración YAML.
    """
    if not os.path.exists(config_path):
        return {}
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def setup_logger(name: str = 'smc-lit', level=logging.INFO):
    """
    Configura un logger estándar.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger 