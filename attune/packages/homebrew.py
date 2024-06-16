import subprocess

from attune.packages.package_manager import PackageManager


class HomebrewPackageManager(PackageManager):
    def name(self):
        return "brew"

    def _install_from_config(self, config):
        name = config["name"]

        homebrew_config = self._get_install_config()
        id = homebrew_config["id"]
        args = []
        if homebrew_config["cask"] is True:
            args = ["--cask"]

        self._install(name, id, args)

    def _install(self, name, id, args):
        try:
            result = subprocess.run(
                ["brew", "install", id] + (args or []),
                check=True,
                text=True,
                capture_output=True,
            )
            print(f"'{name}' installed successfully.")
            if result.stderr:
                print(result.stderr)
        except subprocess.CalledProcessError as e:
            print(
                f"An error occurred while installing {self.name()} pkg '{name}': {e.stderr}"
            )
