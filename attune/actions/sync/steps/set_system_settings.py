import platform
import subprocess

from attune.actions.sync.steps.sync_step import SyncStep


class SetSystemSettingsStep(SyncStep):
    @staticmethod
    def create():
        if platform.system() == "Windows":
            return WindowsSetSystemSettingsStep()
        elif platform.system() == "Darwin":
            return MacSetSystemSettingsStep()
        else:
            raise Exception("Unsupported platform")

    def desc(self):
        return "Updating system settings"

    def run(self):
        pass


class WindowsSetSystemSettingsStep(SetSystemSettingsStep):
    def run(self):
        pass  # Nothing here yet!


class MacSetSystemSettingsStep(SetSystemSettingsStep):
    def run(self):
        subprocess.run(
            [
                "defaults",
                "write",
                "com.apple.driver.AppleBluetoothMultitouch.trackpad",
                "Clicking",
                "-bool",
                "true",
            ],
            check=True,
        )
        subprocess.run(
            [
                "defaults",
                "write",
                "com.apple.AppleMultitouchTrackpad",
                "Clicking",
                "-bool",
                "true",
            ],
            check=True,
        )
        subprocess.run(
            [
                "/System/Library/PrivateFrameworks/SystemAdministration.framework/Resources/activateSettings",
                "-u",
            ],
            check=True,
        )
