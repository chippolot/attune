import subprocess

from attune.packages.package_manager import PackageManager


class WinGetPackageManager(PackageManager):
    installed_packages = None

    def name(self):
        return "winget"

    def _install_from_config(self, config):
        name = config["name"]

        homebrew_config = self._get_install_config()
        id = homebrew_config["id"]

        self._install(name, id, None)

    def _install(self, name, id, args):
        try:
            result = subprocess.run(
                ["winget", "install", "--id", id, "-e", "--source", "winget"],
                check=True,
                text=True,
                capture_output=True,
            )
            if result.stderr:
                print(result.stderr)
        except subprocess.CalledProcessError as e:
            print(
                f"An error occurred while installing {self.name()} pkg '{name}': {e.stderr}"
            )

    def is_installed(self, package_name):
        # Optimization on making multiple install checks per run
        if WinGetPackageManager.installed_packages is None:
            WinGetPackageManager.installed_packages = (
                subprocess.run(["winget", "list"], text=True, capture_output=True)
                .stdout.strip()
                .splitlines()
            )
        return any(package_name in l for l in WinGetPackageManager.installed_packages)
