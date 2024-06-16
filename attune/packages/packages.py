import json
import platform

from attune.packages.homebrew import HomebrewPackageManager
from attune.packages.winget import WinGetPackageManager
from attune.paths import get_repo_file_path


def get_package_manager():
    if platform.system() == "Windows":
        return WinGetPackageManager()
    elif platform.system() == "Darwin":
        return HomebrewPackageManager()


def get_packages_config():
    path = get_repo_file_path("themes/packages.json")
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {path}")
