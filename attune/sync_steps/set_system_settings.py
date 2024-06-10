import platform
import shutil
import subprocess

from attune.sync_steps.sync_step import SyncStep


class SyncStepSetSystemSettings(SyncStep):
    @staticmethod
    def create():
        if platform.system() == "Windows":
            return WindowsSyncStepSetSystemSettings()
        elif platform.system() == "Darwin":
            return MacSyncStepSetSystemSettings()
        else:
            print("Unsupported platform")

    def desc(self):
        return "Updating system settings"

    def run(self):
        pass

class WindowsSyncStepSetSystemSettings(SyncStepSetSystemSettings):
    def run(self):
        pass # Nothing here yet!


class MacSyncStepSetSystemSettings(SyncStepSetSystemSettings):
    def run(self):
        subprocess.run(["defaults", "write", "com.apple.driver.AppleBluetoothMultitouch.trackpad", "Clicking", "-bool", "true"], check=True)
        subprocess.run(["defaults", "write", "com.apple.AppleMultitouchTrackpad", "Clicking", "-bool", "true"], check=True)
        subprocess.run(["/System/Library/PrivateFrameworks/SystemAdministration.framework/Resources/activateSettings", "-u"], check=True)