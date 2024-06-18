import platform

from attune.packages.homebrew import HomebrewPackageManager
from attune.packages.winget import WinGetPackageManager


def get_package_manager():
    if platform.system() == "Windows":
        return WinGetPackageManager()
    elif platform.system() == "Darwin":
        return HomebrewPackageManager()
