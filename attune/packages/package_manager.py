import subprocess
from abc import ABC, abstractmethod


class PackageManager(ABC):
    def install(self, package_name, *opts):
        if not self.is_installed(package_name):
            print(
                f"'{package_name}' is not installed. Installing using {self.name()}..."
            )
            self.install_impl(package_name, *opts)
        else:
            print(f"'{package_name}' is already installed.")

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
    def install_impl(self, package_name, *opts):
        pass
