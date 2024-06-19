import subprocess

from attune.packages.package_manager import PackageManager


class HomebrewPackageManager(PackageManager):
    installed_packages = None

    def name(self):
        return "brew"

    def _install_from_config(self, config):
        name = config["name"]

        homebrew_config = self._get_install_config(config)
        id = homebrew_config["id"]
        args = []
        if homebrew_config.get("cask", False) is True:
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

    def is_installed(self, package_name):
        id = package_name.split("/")[-1]

        # Optimization on making multiple install checks per run
        if HomebrewPackageManager.installed_packages is None:
            HomebrewPackageManager.installed_packages = (
                subprocess.run(["brew", "list", "-1"], text=True, capture_output=True)
                .stdout.strip()
                .splitlines()
            )
        return id in HomebrewPackageManager.installed_packages
