import json
import os
import shutil
import subprocess

from attune.dict import get_dict_value
from attune.paths import get_attune_file_path, get_repo_file_path


def get_config_path():
    return os.path.join(get_attune_file_path(), "config.json")


def get_or_create_config():
    config_path = get_config_path()
    default_config_path = get_repo_file_path("config/config.defaults.json")

    # Copy the default config file if the config file doesn't exist
    if not os.path.exists(config_path):
        shutil.copy(default_config_path, config_path)

    # Load and return the config
    with open(config_path, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    return config


def get_config_param(config, path):
    config = get_or_create_config()
    value = get_dict_value(config, path)
    return value


def edit_config(args):
    # Force config creation
    get_or_create_config()
    config_path = get_config_path()
    try:
        subprocess.run(["code.cmd", config_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to open {config_path} with VSCode: {e}")


def save_config(config):
    config_path = get_config_path()
    try:
        with open(config_path, "w", encoding="utf-8") as config_file:
            json.dump(config, config_file, indent=4)
    except Exception as e:
        print(f"Failed to save config to {config_path}: {e}")