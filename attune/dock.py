import os
import plistlib
import subprocess


class Dock:
    def get_plist_path(self):
        return os.path.expanduser("~/Library/Preferences/com.apple.dock.plist")

    def load_plist(self):
        plist_path = self.get_plist_path()
        with open(plist_path, "rb") as f:
            return plistlib.load(f)

    def save_plist(self, plist_data):
        plist_path = self.get_plist_path()
        with open(plist_path, "wb") as f:
            plistlib.dump(plist_data, f)

    def restart(self):
        subprocess.run(["killall", "Dock"], check=True)

    def filter_apps(self, plist_data, keep_apps):
        persistent_apps = plist_data.get("persistent-apps", [])
        filtered_apps = [
            app
            for app in persistent_apps
            if any(app["tile-data"].get("file-label") == name for name in keep_apps)
        ]
        return filtered_apps
