import platform

from attune.packages.homebrew import HomebrewPackageManager
from attune.packages.vscode import VSCodePackageManager
from attune.packages.winget import WinGetPackageManager


def get_system_package_manager():
    if platform.system() == "Windows":
        return WinGetPackageManager()
    elif platform.system() == "Darwin":
        return HomebrewPackageManager()


def install(package_config):
    packages_config = package_config["packages"]
    if packages_config.get("vscode", None) is not None:
        package_manager = VSCodePackageManager()
    else:
        package_manager = get_system_package_manager()
    package_manager.install_from_config(package_config)
