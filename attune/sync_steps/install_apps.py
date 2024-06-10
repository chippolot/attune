import platform
import shutil
import subprocess

from attune.sync_steps.sync_step import SyncStep


class SyncStepInstallApps(SyncStep):
    @staticmethod
    def create():
        if platform.system() == "Windows":
            return WindowsSyncStepInstallApps()
        elif platform.system() == "Darwin":
            return MacSyncStepInstallApps()
        else:
            print("Unsupported platform")

    def desc(self):
        return "Checking app dependencies"

    def run(self):
        pass


class WindowsSyncStepInstallApps(SyncStepInstallApps):
    def run(self):
        self.__install("visual studio code", "code", "Microsoft.VisualStudioCode")
        self.__install("terminal", "wt", "Microsoft.WindowsTerminal")
        self.__install("oh-my-posh", "oh-my-posh", "JanDeDobbeleer.OhMyPosh")

    def __install(self, app_desc, app_name, pkg_id):
        if shutil.which(app_name) is None:
            print(f"'{app_desc}' is not installed. Installing using winget...")
            try:
                result = subprocess.run(
                    ["winget", "install", "--id", pkg_id, "-e", "--source", "winget"],
                    check=True,
                    text=True,
                    capture_output=True,
                )
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
            except subprocess.CalledProcessError as e:
                print(
                    f"An error occurred while installing winget pkg '{app_desc}': {e.stderr}"
                )
        else:
            print(f"'{app_desc}' is already installed.")


class MacSyncStepInstallApps(SyncStepInstallApps):
    def run(self):
        self.__install("visual studio code", "code", "--cask visual-studio-code")
        self.__install(
            "oh-my-posh", "oh-my-posh", "jandedobbeleer/oh-my-posh/oh-my-posh"
        )
        self.__install("fontconfig", "fc-list", "fontconfig")

    def __install(self, app_desc, app_name, pkg_id):
        if shutil.which(app_name) is None:
            print(f"'{app_desc}' is not installed. Installing using brew...")
            try:
                result = subprocess.run(
                    ["brew", "install", pkg_id],
                    check=True,
                    text=True,
                    capture_output=True,
                )
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
            except subprocess.CalledProcessError as e:
                print(
                    f"An error occurred while installing brew pkg '{app_desc}': {e.stderr}"
                )
        else:
            print(f"'{app_desc}' is already installed.")
