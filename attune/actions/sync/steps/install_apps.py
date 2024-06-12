import platform

from attune import module
from attune.actions.sync.steps.sync_step import SyncStep
from attune.packages.packages import get_package_manager


class InstallAppsStep(SyncStep):
    @staticmethod
    def create():
        if platform.system() == "Windows":
            return WindowsInstallAppsStep()
        elif platform.system() == "Darwin":
            return MacInstallAppsStep()
        else:
            raise Exception("Unsupported platform")

    def desc(self):
        return "Checking app dependencies"

    def run(self):
        pass


class WindowsInstallAppsStep(InstallAppsStep):
    def run(self):
        package_manager = get_package_manager()
        if module.is_enabled(module.Modules.VSCODE):
            package_manager.install("Microsoft.VisualStudioCode")
        package_manager.install("Microsoft.WindowsTerminal")
        package_manager.install("JanDeDobbeleer.OhMyPosh")


class MacInstallAppsStep(InstallAppsStep):
    def run(self):
        package_manager = get_package_manager()
        if module.is_enabled(module.Modules.VSCODE):
            package_manager.install("visual-studio-code", "--cask")
        package_manager.install("iterm2", "--cask")
        if module.is_enabled(module.Modules.CHATGPT):
            package_manager.install("chatgpt", "--cask")
        package_manager.install("jandedobbeleer/oh-my-posh/oh-my-posh")
        package_manager.install("fontconfig")
        package_manager.install("dockutil")
