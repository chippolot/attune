import platform
import shutil
import subprocess

from attune.actions.sync.steps.sync_step import SyncStep


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
                if result.stderr:
                    print(result.stderr)
            except subprocess.CalledProcessError as e:
                print(
                    f"An error occurred while installing winget pkg '{app_desc}': {e.stderr}"
                )
        else:
            print(f"'{app_desc}' is already installed.")


class MacInstallAppsStep(InstallAppsStep):
    def run(self):
        self.__install("visual studio code", "--cask", "visual-studio-code")
        self.__install("iterm2", "--cask", "iterm2")
        self.__install("chatGPT", "--cask", "chatgpt")
        self.__install("oh-my-posh", "jandedobbeleer/oh-my-posh/oh-my-posh")
        self.__install("fontconfig", "fontconfig")
        self.__install("dockutil", "dockutil")

    def __install(self, app_desc, *args):
        if not self.__is_brew_package_installed(args[-1]):
            print(f"'{app_desc}' is not installed. Installing using brew...")
            try:
                result = subprocess.run(
                    ["brew", "install"] + [*args],
                    check=True,
                    text=True,
                    capture_output=True,
                )
                print(f"'{app_desc}' installed successfully.")
                if result.stderr:
                    print(result.stderr)
            except subprocess.CalledProcessError as e:
                print(
                    f"An error occurred while installing brew pkg '{app_desc}': {e.stderr}"
                )
        else:
            print(f"'{app_desc}' is already installed.")

    def __is_brew_package_installed(self, package_name):
        try:
            result = subprocess.run(
                ["brew", "list", package_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
            )
            if result.returncode == 0:
                return True
            else:
                return False
        except FileNotFoundError:
            print("Homebrew is not installed or not found in the PATH.")
            return False
