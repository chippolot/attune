import json
import os
import shutil

from attune.dict import get_dict_value, set_dict_value
from attune.paths import get_attune_file_path, get_repo_file_path


class Config:
    cfg = {}

    @staticmethod
    def path():
        return os.path.join(get_attune_file_path(), "config.json")

    @staticmethod
    def exists():
        return os.path.exists(Config.path())

    @staticmethod
    def load():
        config_path = Config.path()

        default_config_path = get_repo_file_path("config/config.defaults.json")

        # Copy the default config file if the config file doesn't exist
        if not os.path.exists(config_path):
            shutil.copy(default_config_path, config_path)

        # Load and return the config
        with open(config_path, "r", encoding="utf-8") as config_file:
            cfg = json.load(config_file)

        return Config(cfg)

    def __init__(self, cfg) -> None:
        self.cfg = cfg

    def get(self, path, default=None):
        return get_dict_value(self.cfg, path, default)

    def set(self, path, value):
        set_dict_value(self.cfg, path, value)

    def save(self):
        config_path = Config.path()
        try:
            with open(config_path, "w", encoding="utf-8") as config_file:
                json.dump(self.cfg, config_file, indent=4)
        except Exception as e:
            print(f"Failed to save config to {config_path}: {e}")
