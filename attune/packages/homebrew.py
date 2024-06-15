import subprocess

from attune.packages.package_manager import PackageManager


class HomebrewPackageManager(PackageManager):
    def name(self):
        return "brew"

    def install_impl(self, package_name, *opts):
        try:
            result = subprocess.run(
                ["brew", "install", package_name] + [*opts],
                check=True,
                text=True,
                capture_output=True,
            )
            print(f"'{package_name}' installed successfully.")
            if result.stderr:
                print(result.stderr)
        except subprocess.CalledProcessError as e:
            print(
                f"An error occurred while installing {self.name()} pkg '{package_name}': {e.stderr}"
            )
