import subprocess
from abc import ABC, abstractmethod

from attune import features, gum


class PackageManager(ABC):
    def install_from_id(self, name, id):
        if self.is_installed(id):
            print(f"'{name}' is already installed.")
            return
        self._install(name, id, None)

    def install_from_config(self, config):
        name = config["name"]

        install_config = self._get_install_config(config)
        if install_config is None:
            return

        id = install_config["id"]
        if not self.is_installed(id):
            if config.get("optional", False) is True:
                if not gum.confirm(f"Do you want to install '{name}'?"):
                    return

            print(f"'{name}' is not installed. Installing using {self.name()}...")
            self._install_from_config(config)

            feature = config.get("feature", None)
            if feature is not None:
                features.enable(feature)
        else:
            print(f"'{name}' is already installed.")

    def is_installed(self, package_name):
        try:
            result = subprocess.run(
                [self.name(), "list", package_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
            )
            if result.returncode == 0:
                return True
            else:
                return False
        except FileNotFoundError:
            print(f"{self.name()} is not installed or not found in the PATH.")
            return False

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def _install_from_config(self, config):
        pass

    @abstractmethod
    def _install(self, name, id, args):
        pass

    def _get_install_config(self, config):
        return config["packages"].get(self.name(), None)
