import platform
import subprocess

from attune.actions.sync.steps.sync_step import SyncStep
from attune.fonts import get_font_config, get_font_ids

if platform.system() == "Windows":
    from attune.platforms.windows import is_font_installed
elif platform.system() == "Darwin":
    from attune.platforms.mac import is_font_installed


class InstallFontsStep(SyncStep):
    @staticmethod
    def create():
        return InstallFontsStep()

    def desc(self):
        return "Checking font dependencies"

    def run(self):
        for id in get_font_ids():
            install_font_prereq(id)


def install_font_prereq(font_id):
    config = get_font_config(font_id)
    family = config.get("family")

    if is_font_installed(family):
        print(f"'{family}' is already installed.")
        return

    print(f"'{family}' is not installed. Installing using oh-my-posh...")
    pkg_id = config.get("pkg")
    try:
        subprocess.run(
            ["oh-my-posh", "font", "install", pkg_id],
            stdout=subprocess.DEVNULL,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing font '{pkg_id}': {e.stderr}")
