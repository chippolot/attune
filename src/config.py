import subprocess
import os
import json
import shutil

def get_attune_path():
    home_dir = os.path.expanduser("~")
    attune_path = os.path.join(home_dir, ".attune")
    if not os.path.exists(attune_path):
        os.makedirs(attune_path)
    return attune_path

def get_config_path():
    return os.path.join(get_attune_path(), "config.json")

def get_or_create_config():
    config_path = get_config_path()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_config_path = os.path.join(script_dir, "../", "config", "config.defaults.json")

    # Copy the default config file if the config file doesn't exist
    if not os.path.exists(config_path):
        shutil.copy(default_config_path, config_path)

    # Load and return the config
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    
    return config

def edit_config(args):
    # Force config creation
    get_or_create_config()
    config_path = get_config_path()
    try:
        subprocess.run(['code.cmd', config_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to open {config_path} with VSCode: {e}")

def save_config(config):
    config_path = get_config_path()
    try:
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)
    except Exception as e:
        print(f"Failed to save config to {config_path}: {e}")