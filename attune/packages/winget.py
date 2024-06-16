import subprocess

from attune.packages.package_manager import PackageManager


class WinGetPackageManager(PackageManager):
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
