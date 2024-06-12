import subprocess

from attune.packages.package_manager import PackageManager


class WinGetPackageManager(PackageManager):
    def name(self):
        return "winget"

    def install_impl(self, package_name, *opts):
        try:
            result = subprocess.run(
                ["winget", "install", "--id", package_name, "-e", "--source", "winget"],
                check=True,
                text=True,
                capture_output=True,
            )
            if result.stderr:
                print(result.stderr)
        except subprocess.CalledProcessError as e:
            print(
                f"An error occurred while installing {self.name()} pkg '{package_name}': {e.stderr}"
            )
