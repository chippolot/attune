import platform

from attune.actions.sync.steps.sync_step import SyncStep
from attune.packages.packages import get_system_package_manager


class InstallGumStep(SyncStep):
    @staticmethod
    def create():
        if platform.system() == "Windows":
            return WindowsInstallGumStep()
        elif platform.system() == "Darwin":
            return MacInstallGumStep()
        else:
            raise Exception("Unsupported platform")

    def desc(self):
        return "Checking app dependencies"

    def run(self):
        pass


class WindowsInstallGumStep(InstallGumStep):
    def run(self):
        package_manager = get_system_package_manager()
        package_manager.install_from_id("Gum", "charmbracelet.gum")


class MacInstallGumStep(InstallGumStep):
    def run(self):
        package_manager = get_system_package_manager()
        package_manager.install_from_id("Gum", "gum")
