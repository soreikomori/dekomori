# usr/bin/env python3
# -*- coding: utf-8 -*-
# Config Handler
import json
import os

configPath = os.path.join(os.path.dirname(__file__), '../../env/config.json')

def load_config():
    """
    Loads the configuration file.
    
    Returns
    -------
    dict
        A dictionary containing the configuration settings.
    """
    if not os.path.exists(configPath):
        raise FileNotFoundError(f"Configuration file not found: {configPath}")
    
    with open(configPath, 'r') as config_file:
        config = json.load(config_file)
        return config
    
def save_config(config):
    """
    Saves the configuration to the file.
    
    Parameters
    ----------
    config : dict
        A dictionary containing the configuration settings to save.
    """
    with open(configPath, 'w') as config_file:
        json.dump(config, config_file, indent=4, ensure_ascii=False)

def update_config(key, value):
    """
    Updates a specific key in the configuration file.
    
    Parameters
    ----------
    key : str
        The key to update in the configuration file.
    value : any
        The new value to set for the specified key.
    """
    config = load_config()
    config[key] = value
    save_config(config)

def get_config(key):
    """
    Retrieves the value of a specific key from the configuration file.
    
    Parameters
    ----------
    key : str
        The key to retrieve from the configuration file.
    
    Returns
    -------
    any
        The value associated with the specified key.
    """
    config = load_config()
    return config.get(key, None)